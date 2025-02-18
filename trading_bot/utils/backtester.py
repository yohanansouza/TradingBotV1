# 🚀 Código Corrigido do `backtester.py`
# ==========================================

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

__all__ = ['Backtester']

# ✅ 1. Classe Backtester para Simulação de Estratégias
class Backtester:
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.equity_curve = []

    def run(self, data, strategy):
        self.equity_curve = [self.initial_balance]
        for index, row in data.iterrows():
            signal = strategy(row)
            if signal == 'buy':
                profit = (row['close'] - row['open']) * 0.01 * self.balance
                self.balance += profit
            self.equity_curve.append(self.balance)
        return np.array(self.equity_curve)

    def calculate_metrics(self, equity_curve):
        returns = np.diff(equity_curve) / equity_curve[:-1]
        sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-8)
        drawdown = np.max(np.maximum.accumulate(equity_curve) - equity_curve)
        return sharpe_ratio, drawdown

# ✅ 2. Execução de Teste
if __name__ == "__main__":
    sample_data = pd.DataFrame({
        'open': [100, 102, 101, 103, 104],
        'close': [102, 101, 103, 105, 102]
    })
    
    def sample_strategy(row):
        return 'buy' if row['close'] > row['open'] else 'hold'

    backtester = Backtester()
    equity = backtester.run(sample_data, sample_strategy)
    sharpe, drawdown = backtester.calculate_metrics(equity)
    print(f"📊 Sharpe Ratio: {sharpe:.2f}")
    print(f"📉 Máx Drawdown: {drawdown:.2f}")
