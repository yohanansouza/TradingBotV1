# trading_bot/utils/db_manager.py
# Módulo para gerenciar o armazenamento e recuperação de dados no banco SQLite3, evitando duplicações

import sqlite3
import pandas as pd
import os

DB_DIR = "logs"
DB_PATH = os.path.join(DB_DIR, "trading_data.db")

# Criar banco de dados e tabelas se não existirem
def create_database():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)  # Garante que o diretório existe
    
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)  # Aumenta tempo de espera para evitar bloqueios
        cursor = conn.cursor()
        
        # Criar tabela de dados históricos com UNIQUE para evitar duplicações
        cursor.execute('''CREATE TABLE IF NOT EXISTS historical_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            symbol TEXT,
                            timestamp DATETIME,
                            open REAL,
                            high REAL,
                            low REAL,
                            close REAL,
                            volume REAL,
                            UNIQUE(symbol, timestamp))''')  # Impede duplicação
        
        # Criar tabela para armazenar preços em tempo real
        cursor.execute('''CREATE TABLE IF NOT EXISTS live_prices (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            symbol TEXT,
                            timestamp DATETIME,
                            last_price REAL,
                            high REAL,
                            low REAL,
                            volume REAL)''')
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados criado e pronto para uso.")
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")

# Função para armazenar dados históricos no SQLite, evitando duplicação
def store_historical_data(df, symbol):
    if df.empty:
        print(f"⚠️ Nenhum dado para armazenar em {symbol}")
        return
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO historical_data (symbol, timestamp, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (symbol, row['timestamp'].strftime("%Y-%m-%d %H:%M:%S"), row['open'], row['high'], row['low'], row['close'], row['volume']))
        
        conn.commit()
        conn.close()
        print(f"✅ Dados históricos armazenados para {symbol}, sem duplicação.")
    except Exception as e:
        print(f"❌ Erro ao salvar dados históricos no banco para {symbol}: {e}")

# Função para buscar dados históricos diretamente do banco para o treinamento
def get_training_data():
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        query = "SELECT open, high, low, close, volume FROM historical_data ORDER BY timestamp ASC"
        df = pd.read_sql(query, conn)
        conn.close()
        if df.empty:
            print("⚠️ Nenhum dado disponível no banco para treinamento.")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados de treinamento do banco: {e}")
        return pd.DataFrame()

# Testar conexão para verificar problemas de acesso ao banco
def test_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Testa conexão
        conn.close()
        print("✅ Conexão com o banco de dados testada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")

# Função para armazenar preços em tempo real no SQLite
def store_live_price(symbol, last_price, high, low, volume):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        cursor = conn.cursor()
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")  # Converter para string
        cursor.execute('''INSERT INTO live_prices (symbol, timestamp, last_price, high, low, volume)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (symbol, timestamp, last_price, high, low, volume))
        conn.commit()
        conn.close()
        print(f"📡 Dados em tempo real armazenados para {symbol}")
    except Exception as e:
        print(f"❌ Erro ao salvar preços em tempo real no banco de dados para {symbol}: {e}")

# Função para recuperar dados históricos do banco
def get_historical_data_from_db(symbol):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        query = f"SELECT * FROM historical_data WHERE symbol = '{symbol}'"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Erro ao recuperar dados históricos do banco para {symbol}: {e}")
        return pd.DataFrame()

# Função para recuperar preços em tempo real do banco
def get_live_prices_from_db(symbol):
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        query = f"SELECT * FROM live_prices WHERE symbol = '{symbol}' ORDER BY timestamp DESC LIMIT 1"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Erro ao recuperar preços em tempo real do banco para {symbol}: {e}")
        return pd.DataFrame()

# Inicializar banco de dados na primeira execução
test_db_connection()
create_database()
