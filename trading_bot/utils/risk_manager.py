# 🚀 Código Corrigido do `risk_manager.py`
# ==========================================

import numpy as np

__all__ = ['RiskManager']

# ✅ 1. Classe para Gerenciamento de Risco
class RiskManager:
    def __init__(self, risk_per_trade=0.01, max_drawdown=0.2):
        self.risk_per_trade = risk_per_trade
        self.max_drawdown = max_drawdown

    def calculate_risk_parameters(self, balance, volatility):
        position_size = balance * self.risk_per_trade
        stop_loss = position_size * self.max_drawdown
        risk_adjusted_leverage = min(5, 1 / (volatility + 1e-8))
        return position_size, stop_loss, risk_adjusted_leverage

    def check_drawdown(self, equity_curve):
        peak = np.maximum.accumulate(equity_curve)
        drawdown = (peak - equity_curve) / peak
        max_dd = np.max(drawdown)
        return max_dd, max_dd > self.max_drawdown

    def adjust_risk(self, current_balance, equity_curve, volatility):
        max_dd, is_excessive = self.check_drawdown(equity_curve)
        if is_excessive:
            print(f"⚠️ Alto drawdown detectado: {max_dd:.2%}. Reduzindo risco.")
            return self.calculate_risk_parameters(current_balance, volatility * 1.5)
        return self.calculate_risk_parameters(current_balance, volatility)

# ✅ 2. Execução de Teste
if __name__ == "__main__":
    manager = RiskManager()
    sample_balance = 10000
    sample_volatility = 0.03
    sample_equity_curve = np.array([10000, 9800, 9500, 9400, 9200])

    position_size, stop_loss, leverage = manager.adjust_risk(sample_balance, sample_equity_curve, sample_volatility)
    print(f"💰 Posição: ${position_size:.2f}, Stop Loss: ${stop_loss:.2f}, Alavancagem: {leverage:.2f}x")
