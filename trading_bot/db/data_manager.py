# 🚀 Código Completo do `data_manager.py`
# =========================================

import os
import pandas as pd
import time
from trading_bot.config import (crypto_list, Train_Date_Start, Train_Date_End,
                                Test_Date_Start, Test_Date_End, Enable_Vet_Symbol, crypto_list_test)
from trading_bot.utils.bybit_api import get_historical_data, get_top_movers_by_api, test_connection
from trading_bot.db.db_manager import create_database, store_historical_data, get_existing_date_range, ensure_db_ready
from trading_bot.utils.indicators import compute_rsi, compute_macd, compute_bollinger_bands

DB_PATH = os.path.join("models", "trading_data.db")

# ✅ 1. Inicialização do Banco de Dados
def initialize_database():
    if not os.path.exists(DB_PATH):
        print("Banco de dados não encontrado. Criando novo banco...")
        create_database()
    else:
        print("Banco de dados existente.")

# ✅ 2. Processamento de Dados com Indicadores
def process_and_store(symbol, df):
    df['rsi'] = compute_rsi(df['close'])
    macd, macd_signal = compute_macd(df['close'])
    df['macd'] = macd
    df['macd_signal'] = macd_signal
    upper_band, mid_band, lower_band = compute_bollinger_bands(df['close'])
    df['upper_band'], df['mid_band'], df['lower_band'] = upper_band, mid_band, lower_band
    df.fillna(0, inplace=True)
    store_historical_data(df, symbol)

# ✅ 1. Garante que o Banco de Dados está Criado Antes da Importação
def import_data_for_symbol(symbol, start_date, end_date):
    ensure_db_ready()  # Garante que o banco de dados e a tabela existem
    print(f"Importando dados para {symbol} de {start_date} até {end_date}...")
    date_range = get_existing_date_range(symbol)
    fetch_start = start_date
    if date_range and date_range[0]:
        existing_start, existing_end = date_range
        # Se os dados existentes já cobrem o período completo, nada é feito.
        if pd.to_datetime(existing_start) <= pd.to_datetime(start_date) and pd.to_datetime(existing_end) >= pd.to_datetime(end_date):
            print(f"Dados para {symbol} já completos no DB.")
            return
        # Se faltar dados após o final existente, inicia do dia seguinte ao último registro.
        fetch_start = (pd.to_datetime(existing_end) + pd.Timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        df = get_historical_data(symbol, interval="1", start_date=fetch_start, end_date=end_date)
        if df.empty:
            print(f"⚠️ Nenhum dado retornado para {symbol}.")
            return
        process_and_store(symbol, df)
        print(f"✅ Dados para {symbol} importados com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao importar dados para {symbol}: {e}")

# ✅ 2. Importação de Treinamento (Baixa Todos os Dados Definidos no `config.py`)
def import_training_data():
    for symbol in crypto_list:
        import_data_for_symbol(symbol, Train_Date_Start, Train_Date_End)

# ✅ 3. Importação de Teste (Baixa Todos os Dados Definidos no `config.py`)
def import_testing_data():
    for symbol in crypto_list_test:
        import_data_for_symbol(symbol, Test_Date_Start, Test_Date_End)      

# ✅ 6. Atualização de Symbols Dinâmicos
def update_dynamic_symbols():
    if Enable_Vet_Symbol:
        try:
            gainers, losers = get_top_movers_by_api(interval="5m")
            return gainers + losers
        except Exception as e:
            print(f"Erro ao atualizar symbols dinâmicos: {e}")
            return crypto_list
    return crypto_list

# ✅ 7. Pipeline Principal
def data_manager_main():
    print("🚀 Iniciando Data Manager...")
    initialize_database()
    symbols = update_dynamic_symbols()
    print("⬇️ Importando dados de treinamento...")
    for symbol in symbols:
        import_data_for_symbol(symbol, Train_Date_Start, Train_Date_End)
    print("⬇️ Importando dados de backtest...")
    for symbol in crypto_list_test:
        import_data_for_symbol(symbol, Test_Date_Start, Test_Date_End)
    print("✅ Data Manager concluído.")

# ✅ 4. Execução Principal
if __name__ == "__main__":
    ensure_db_ready()
    import_training_data()
    import_testing_data()