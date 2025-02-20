# 📂 Módulo: `retrainer.py`
# ===================================================================================================

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from trading_bot.db.db_manager import get_historical_data_from_db
from trading_bot.utils.backtester import Backtester
from trading_bot.utils.checkpoint_saver import save_checkpoint, load_checkpoint
from trading_bot.config import crypto_list, Train_Date_Start, Train_Date_End, Batch_Method, QTD_Pack_Batch, QTD_Unique_Batch
from sklearn.preprocessing import LabelEncoder

__all__ = ['ModelRetrainer']

class ModelRetrainer:
    def __init__(self, model_path='models/regime_model.pkl', checkpoint_path='models/checkpoints'):
        self.model_path = model_path
        self.checkpoint_path = checkpoint_path
        self.backtester = Backtester() # ✅ Inicialize Backtester aqui

        # Removendo a verificação de existencia do modelo do __init__ para focar no treinamento sob demanda
        print("🚀 Retrainer inicializado, pronto para treinar modelos sob demanda.")


    def get_training_data(self, symbol, start_date, end_date):
        """
        Recupera dados de treinamento do banco de dados dentro de um intervalo de datas.
        """
        df = get_historical_data_from_db(symbol, start_date=start_date, end_date=end_date) # Modificar db_manager para aceitar start_date, end_date
        if df.empty:
            print(f"⚠️ Sem dados disponíveis para {symbol} no período de {start_date} a {end_date}.")
            return None
        return df

    def prepare_batches(self, df, batch_method, qtd_pack_batch, qtd_unique_batch):
        """
        Prepara os batches de dados com base no método de batching configurado.
        """
        if df is None or df.empty:
            return []

        if batch_method == 1: # Unique Batch
            num_batches = len(df) // qtd_unique_batch
            batches = [df[i*qtd_unique_batch:(i+1)*qtd_unique_batch] for i in range(num_batches)]
        elif batch_method == 0: # Pack Batch
            num_batches = qtd_pack_batch
            batch_size = len(df) // num_batches if num_batches > 0 else 0
            batches = [df[i*batch_size:(i+1)*batch_size] for i in range(num_batches)]
        else:
            print("⚠️ Método de batch inválido. Retornando batches únicos.")
            return [df] # Retorna um batch único com todos os dados

        return batches

    def initial_train(self, model_type, symbol=crypto_list[0], start_date=Train_Date_Start, end_date=Train_Date_End):
        """
        Treina o modelo pela primeira vez, temporalmente e com batching configurável.

        Args:
            model_type (str): Tipo de modelo a ser treinado ('xgboost', 'lstm', 'patchtst', 'informer', 'ppo').
            symbol (str): Símbolo da criptomoeda para treinamento.
            start_date (str): Data inicial do período de treinamento.
            end_date (str): Data final do período de treinamento.
        """
        print(f"🚀 Iniciando treinamento inicial para {model_type.upper()}...")

        df = self.get_training_data(symbol, start_date, end_date)
        if df is None:
            print(f"⚠️ Dados insuficientes para treinamento inicial de {model_type.upper()}. Abortando.")
            return

        batches = self.prepare_batches(df.copy(), Batch_Method, QTD_Pack_Batch, QTD_Unique_Batch) # Passa uma cópia para evitar modificar o original

        if not batches:
            print(f"⚠️ Nenhum batch de dados preparado para treinamento de {model_type.upper()}. Abortando.")
            return

        for i, batch_df in enumerate(batches):
            print(f"📊 Treinando Batch {i+1}/{len(batches)} para {model_type.upper()}...")

            X = batch_df.drop(columns=["timestamp", "symbol", "regime"], errors="ignore") # Mantem 'regime' para XGBoost
            y = batch_df.get("regime", pd.Series(dtype='object'))

            # 🔄 Corrigir rótulos não numéricos e substituir valores inválidos (Aplica-se ao XGBoost regime model)
            if model_type == 'xgboost':
                y = y.fillna("unknown")
                unique_values = y.unique()
                if any(isinstance(val, str) for val in unique_values):
                    print(f"⚠️ Corrigindo rótulos inválidos: {unique_values}")
                    label_encoder = LabelEncoder()
                    y = label_encoder.fit_transform(y)
                else:
                    print("✅ Rótulos numéricos detectados para XGBoost. Label Encoding ignorado.")


            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            if model_type == 'xgboost':
                model = XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.04) # Parametros padrão para XGBoost
            elif model_type == 'lstm':
                model = LSTMModel(input_dim=X_train.shape[1], hidden_dim=64, num_layers=2, output_dim=1) # Adapta input_dim
            elif model_type == 'patchtst':
                model = PatchTST(input_dim=X_train.shape[1], embed_size=64, patch_size=4, heads=4, forward_expansion=4, num_layers=3) # Adapta input_dim
            elif model_type == 'informer':
                model = Informer(input_dim=X_train.shape[1], embed_size=64, heads=4, forward_expansion=4, num_layers=3) # Adapta input_dim
            elif model_type == 'ppo':
                model = PPOAgent(state_dim=X_train.shape[1], action_dim=3, hidden_dim=64) # Adapta state_dim
            else:
                print(f"⚠️ Tipo de modelo desconhecido: {model_type}. Abortando treinamento deste batch.")
                continue # Pula para o próximo batch se o tipo de modelo for inválido

            model.fit(X_train, y_train) # Ajustar fit para PPO se necessário (PPO geralmente usa update steps, não fit diretamente)

            checkpoint_path = os.path.join(self.checkpoint_path, f"{model_type}_checkpoint_batch_{i+1}.pkl") # Checkpoints batch a batch
            model_path = os.path.join(self.model_path, f"{model_type}_model_batch_{i+1}.pkl") # Salva modelo batch a batch por enquanto para debug
            save_checkpoint(model, checkpoint_path)
            joblib.dump(model, model_path)
            print(f"✅ Batch {i+1} para {model_type.upper()} treinado e salvo em {model_path}")

        print(f"✅ Treinamento inicial para {model_type.upper()} concluído em {len(batches)} batches.")


    def retrain(self, model_type, error_data): # Mantem error_data para re-treino baseado em erros futuros
        """Re-treina o modelo baseado nos erros do backtest."""
        # A ser implementado para re-treino fino com dados de erro e para os outros modelos (LSTM, PatchTST, Informer, PPO)
        print(f"🚧 Re-treino para {model_type.upper()} ainda não implementado.")
        pass


# ✅ 2. Função de Normalização de Colunas para a API Bybit (Manter, pode ser útil)
def normalize_bybit_columns(data_list):
    columns = ["timestamp", "open", "high", "low", "close", "volume", "extra"]
    df = pd.DataFrame(data_list, columns=columns)
    df = df.drop(columns=["extra"], errors="ignore")
    return df


# Para teste e inicialização (exemplo de uso):
if __name__ == '__main__':
    retrainer = ModelRetrainer()
    # Exemplo de treinamento inicial do modelo XGBoost (regime)
    retrainer.initial_train(model_type='xgboost') # Treina XGBoost
    # Exemplo de treinamento inicial do modelo LSTM
    retrainer.initial_train(model_type='lstm') # Treina LSTM
    # Exemplo de treinamento inicial do modelo PatchTST
    retrainer.initial_train(model_type='patchtst') # Treina PatchTST
    # Exemplo de treinamento inicial do modelo Informer
    retrainer.initial_train(model_type='informer') # Treina Informer
    # Exemplo de treinamento inicial do modelo PPO
    retrainer.initial_train(model_type='ppo') # Treina PPO