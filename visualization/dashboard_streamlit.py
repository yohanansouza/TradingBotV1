# trading_bot/visualization/dashboard_streamlit.py
# Dashboard interativo para monitorar o desempenho do bot em tempo real usando Streamlit

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

DB_PATH = "logs/trading_data.db"

# Função para carregar dados do banco de dados SQLite3
def get_data_from_db(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados do banco: {e}")
        return pd.DataFrame()

# Configuração do Streamlit
st.set_page_config(page_title="Trading Bot Dashboard", layout="wide")
st.title("📊 Trading Bot Dashboard")

# Seleção de criptomoeda
crypto_list = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
selected_crypto = st.selectbox("Escolha a Criptomoeda:", crypto_list)

# Carregar dados de preços
query = f"SELECT timestamp, close FROM historical_data WHERE symbol = '{selected_crypto}' ORDER BY timestamp ASC"
df = get_data_from_db(query)

# Verificar se há dados
if df.empty:
    st.warning(f"⚠️ Nenhum dado encontrado para {selected_crypto}")
else:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    fig = px.line(df, x='timestamp', y='close', title=f"📈 Histórico de Preços para {selected_crypto}")
    st.plotly_chart(fig, use_container_width=True)

# Histórico de Trades
st.subheader("📑 Histórico de Trades")
query = f"SELECT timestamp, symbol, 'N/A' as action, close as price, 'N/A' as confidence FROM historical_data WHERE symbol = '{selected_crypto}' ORDER BY timestamp DESC LIMIT 20"
df_trades = get_data_from_db(query)

if df_trades.empty:
    st.warning(f"⚠️ Nenhum histórico de trades encontrado para {selected_crypto}")
else:
    st.dataframe(df_trades, height=400)
