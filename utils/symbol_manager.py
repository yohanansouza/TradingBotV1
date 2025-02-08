# trading_bot/utils/symbol_manager.py
# Módulo centralizado para gerenciar os symbols mais voláteis e ordenar treinamento

from config import crypto_list
import time

# Vetores organizadores
_global_symbols = []  # Lista principal de symbols a serem operados

def update_symbols(top_gainers=None, top_losers=None):
    """
    Atualiza a lista de symbols com base na volatilidade e na ordem do treinamento.
    """
    global _global_symbols

    # Se nenhum dado for passado, mantém a lista anterior
    if top_gainers is None:
        top_gainers = []
    if top_losers is None:
        top_losers = []

    # Atualiza lista global
    _global_symbols = crypto_list.copy()

    while top_gainers or top_losers:
        if top_gainers:
            _global_symbols.append(top_gainers.pop(0))
        if top_losers:
            _global_symbols.append(top_losers.pop(0))

    print("🔄 Lista de Symbols Atualizada!", _global_symbols)

    return _global_symbols

def get_global_symbols():
    """
    Retorna a lista global de symbols.
    """
    return _global_symbols
