# trading_bot/execution/trade_execution.py
# Módulo responsável pela execução de ordens na Bybit, agora com gestão de capital integrada.

from utils.bybit_api import execute_order
from utils.logger import log_trade
from utils.capital_manager import adjust_leverage, manage_profit, check_risk_management

def execute_trade(symbol, prediction, balance):
    """
    Executa um trade baseado na previsão do modelo, ajustando alavancagem, verificando risco e gerenciando lucro.
    
    Parâmetros:
    - symbol (str): Par de negociação (ex: BTCUSDT).
    - prediction (int): 1 para Long, 0 para Short.
    - balance (float): Saldo atual do trader.

    Retorna:
    - dict: Dados da ordem executada.
    """

    # Ajustar alavancagem com base na confiança do modelo
    confidence = prediction.get("confidence", 50)  # Simulação de confiança caso não esteja disponível
    leverage = adjust_leverage(confidence)

    # Verificar gestão de risco antes de executar o trade
    if not check_risk_management(balance):
        print("🚨 Trade bloqueado por risco elevado!")
        return None

    # Definir ação e tamanho da posição
    size = 1 * leverage  # Define tamanho da posição proporcional à alavancagem
    action = "Long" if prediction == 1 else "Short"

    # Executar ordem na Bybit
    order = execute_order(symbol, "Buy" if prediction == 1 else "Sell", size, "Market")

    # Obter informações do trade
    pnl = order.get("pnl", 0)  # Lucro ou prejuízo da ordem
    executed_price = order.get("last_price", 0)  # Preço em que a ordem foi executada
    balance += pnl  # Atualiza saldo após o trade

    # Gerenciar lucro e reinvestir parte do saldo
    reinvest_amount = manage_profit({"pnl": pnl}, leverage)
    balance += reinvest_amount  # Atualiza saldo após reinvestimento

    # Registrar a operação no log
    log_trade(symbol, executed_price, action, pnl, confidence, leverage, balance)

    return order
