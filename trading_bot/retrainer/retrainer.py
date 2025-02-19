# 📂 Módulo: `retrainer.py`
# 🚀 Correção do Erro: "PermissionError: Sem permissão para acessar logs/trading_data.db"
# ===================================================================================================

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from trading_bot.db.db_manager import create_database  # 🔹 Importação Correta

__all__ = ['ModelRetrainer']

# ✅ 1. Função para Criar e Garantir Permissão do Banco de Dados
def ensure_db_path(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if not os.path.exists(db_path):
        print(f"⚠️ Banco de dados {db_path} não encontrado. Criando...")
        create_database()
    try:
        os.chmod(db_path, 0o666)
        print(f"✅ Permissões ajustadas para: {db_path}")
    except Exception as e:
        raise PermissionError(f"🚨 Erro ao ajustar permissões: {e}")

# ✅ 2. Classe ModelRetrainer com Caminho Corrigido para Banco de Dados
class ModelRetrainer:
    def __init__(self, model_path='models/regime_model.pkl', db_path='models/trading_data.db'):
        self.model_path = model_path
        self.db_path = db_path
        ensure_db_path(self.db_path)

    def retrain(self, error_data):
        if error_data.empty:
            print("⚠️ Nenhum dado de erro disponível para re-treino. Pulando processo.")
            return
        
        X = error_data.drop(columns=['actual', 'predicted'], errors='ignore')
        y = error_data.get('actual', pd.Series())
        
        if X.empty or y.empty:
            print("⚠️ Dados insuficientes para re-treino. Pulando...")
            return
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        if X_train.empty or y_train.empty:
            print("⚠️ Train set vazio, ajustando split...")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.1, random_state=42
            )
        
        model = XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.04)
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        print("📊 Relatório Pós-Re-Treino:")
        print(classification_report(y_test, predictions))
        
        joblib.dump(model, self.model_path)
        print(f"💾 Modelo re-treinado salvo em {self.model_path}")


# ✅ 2. Função de Normalização de Colunas para a API Bybit
def normalize_bybit_columns(data_list):
    columns = ["timestamp", "open", "high", "low", "close", "volume", "extra"]
    df = pd.DataFrame(data_list, columns=columns)
    df = df.drop(columns=["extra"], errors="ignore")
    return df