# trading_bot/utils/websocket_data.py
# Coleta de dados de mercado em tempo real via WebSocket

import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"📡 Preço atualizado: {data['data']['price']} USDT")

def start_websocket():
    """
    Inicia conexão WebSocket com a Bybit para obter preços em tempo real.
    """
    ws = websocket.WebSocketApp("wss://stream.bybit.com/v5/public/spot", on_message=on_message)
    ws.run_forever()