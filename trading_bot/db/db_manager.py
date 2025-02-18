# 🚀 Código Completo do `db_manager.py`
# ======================================

import sqlite3
import os
import pandas as pd

DB_DIR = "models"
DB_PATH = os.path.join(DB_DIR, "trading_data.db")

# ✅ 1. Criação do Banco de Dados
def create_database():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                timestamp DATETIME,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                rsi REAL,
                macd REAL,
                macd_signal REAL,
                upper_band REAL,
                mid_band REAL,
                lower_band REAL,
                regime TEXT,
                UNIQUE(symbol, timestamp)
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Banco de dados criado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar banco: {e}")

# ✅ 2. Armazenamento de Dados Históricos
def store_historical_data(df, symbol):
    if df.empty:
        print(f"⚠️ Nenhum dado para {symbol}.")
        return
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO historical_data 
                (symbol, timestamp, open, high, low, close, volume, rsi, macd, macd_signal, upper_band, mid_band, lower_band, regime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                row['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                row['open'], row['high'], row['low'],
                row['close'], row['volume'],
                row.get('rsi', 0), row.get('macd', 0),
                row.get('macd_signal', 0),
                row.get('upper_band', 0),
                row.get('mid_band', 0),
                row.get('lower_band', 0),
                row.get('regime', 'unknown')
            ))
        conn.commit()
        conn.close()
        print(f"✅ Dados armazenados para {symbol}.")
    except Exception as e:
        print(f"❌ Erro ao armazenar dados para {symbol}: {e}")

# ✅ 3. Consulta de Intervalo Existente
def get_existing_date_range(symbol):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM historical_data WHERE symbol = ?", (symbol,))
        result = cursor.fetchone()
        conn.close()
        return result  # (min_date, max_date)
    except Exception as e:
        print(f"❌ Erro ao consultar intervalo: {e}")
        return None

# ✅ 4. Recuperação de Dados Históricos
def get_historical_data_from_db(symbol):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        query = f"SELECT * FROM historical_data WHERE symbol = '{symbol}'"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Erro ao recuperar dados: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    create_database()
