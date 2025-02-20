# 📂 Módulo: `backtester.py`
# ===================================================================================================

import pandas as pd
import numpy as np
from trading_bot.utils.risk_manager import RiskManager
from trading_bot.config import initial_balance, slippage, commission_rate

from rich.console import Console  # Import for Rich output in example
from rich.table import Table      # Import for Rich output in example

__all__ = ['Backtester']


class Backtester:
    def __init__(self, initial_balance=initial_balance, slippage=slippage, commission_rate=commission_rate):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.equity_curve = [initial_balance]  # Equity curve starts with initial balance
        self.slippage = slippage
        self.commission_rate = commission_rate
        self.trades = []  # Store trades for detailed analysis
        self.risk_manager = RiskManager()  # Risk Manager instance

    def run(self, data, strategy):
        """
        Executa o backtest da estratégia fornecida.

        Args:
            data (pd.DataFrame): Dados históricos para o backtest.
            strategy (function): Função que implementa a estratégia de trading.
                                 Deve receber uma linha do DataFrame e retornar um sinal de negociação
                                 ('buy', 'sell', 'hold' ou None).
        Returns:
            tuple: Uma tupla contendo:
                - pd.DataFrame: DataFrame contendo a curva de equity e os sinais de negociação.
                - list: Lista de dicionários com dados estruturados dos trades para Rich output.
        """
        if data.empty:
            print("⚠️ Alerta: DataFrame de dados vazio recebido pelo Backtester.")
            return pd.DataFrame({'equity_curve': []}), []  # Retorna DataFrame e lista vazios

        equity_curve = []
        predicted_signals = []  # Store predicted signals
        actual_signals = []     # Store actual signals (para agora, igual ao predicted para simplicidade)
        trades_rich_data = []  # Lista para armazenar dados de trades para output Rich

        for index, row in data.iterrows():
            #print(f"Type of row.name (index) inside backtester.run: {type(row.name)}")  # Debug print
            signal = strategy(row)  # Obtém sinal da estratégia (sinal predito)

            # Por agora, vamos assumir que o sinal 'actual' é o mesmo que o 'predicted' para teste.
            # Num cenário real, 'actual' seria determinado por algum benchmark ou resultado ideal.
            actual_signal = signal

            if signal == 'buy':
                self.execute_trade('buy', row['close'])
            elif signal == 'sell':
                self.execute_trade('sell', row['close'])
            # sinal 'hold' não aciona trade

            equity_curve.append(self.current_balance)
            predicted_signals.append(signal)
            actual_signals.append(actual_signal)

            trades_data = {  # Prepara dados para cada linha, para ser usado pela tabela Rich depois
                'timestamp': row.name,  # Usa o index (timestamp) - No isoformat() here for now
                'signal': signal,
                'price': row['close'],
                'balance': self.current_balance
            }
            trades_rich_data.append(trades_data)  # Armazena dados para output Rich

        results_df = pd.DataFrame({
            'equity_curve': equity_curve,
            'predicted': predicted_signals,  # Adiciona sinais preditos aos resultados
            'actual': actual_signals  # Adiciona sinais actuals (igual ao predito por agora)
        }, index=data.index)  # Usa o index dos dados para alinhar resultados

        return results_df, trades_rich_data  # Retorna DataFrame e dados estruturados para Rich

    def execute_trade(self, trade_type, price):
        """Executa uma ordem de compra ou venda simulada."""
        if trade_type == 'buy':
            units_to_buy = self.risk_manager.get_position_size(self.current_balance, price, risk_per_trade=0.01)  # Risco por trade como exemplo
            cost = units_to_buy * price * (1 + self.slippage) * (1 + self.commission_rate)

            if cost <= self.current_balance:
                self.current_balance -= cost
                self.trades.append({'type': 'buy', 'price': price, 'units': units_to_buy, 'cost': cost, 'balance': self.current_balance})
                # Removido print: print(f"📈 BUY {units_to_buy:.2f} unidades a {price:.2f}, Custo: {cost:.2f}, Saldo: {self.current_balance:.2f}")
            else:
                pass  # Removido print: print(f"⚠️ Saldo insuficiente para COMPRAR a {price:.2f}. Saldo atual: {self.current_balance:.2f}, Custo necessário: {cost:.2f}")

        elif trade_type == 'sell':
            units_held = sum([trade['units'] for trade in self.trades if trade['type'] == 'buy'])  # Cálculo ingênuo - melhorar isso para cenários reais
            if units_held > 0:
                revenue = units_held * price * (1 - self.slippage) * (1 - self.commission_rate)
                self.current_balance += revenue
                self.trades.append({'type': 'sell', 'price': price, 'units': units_held, 'revenue': revenue, 'balance': self.current_balance})
                # Removido print: print(f"📉 SELL {units_held:.2f} unidades a {price:.2f}, Receita: {revenue:.2f}, Saldo: {self.current_balance:.2f}")
            else:
                pass  # Removido print: print(f"⚠️ Sem unidades para VENDER a {price:.2f}. Unidades em posse: {units_held:.2f}")
        else:
            pass  # Removido print: print(f"🚫 Tipo de trade inválido: {trade_type}")


if __name__ == '__main__':
    # Exemplo de Uso (substitua com seu carregamento de dados e estratégia reais)
    data = pd.DataFrame({
        'timestamp': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-06']),
        'close': [29000, 29200, 29100, 29300, 29400, 29500]
    }).set_index('timestamp')  # Definindo timestamp como índice para exemplo

    backtester = Backtester()
    # Estratégia de exemplo: sempre 'buy'
    strategy = lambda row: 'buy'
    results_df, trades_rich_data = backtester.run(data, strategy)
'''
    console = Console()  # Cria console Rich
    table = Table(title="Resultados do Backtest (Rich)")  # Cria tabela Rich

    table.add_column("Timestamp", style="dim", width=20)  # Define colunas
    table.add_column("Signal", style="cyan")
    table.add_column("Price", justify="right", style="magenta")
    table.add_column("Balance", justify="right", style="green")

    for trade in trades_rich_data:  # Adiciona linhas da lista de dicionários
        table.add_row(
            str(trade['timestamp']), # Convert timestamp to string for Rich table
            trade['signal'] or '',  # Lida com sinais None graciosamente
            f"{trade['price']:.2f}",
            f"{trade['balance']:.2f}"
        )

    #console.print(table)  # Exibe a tabela Rich
    #print("DataFrame de Resultados (raw - para outros processos):")  # Mantém print para DataFrame raw
    #print(results_df)  # Exibe DataFrame de resultados (raw)'''