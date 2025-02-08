# trading_bot/utils/logger.py
# Sistema de logs para registrar cada operação de forma unificada

import csv
import os
from datetime import datetime

LOG_FILE = "logs/trade_logs.csv"

# Criar diretório de logs se não existir
if not os.path.exists("logs"):
    os.makedirs("logs")

# Criar cabeçalho do CSV se não existir
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "cripto", "preco", "acao", "pnl", "confianca", "alavancagem", "saldo apos trade"])

def log_trade(symbol, price, action, pnl, confidence, leverage, balance):
    """
    Registra os detalhes de cada trade no log padronizado.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = [timestamp, symbol, price, action, pnl, confidence, leverage, balance]
    
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(log_data)
    
    print(f"[LOG] {timestamp} | {symbol} | {action} | Preço: {price} USDT | P&L: {pnl} USDT | Confiança: {confidence}% | Alavancagem: {leverage}x | Saldo: {balance} USDT")
