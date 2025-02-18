# 🚀 Código Corrigido do `bybit_api.py`
# ==========================================

import requests
import pandas as pd
import time
from trading_bot.config import BASE_URL

__all__ = ['get_historical_data', 'get_top_movers', 'test_connection']

# ✅ 1. Função de Requisição com Repetições (Retries)
def request_with_retries(url, params, retries=5, delay=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"⚠️ Erro na conexão (tentativa {attempt+1}): {e}")
        time.sleep(delay * (2 ** attempt))
    raise ValueError("🚫 Falha após múltiplas tentativas")

# ✅ 2. Obter Dados Históricos
def get_historical_data(symbol, interval="1", start_date=None, end_date=None):
    start_ts = int(pd.Timestamp(start_date).timestamp() * 1000)
    end_ts = int(pd.Timestamp(end_date).timestamp() * 1000)
    
    url = f"{BASE_URL}/v5/market/kline"
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "start": start_ts,
        "end": end_ts,
        "limit": 1000
    }
    
    data = request_with_retries(url, params)
    df = pd.DataFrame(data["result"]["list"], columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms")
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
    return df

# ✅ 3. Obter Top Movers (Maiores Altas e Quedas)
def get_top_movers_by_api(interval="5m"):
    url = f"{BASE_URL}/v5/market/tickers"
    params = {"category": "linear"}
    
    data = request_with_retries(url, params)
    df = pd.DataFrame(data["result"]["list"])
    df = df[df["symbol"].str.endswith("USDT")]
    df["percent_change"] = ((df["lastPrice"].astype(float) - df["prevPrice24h"].astype(float)) / df["prevPrice24h"].astype(float)) * 100
    
    top_gainers = df.nlargest(10, "percent_change")["symbol"].tolist()
    top_losers = df.nsmallest(10, "percent_change")["symbol"].tolist()
    
    return top_gainers, top_losers

# ✅ 4. Teste de Conexão
def test_connection():
    try:
        url = f"{BASE_URL}/v5/market/tickers"
        params = {"category": "linear"}
        request_with_retries(url, params)
        print("✅ Conexão com a API da Bybit bem-sucedida")
    except Exception as e:
        print(f"🚫 Erro ao conectar com a API da Bybit: {e}")

# ✅ 5. Execução de Teste
if __name__ == "__main__":
    test_connection()
    df = get_historical_data("BTCUSDT", start_date="2024-01-01", end_date="2024-01-02")
    print(df.head())
    gainers, losers = get_top_movers_by_api()
    print(f"🚀 Top Gainers: {gainers}")
    print(f"📉 Top Losers: {losers}")
