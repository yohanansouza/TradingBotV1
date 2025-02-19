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
results = backtester.run(data=import_testing_data(), strategy=lambda x: 'buy')
save_results(results, 'logs/backtest_results.csv')

# ✅ 5. Análise de Erros
validator = ErrorValidator()
errors = validator.analyze_errors(results)
validator.save_error_report(errors)

# ✅ 6. Re-Treino com Base nos Erros
retrainer = ModelRetrainer()
retrainer.retrain(errors)

logging.info("🏁 Pipeline completo!")
