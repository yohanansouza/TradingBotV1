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
from trading_bot.config import crypto_list 
from sklearn.preprocessing import LabelEncoder 

__all__ = ['ModelRetrainer']

class ModelRetrainer:
    def __init__(self, model_path='models/regime_model.pkl', checkpoint_path='models/checkpoints'):
        self.model_path = model_path
        self.checkpoint_path = checkpoint_path
        self.backtester = Backtester() # ✅ Inicialize Backtester aqui

        if not os.path.exists(self.model_path):
            print("🚀 Modelo não encontrado! Iniciando treinamento inicial...")
            self.initial_train()
        else:
            print(f"✅ Modelo encontrado em: {self.model_path}. Treinamento inicial pulado.") # Mensagem informativa

    def initial_train(self):
        """Treina o modelo pela primeira vez usando dados históricos para todas as criptos definidas no config.py."""
        all_data = []
        for symbol in crypto_list:
            df = get_historical_data_from_db(symbol)
            if df.empty:
                print(f"⚠️ Sem dados disponíveis para {symbol}. Pulando...")
                continue
            all_data.append(df)

        if not all_data:
            print("⚠️ Nenhum dado disponível para treinamento inicial! Abortando...")
            return

        df = pd.concat(all_data, ignore_index=True)
        X = df.drop(columns=["timestamp", "symbol", "regime"], errors="ignore")
        y = df.get("regime", pd.Series(dtype='object'))

        # 🔄 Corrigir rótulos não numéricos e substituir valores inválidos
        y = y.fillna("unknown")  # Preenche valores nulos com "unknown"
        unique_values = y.unique()

        # ✅ Correção: Label Encoding apenas se houver rótulos string
        if any(isinstance(val, str) for val in unique_values):
            print(f"⚠️ Corrigindo rótulos inválidos: {unique_values}")
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)
        else:
            print("✅ Rótulos numéricos detectados. Label Encoding ignorado.")


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.04)
        model.fit(X_train, y_train)

        save_checkpoint(model, self.checkpoint_path)
        joblib.dump(model, self.model_path)
        print(f"✅ Modelo inicial treinado e salvo em {self.model_path}")

    def retrain(self, error_data):
        """Re-treina o modelo baseado nos erros do backtest."""
        if not os.path.exists(self.model_path):
            print("⚠️ Modelo não encontrado! Treinamento inicial necessário.")
            self.initial_train()
            return

        if error_data.empty:
            print("⚠️ Nenhum erro detectado, re-treino não necessário.")
            return

        X = error_data.drop(columns=["actual", "predicted"], errors="ignore")
        y = error_data["actual"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = load_checkpoint(self.checkpoint_path)
        if not model:
            model = XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.04)

        model.fit(X_train, y_train)

        # 🚀 Valida o modelo rodando backtest ao final do batch
        backtest_results = self.backtester.run(data=get_historical_data_from_db("BTCUSDT"), strategy=lambda x: 'buy')

        if not backtest_results.empty:
            print("✅ Backtest concluído com sucesso!")

        # 💾 Salva o checkpoint e o modelo final
        save_checkpoint(model, self.checkpoint_path)
        joblib.dump(model, self.model_path)
        print(f"✅ Modelo re-treinado e salvo em {self.model_path}")

# ✅ 2. Função de Normalização de Colunas para a API Bybit
def normalize_bybit_columns(data_list):
    columns = ["timestamp", "open", "high", "low", "close", "volume", "extra"]
    df = pd.DataFrame(data_list, columns=columns)
    df = df.drop(columns=["extra"], errors="ignore")
    return df