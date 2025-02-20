# 📂 Módulo: `main.py`
# 🚀 Código Completo do `main.py`
# ==================================================================

import logging
from trading_bot.config import *
from trading_bot.db.data_manager import import_training_data, import_testing_data
from trading_bot.models.informer import Informer
from trading_bot.models.patchtst import PatchTST
from trading_bot.models.lstm import LSTMModel
from trading_bot.models.ppo import PPOAgent
from trading_bot.models.ensemble import EnsembleModel
from trading_bot.utils.logger import setup_logger
from trading_bot.utils.file_manager import save_results
from trading_bot.utils.risk_manager import RiskManager
from trading_bot.utils.backtester import Backtester
from trading_bot.validators.validator import ErrorValidator
from trading_bot.retrainer.retrainer import ModelRetrainer
from trading_bot.db.db_manager import get_historical_data_from_db  # ✅ Import get_historical_data_from_db

from rich.console import Console
from rich.table import Table
from rich import print  # Optional, but rich's print can be nice too.


# ✅ 1. Configuração Global
setup_logger()
logging.info("🚀 Iniciando o Trading Bot")

# ✅ 2. Inicialização dos Modelos
informer = Informer(input_dim=16, embed_size=64, heads=4, forward_expansion=4, num_layers=3)
patchtst = PatchTST(input_dim=16, embed_size=64, patch_size=4, heads=4, forward_expansion=4, num_layers=3)
lstm = LSTMModel(input_dim=16, hidden_dim=64, num_layers=2, output_dim=1)
ppo = PPOAgent(state_dim=16, action_dim=3, hidden_dim=64)

ensemble = EnsembleModel(
    informer=informer,
    patchtst=patchtst,
    lstm=lstm,
    ppo=ppo,
    weights={'informer': 0.3, 'patchtst': 0.3, 'lstm': 0.2, 'ppo': 0.2}
)
logging.info("✅ Modelos inicializados.")

# ✅ 3. Importação de Dados
import_training_data()
import_testing_data()

# ✅ 4. Execução do Backtest
backtester = Backtester()
# ✅ Fetch testing data from DB using get_historical_data_from_db and crypto_list_test
testing_data = get_historical_data_from_db(crypto_list_test[0])
print(f"Type of index for testing_data in main.py before backtest: {type(testing_data.index)}") # Debug print
results_df, trades_rich_data = backtester.run(data=testing_data, strategy=lambda x: 'buy')  # ✅ Pass fetched testing_data
save_results(results_df, 'logs/backtest_results.csv')

# ✅ 5. Análise de Erros
validator = ErrorValidator()
errors = validator.analyze_errors(results_df)
validator.save_error_report(errors)

# ✅ 6. Re-Treino com Base nos Erros
retrainer = ModelRetrainer()
retrainer.retrain(model_type='xgboost', error_data=errors)  # ✅ Pass model_type and error_data


# ✅ 7. Função para exibir resultados do Backtest com Rich
def display_backtest_results_rich(trades_data):
    """Exibe os resultados do backtest usando a biblioteca Rich."""
    console = Console()
    table = Table(title="Resultados do Backtest")

    table.add_column("Timestamp", style="dim", width=20)
    table.add_column("Signal", style="cyan")
    table.add_column("Price", justify="right", style="magenta")
    table.add_column("Balance", justify="right", style="green")

    for trade in trades_data:
        table.add_row(
            str(trade['timestamp']), # Ensure timestamp is a string for Rich table
            trade['signal'] or '',  # Handle None signals gracefully
            f"{trade['price']:.2f}",
            f"{trade['balance']:.2f}"
        )

    console.print(table)
    print(f"[bold green]✅ Backtest Concluído! Resultados exibidos acima.[/bold green]")


# ✅ 8. Exibir resultados Rich
display_backtest_results_rich(trades_rich_data)  # Chama a função para exibir com Rich


logging.info("🏁 Pipeline completo!")