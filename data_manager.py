# trading_bot/data_manager.py
# Módulo responsável por gerenciar a atualização de dados e execução do Paper Trading
import sqlite3
import threading
import pandas as pd
import time
import os
from config import MIN_DATA_REQUIRED, crypto_list
from typing import List
from utils.bybit_api import get_historical_data
from utils.symbol_manager import get_global_symbols
from utils.db_manager import store_live_price, store_historical_data, get_historical_data_from_db

DB_PATH = "logs/trading_data.db"

# Importar dados históricos iniciais para o banco de dados
def import_initial_historical_data():
    symbols = get_global_symbols()  # Obtém symbols diretamente do Symbol Manager
    for symbol in symbols:
        try:
            print(f"🔄 Importando dados iniciais para {symbol}...")
            historical_data = get_historical_data(symbol, interval="1", limit=5000)  # Buscar 5000 registros iniciais
            store_historical_data(historical_data, symbol)
            print(f"✅ Dados iniciais armazenados para {symbol}")
        except Exception as e:
            print(f"❌ Erro ao importar dados iniciais para {symbol}: {e}")

# Atualizar dados históricos continuamente
def update_historical_data():
    while True:
        time.sleep(60)  # Atualizar a cada 1 minuto
        symbols = get_global_symbols()
        for symbol in symbols:
            try:
                print(f"🔄 Atualizando dados históricos para {symbol}...")
                historical_data = get_historical_data(symbol, interval="1", limit=2)  # Buscar apenas os últimos 2 registros mais recentes
                
                # Remover duplicatas antes de armazenar
                existing_data = get_historical_data_from_db(symbol)
                historical_data = historical_data[~historical_data["timestamp"].isin(existing_data["timestamp")]
                
                if not historical_data.empty:
                    store_historical_data(historical_data, symbol)
                    print(f"✅ Dados históricos atualizados para {symbol}")
                else:
                    print(f"⚠️ Nenhum novo dado para {symbol}, evitando duplicação.")
            except Exception as e:
                print(f"❌ Erro ao atualizar dados históricos para {symbol}: {e}")

# Atualização contínua dos preços e dados históricos
def update_prices_continuous():
    while True:
        time.sleep(15)
        symbols = get_global_symbols()
        for symbol in symbols:
            try:
                market_data = get_crypto_data(symbol)
                store_live_price(symbol, market_data["last_price"], market_data["high"], market_data["low"], market_data["volume"])
                print(f"📡 Dados em tempo real armazenados para {symbol}")
            except Exception as e:
                print(f"Erro ao atualizar preços para {symbol}: {e}")

# Inicializar atualização de dados e Paper Trading
def initialize_data_updates():
    import_initial_historical_data()  # Executar apenas uma vez no início
    threading.Thread(target=update_historical_data, daemon=True).start()
    threading.Thread(target=update_prices_continuous, daemon=True).start()

# Função principal para ser chamada pelo main.py
def data_manager_main():
    print("[INFO] Iniciando Data Manager...")
    print("🔄 Importando dados históricos iniciais...")
    import_initial_historical_data()
    print("✅ Dados iniciais importados!")
    print("[INFO] Iniciando threads de atualização contínua...")
    threading.Thread(target=update_historical_data, daemon=True).start()
    threading.Thread(target=update_prices_continuous, daemon=True).start()
    print("✅ Data Manager rodando!")
