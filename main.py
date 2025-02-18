# 🚀 Código Completo do `main.py`
# ======================================

import sys
import logging
from trading_bot.config import *
from trading_bot.db.data_manager import import_training_data, import_testing_data
from trading_bot.models.ensemble import EnsembleModel
from trading_bot.utils.logger import setup_logger
from trading_bot.utils.file_manager import save_results
from trading_bot.utils.risk_manager import RiskManager
from trading_bot.utils.backtester import Backtester
from trading_bot.validators.validator import ErrorValidator
from trading_bot.retrainer.retrainer import ModelRetrainer

# ✅ 1. Configuração Global e Logs
setup_logger()
logging.info("🚀 Iniciando o Trading Bot")

# ✅ 2. Importação de Dados
logging.info("⬇️ Importando dados de treinamento...")
import_training_data()
logging.info("⬇️ Importando dados de teste...")
import_testing_data()

# ✅ 3. Inicialização de Modelos
ensemble = EnsembleModel()
risk_manager = RiskManager()
backtester = Backtester()
validator = ErrorValidator()
retrainer = ModelRetrainer()

# ✅ 4. Execução do Pipeline
logging.info("⚙️ Executando Backtest...")
results = backtester.run(ensemble)
logging.info("💾 Salvando resultados...")
save_results(results, "data/datasets/backtest_results.csv")

# ✅ 5. Validação de Erros
logging.info("🔍 Validando erros do Backtest...")
errors = validator.validate(results)
logging.info(f"📊 Erros identificados: {len(errors)}")

# ✅ 6. Re-Treino com Ajustes
if errors:
    logging.info("♻️ Iniciando Re-Treino...")
    retrainer.retrain(errors)
    logging.info("✅ Re-Treino concluído")
else:
    logging.info("✅ Nenhum erro relevante identificado. Re-Treino não necessário")

logging.info("🏁 Pipeline concluído com sucesso!")

if __name__ == "__main__":
    try:
        logging.info("🎯 Iniciando Main Pipeline")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Erro durante a execução: {e}")
        sys.exit(1)
