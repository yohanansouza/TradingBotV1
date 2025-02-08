# trading_bot/main.py
# Script principal que gerencia a execução do Trading Bot e a inicialização do Dashboard Flask

import threading
import time
import os
import webbrowser
from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
from models.ml_forecast import load_model, predict, train_partial
from data_manager import initialize_data_updates
from utils.bybit_api import get_top_movers_by_api
from utils.symbol_manager import update_symbols, get_global_symbols

# Configuração do servidor Flask
server = Flask(__name__)
DB_PATH = "logs/trading_data.db"

# Função para carregar dados do banco de dados SQLite3
def get_data_from_db(query, source):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        print(f"🔍 Consulta SQL executada na tabela {source}: {query}")
        print(f"📊 Registros retornados: {df.shape[0]} linhas")
        if not df.empty:
            print(df.head())
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados do banco: {e}")
        return pd.DataFrame()

# Rota principal do dashboard
@server.route('/')
def index():
    return render_template('index.html')

# Rota para obter dados de preços
@server.route('/data/<symbol>')
def get_price_data(symbol):
    query = f"SELECT timestamp, close, high, low, volume FROM historical_data WHERE symbol = '{symbol}' ORDER BY timestamp ASC"
    df = get_data_from_db(query, "historical_data")
    data = df.to_dict(orient='records')
    return jsonify({"data": data})

# Rota para obter tabela de dados
@server.route('/table/<symbol>')
def get_table_data(symbol):
    query = f"SELECT timestamp, close, high, low, volume FROM historical_data WHERE symbol = '{symbol}' ORDER BY timestamp DESC LIMIT 20"
    df = get_data_from_db(query, "historical_data")
    return jsonify({"data": df.to_dict(orient='records')})

# Inicializar o Trading Bot e o Dashboard em threads separadas
if __name__ == '__main__':
    print("🚀 Obtendo os ativos mais voláteis da Bybit...")
    top_gainers, top_losers = get_top_movers_by_api()

    print("🚀 Atualizando lista de symbols...")
    update_symbols(top_gainers, top_losers)

    print("✅ Symbols Atualizados:", get_global_symbols())
    
    print("🚀 Iniciando Threads para Data Manager e Treinamento de ML...")

    # Criar threads para execução paralela
    data_manager_thread = threading.Thread(target=initialize_data_updates, daemon=True)
    
    # Iniciar threads
    data_manager_thread.start()
    
    # Espera até que os dados tenham sido carregados antes de iniciar o treinamento
    print("🔄 Aguardando carregamento de dados antes de iniciar o treinamento...")
    time.sleep(30)  # Espera 30 segundos para garantir que os dados foram importados
    
print("🚀 Iniciando treinamento do modelo...")
global_symbols = get_global_symbols()  # Obtém a lista correta de symbols

for symbol in global_symbols:
    train_partial(symbol)  


    print("🚀 Trading Bot, Data Manager e ML Forecast rodando em paralelo!")
    
    while True:
        time.sleep(60)  # Intervalo de atualização
        print("🔄 Verificando atualizações do mercado...")
