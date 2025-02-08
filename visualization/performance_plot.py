# trading_bot/visualization/performance_plot.py
# Geração de gráficos para análise de performance

import pandas as pd
import matplotlib.pyplot as plt

def plot_performance():
    """
    Gera gráficos do desempenho acumulado dos trades.
    """
    df = pd.read_csv("logs/trade_logs.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["cumulative_pnl"] = df["pnl"].cumsum()
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["cumulative_pnl"], label="Lucro Acumulado", color="green")
    plt.axhline(y=0, color="red", linestyle="dashed")
    plt.xlabel("Tempo")
    plt.ylabel("Lucro (USDT)")
    plt.title("Performance do Trading Bot")
    plt.legend()
    plt.show()

# Chamada principal
if __name__ == "__main__":
    plot_performance()
