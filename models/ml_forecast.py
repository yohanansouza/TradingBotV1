# trading_bot/models/ml_forecast.py
# Módulo responsável pelo modelo de previsão baseado em XGBoost,
# utilizando treinamento incremental e ajustes com base em padrões operacionais.

import pickle
import os
import sqlite3
import pandas as pd
import xgboost as xgb
import time
from models.pattern_recognition import check_pattern_similarity, store_pattern
from models.ml_forecast_logs import create_training_version, save_training_log, update_general_log
from models.training_manager import train_and_save_model
from utils.symbol_manager import get_global_symbols
from config import MIN_DATA_REQUIRED, FAMILIAS_DE_GERACOES, GERACOES_POR_CRIPTO  # Importa configurações de treinamento

MODEL_PATH = "models/xgboost_model.pkl"
DB_PATH = "logs/trading_data.db"


# Inicializar Vet_Symbol com criptomoedas padrão
print("✅ Vetores de treinamento inicializados corretamente!")
#print("global_symbols:", global_symbols)

# Carregar modelo treinado ou criar um novo
def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as file:
            model = pickle.load(file)
        print("✅ Modelo carregado com sucesso!")
        return model
    else:
        print(f"❌ Modelo não encontrado: {MODEL_PATH}. Treinando um novo...")
        return train_and_save_model()

# Esperar até que a tabela de dados históricos tenha registros suficientes
def wait_for_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='historical_data'")
        table_exists = cursor.fetchone()[0]
        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM historical_data")
            data_count = cursor.fetchone()[0]
            if data_count >= MIN_DATA_REQUIRED:
                print(f"[SUCESSO] {data_count} registros encontrados na tabela historical_data. Continuando treinamento.")
                conn.close()
                return
        print(f"[AGUARDANDO] Aguardando pelo menos {MIN_DATA_REQUIRED} dados na tabela historical_data... (atualmente: {data_count} registros)")
        time.sleep(5)


 # Substituir Vet_Symbol por get_global_symbols()
def train_partial(symbol):
    global_symbols = get_global_symbols()  # Obtém symbols corretamente

    if not os.path.exists(MODEL_PATH):
        print("❌ Modelo não encontrado, treinando do zero...")
        return train_and_save_model()
    
    model = load_model()
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM historical_data WHERE symbol = '{symbol}' ORDER BY timestamp DESC LIMIT 1000"
    df = pd.read_sql(query, conn)
    conn.close()
    
    if df.empty:
        print(f"⚠️ Nenhum novo dado para treinamento incremental de {symbol}.")
        return model
    
    X = df[["open", "high", "low", "close", "volume"]].astype(float)
    y = (df["close"].shift(-1) > df["close"]).astype(int)
    y.fillna(0, inplace=True)
    
    model.fit(X, y, xgb_model=model)
    
    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)
    print(f"✅ Treinamento incremental realizado para {symbol}. Modelo atualizado!")
    
    return model

# Fazer previsão com o modelo
def predict(market_data):
    """
    Faz uma previsão usando o modelo treinado e retorna a direção da tendência e confiança.
    """
    model = load_model()
    
    df = pd.DataFrame([market_data])
    df = df.astype(float)
    
    prediction_proba = model.predict_proba(df)[0]
    confidence = max(prediction_proba) * 100
    prediction = model.predict(df)[0]
    
    store_pattern(market_data.get("symbol", "UNKNOWN"), market_data, "Long" if prediction == 1 else "Short")
    
    print(f"🔍 Previsão do modelo: {'Alta' if prediction == 1 else 'Baixa'} (Confiança: {confidence:.2f}%)")
    print(f"📈 Probabilidades detalhadas: Subida: {prediction_proba[1] * 100:.2f}%, Queda: {prediction_proba[0] * 100:.2f}%")
    
    return prediction, confidence
