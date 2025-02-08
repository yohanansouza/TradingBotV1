# trading_bot/models/pattern_recognition.py
# Módulo responsável por identificar padrões operacionais e comparar similaridades
# para otimizar o treinamento do modelo de trading.

import sqlite3
import pandas as pd

DB_PATH = "logs/training_patterns.db"

# Criar banco de dados se não existir
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trade_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            rsi REAL,
            macd REAL,
            bollinger REAL,
            price REAL,
            action TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Armazenar um novo padrão operacional
def store_pattern(symbol, indicators, action):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trade_patterns (symbol, rsi, macd, bollinger, price, action)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (symbol, indicators['rsi'], indicators['macd'], indicators['bollinger'], indicators['price'], action))
    conn.commit()
    conn.close()

# Comparar padrões para verificar a similaridade com os dados históricos
def check_pattern_similarity(symbol, new_pattern):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM trade_patterns WHERE symbol = '{symbol}'", conn)
    conn.close()
    
    if df.empty:
        return 0  # Nenhum padrão registrado ainda
    
    mean_rsi = df["rsi"].mean()
    mean_macd = df["macd"].mean()
    mean_bollinger = df["bollinger"].mean()
    
    similarity = (
        (1 - abs(mean_rsi - new_pattern['rsi']) / mean_rsi) * 100 +
        (1 - abs(mean_macd - new_pattern['macd']) / mean_macd) * 100 +
        (1 - abs(mean_bollinger - new_pattern['bollinger']) / mean_bollinger) * 100
    ) / 3  # Média da similaridade
    
    return similarity

# Inicializar banco de dados
initialize_database()
