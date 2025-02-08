# trading_bot/backtesting/backtest.py
# Módulo de backtesting aprimorado para avaliação detalhada da estratégia

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_backtest():
    """
    Simula o desempenho da estratégia utilizando dados históricos, considerando taxas, funding e liquidação.
    """
    df = pd.read_csv("logs/trade_logs.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)
    df["cumulative_pnl"] = df["pnl"].cumsum()
    
    # Cálculo de métricas
    win_rate = (df["pnl"] > 0).sum() / len(df) * 100 if len(df) > 0 else 0
    drawdown = (df["cumulative_pnl"].cummax() - df["cumulative_pnl"]).max()
    sharpe_ratio = np.mean(df["pnl"]) / np.std(df["pnl"]) if np.std(df["pnl"]) != 0 else 0
    expectancia = np.mean(df["pnl"]) if len(df) > 0 else 0
    
    # Considerando taxas e funding rate
    df["fees"] = df["pnl"] * 0.0006  # Simulação da taker fee (0.06%)
    df["funding_cost"] = df["pnl"] * 0.0001  # Simulação da funding rate (0.01%)
    df["net_pnl"] = df["pnl"] - df["fees"] - df["funding_cost"]
    
    # Gráfico de Lucro Acumulado
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["cumulative_pnl"], label="Lucro Bruto", color="blue")
    plt.plot(df["timestamp"], df["net_pnl"].cumsum(), label="Lucro Líquido (após taxas)", color="green")
    plt.axhline(y=0, color="red", linestyle="dashed")
    plt.xlabel("Tempo")
    plt.ylabel("Lucro (USDT)")
    plt.title("Performance do Trading Bot (Backtesting)")
    plt.legend()
    plt.show()
    
    print(f"📊 Backtest Concluído: Win Rate: {win_rate:.2f}% | Drawdown Máximo: {drawdown:.2f} USDT | Sharpe Ratio: {sharpe_ratio:.2f} | Expectância: {expectancia:.2f} USDT")
    df.to_csv("logs/backtest_results.csv", index=False)

# Chamada principal para execução do backtest
if __name__ == "__main__":
    run_backtest()
