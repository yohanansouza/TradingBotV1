# 🚀 Código Completo do `indicators.py`
# ==========================================

import pandas as pd
import numpy as np

# ✅ 1. Cálculo do RSI (Relative Strength Index)
def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / (avg_loss + 1e-8)
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ✅ 2. Cálculo do MACD (Moving Average Convergence Divergence)
def compute_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    exp1 = prices.ewm(span=fast_period, adjust=False).mean()
    exp2 = prices.ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal

# ✅ 3. Cálculo das Bandas de Bollinger
def compute_bollinger_bands(prices, period=20, std_dev=2):
    sma = prices.rolling(window=period).mean()
    rolling_std = prices.rolling(window=period).std()
    upper_band = sma + (rolling_std * std_dev)
    lower_band = sma - (rolling_std * std_dev)
    return upper_band, sma, lower_band

# ✅ 4. Execução de Teste
if __name__ == "__main__":
    sample_prices = pd.Series([100, 102, 104, 103, 105, 107, 110, 108, 109, 111])
    
    rsi = compute_rsi(sample_prices)
    macd, signal = compute_macd(sample_prices)
    upper_band, mid_band, lower_band = compute_bollinger_bands(sample_prices)
    
    print("📊 RSI:\n", rsi)
    print("📈 MACD:\n", macd)
    print("💡 Sinal MACD:\n", signal)
    print("📊 Bandas de Bollinger:")
    print(f"Upper: {upper_band}\nMiddle: {mid_band}\nLower: {lower_band}")
