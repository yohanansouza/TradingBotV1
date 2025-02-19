# 🚀 Código Corrigido do `bybit_api.py`
# ==========================================

import requests
import pandas as pd
import time
from trading_bot.config import BASE_URL, Train_Date_Start, Train_Date_End

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

# ✅ 2. Função Corrigida para Obter Todos os Dados Históricos do Período

def get_historical_data(symbol, interval="1", limit=1000, start_date=None, end_date=None):
    """
    Obtém dados históricos de um símbolo entre start_date e end_date.
    Se start_date/end_date não forem fornecidos, utiliza os parâmetros padrão de treinamento.
    """
    if start_date is None:
        start_date = Train_Date_Start
    if end_date is None:
        end_date = Train_Date_End

    start_timestamp = int(pd.Timestamp(start_date).timestamp() * 1000)
    end_timestamp = int(pd.Timestamp(end_date).timestamp() * 1000)
    
    url = f"{BASE_URL}/v5/market/kline"
    all_data = []
    
    while start_timestamp < end_timestamp:
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "start": start_timestamp
        }
        data = request_with_retries(url, params)
        
        if "result" not in data or "list" not in data["result"]:
            raise ValueError(f"Erro ao buscar dados históricos para {symbol}: {data}")
        
        df = pd.DataFrame(data["result"]["list"])
        expected_columns = ["timestamp", "open", "high", "low", "close", "volume"]
        df = df.iloc[:, :len(expected_columns)]
        df.columns = expected_columns
        
        df["timestamp"] = pd.to_numeric(df["timestamp"], errors='coerce') / 1000
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", errors='coerce')
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        
        all_data.append(df)
        
        if not df.empty:
            start_timestamp = int(df["timestamp"].max().timestamp() * 1000) + 1
        else:
            break
        
        time.sleep(0.5)
    
    final_df = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
    final_df = final_df[(final_df["timestamp"] >= pd.Timestamp(start_date)) & (final_df["timestamp"] <= pd.Timestamp(end_date))]
    return final_df

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
