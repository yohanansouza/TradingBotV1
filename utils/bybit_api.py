# trading_bot/utils/bybit_api.py
# Módulo para conexão com a API da Bybit e obtenção de dados de mercado

import requests
import time
import pandas as pd
from config import BASE_URL
#from utils.symbol_manager import get_global_symbols

def request_with_retries(url, params, method="GET", retries=5, delay=3):
    """
    Faz uma requisição HTTP com tentativas automáticas em caso de erro.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10) if method == "GET" else requests.post(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"⚠️ Erro de conexão com a API da Bybit: {e}. Tentativa {attempt + 1}/{retries}...")
        time.sleep(delay * (2 ** attempt))  # Retry progressivo (3s, 6s, 12s...)

    raise ValueError("❌ Falha na conexão com a API da Bybit após múltiplas tentativas.")


def get_top_movers_by_api(interval="1h"):
    """
    Obtém os 10 ativos com maior valorização e os 10 ativos com maior desvalorização na Bybit.
    """
    url = f"{BASE_URL}/v5/market/tickers"
    params = {"category": "linear"}  # Obtém todos os contratos Perpetual
    data = request_with_retries(url, params)

    if "result" not in data or "list" not in data["result"]:
        raise ValueError(f"Erro ao buscar os ativos mais voláteis: {data}")

    df = pd.DataFrame(data["result"]["list"])
    df = df[df["symbol"].str.endswith("USDT")]  # Filtra apenas pares USDT Perpetual

    df["percent_change"] = ((df["lastPrice"].astype(float) - df["prevPrice24h"].astype(float)) / df["prevPrice24h"].astype(float)) * 100
    df = df.sort_values(by="percent_change", ascending=False)

    top_gainers = df.head(10)["symbol"].tolist()  # Top 10 maiores altas
    top_losers = df.tail(10)["symbol"].tolist()  # Top 10 maiores quedas

    return top_gainers, top_losers


def get_historical_data(interval="60", limit=500):
    """
    Obtém dados históricos para os symbols definidos no global_symbols do symbol_manager.
    """
    results = {}
    global_symbols = get_global_symbols()  # Obtém os symbols dinamicamente

    for symbol in global_symbols:
        url = f"{BASE_URL}/v5/market/kline"
        params = {"category": "linear", "symbol": symbol, "interval": interval, "limit": limit}
        data = request_with_retries(url, params)

        if "result" not in data or "list" not in data["result"]:
            print(f"⚠️ Erro ao buscar dados para {symbol}: {data}")
            continue

        df = pd.DataFrame(data["result"]["list"], columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors='coerce') / 1000
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", errors='coerce')
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

        results[symbol] = df

    return results