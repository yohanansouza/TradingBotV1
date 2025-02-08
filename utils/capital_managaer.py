# trading_bot/utils/capital_manager.py
# Módulo responsável pela gestão de capital, incluindo alavancagem dinâmica, gestão de lucros e controle de risco.

def adjust_leverage(prediction_confidence):
    """
    Ajusta a alavancagem automaticamente com base na confiança da previsão.
    """
    if prediction_confidence > 95:
        leverage = 80
    elif 85 < prediction_confidence <= 95:
        leverage = 50
    elif 75 < prediction_confidence <= 85:
        leverage = 30
    else:
        leverage = 20
    
    print(f"📈 Confiança: {prediction_confidence:.2f}% | Alavancagem ajustada para: {leverage}x")
    return leverage

def manage_profit(trade_result, leverage):
    """
    Separa 5% do lucro para saque e reinveste o restante, considerando a alavancagem.
    """
    profit = trade_result.get("pnl", 0)
    if profit > 0:
        withdraw_amount = profit * 0.05  # 5% para saque
        reinvest_amount = (profit - withdraw_amount) * (leverage / 20)  # Ajuste com base na alavancagem mínima de 20x
        print(f"💰 Lucro: {profit:.2f} USDT | Saque: {withdraw_amount:.2f} USDT | Reinvestindo: {reinvest_amount:.2f} USDT")
    else:
        reinvest_amount = 0
    return reinvest_amount

def check_risk_management(balance, max_loss=-500, max_gain=1000):
    """
    Verifica se o risco do trade está dentro dos limites aceitáveis.
    Se o saldo atingir o limite de perda ou atingir a meta diária de lucro, bloqueia novas operações.
    """
    if balance <= max_loss:
        print(f"🚨 STOP! Perda diária atingida: {balance} USDT. Interrompendo operações.")
        return False
    if balance >= max_gain:
        print(f"✅ Meta diária atingida: {balance} USDT. Parando operações para garantir lucro.")
        return False
    return True
