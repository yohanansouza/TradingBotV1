# trading_bot/visualization/dashboard.py
# Dashboard interativo para monitorar o desempenho do bot em tempo real com dados do SQLite3

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
import webbrowser
import threading
from flask import Flask

DB_PATH = "logs/trading_data.db"

# Criar servidor Flask para rodar o Dash
server = Flask(__name__)
dashboard_app = dash.Dash(__name__, server=server)

# Função para carregar dados do banco de dados SQLite3
def get_data_from_db(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        print(f"🔍 Consulta SQL executada: {query}")
        print(f"📊 Dados retornados: {df.shape[0]} linhas")
        print(df.head())  # Mostrar as primeiras linhas para depuração
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados do banco: {e}")
        return pd.DataFrame()

# Layout do Dashboard
dashboard_app.layout = html.Div([
    html.H1("📊 Trading Bot Dashboard"),
    
    # Atualização automática
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0),
    
    # Seleção de criptomoeda
    html.Label("Escolha a Criptomoeda:"),
    dcc.Dropdown(
        id='crypto-selector',
        options=[{'label': symbol, 'value': symbol} for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]],
        value='BTCUSDT'
    ),
    
    # Gráfico de preços - Dados do Banco
    dcc.Graph(id='crypto-price-chart'),
    
    # Histórico de Trades
    html.H2("📑 Histórico de Trades"),
    dash_table.DataTable(
        id='trade-history-table',
        columns=[
            {"name": "Timestamp", "id": "timestamp"},
            {"name": "Cripto", "id": "symbol"},
            {"name": "Ação", "id": "action"},
            {"name": "Preço", "id": "price"},
            {"name": "Confiança", "id": "confidence"}
        ],
        style_table={'overflowX': 'auto'}
    )
])

# Atualização do gráfico de preços
@dashboard_app.callback(
    Output('crypto-price-chart', 'figure'),
    Input('crypto-selector', 'value')
)
def update_crypto_chart(selected_crypto):
    try:
        query = f"SELECT timestamp, close FROM historical_data WHERE symbol = '{selected_crypto}' ORDER BY timestamp ASC"
        df = get_data_from_db(query)
        
        # Verificar se há dados
        if df.empty:
            print(f"⚠️ Nenhum dado encontrado para {selected_crypto}")
            return {
                'data': [],
                'layout': {'title': f"📈 Histórico de Preços para {selected_crypto} (sem dados)"}
            }
        
        # Converter timestamp para datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        print(f"📅 Timestamps convertidos corretamente para {selected_crypto}")
        
        fig = {
            'data': [
                {'x': df['timestamp'], 'y': df['close'], 'type': 'line', 'name': selected_crypto},
            ],
            'layout': {
                'title': f"📈 Histórico de Preços para {selected_crypto}"
            }
        }
        return fig
    except Exception as e:
        print(f"Erro ao atualizar o gráfico de preços: {e}")
        return {}

# Atualização do histórico de trades
@dashboard_app.callback(
    Output('trade-history-table', 'data'),
    Input('crypto-selector', 'value')
)
def update_trade_history(selected_crypto):
    try:
        query = f"SELECT timestamp, symbol, 'N/A' as action, close as price, 'N/A' as confidence FROM historical_data WHERE symbol = '{selected_crypto}' ORDER BY timestamp DESC LIMIT 20"
        df = get_data_from_db(query)
        
        # Verificar se há dados
        if df.empty:
            print(f"⚠️ Nenhum histórico de trades encontrado para {selected_crypto}")
            return []
        
        return df.to_dict("records")
    except Exception as e:
        print(f"Erro ao atualizar o histórico de trades: {e}")
        return []

# Abrir automaticamente o Dashboard
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050")

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    dashboard_app.run_server(debug=True, use_reloader=False)
