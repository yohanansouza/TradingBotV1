# 🚀 Código Completo do `logger.py`
# =========================================

import logging
import os
from datetime import datetime
import io  # Import the io module

def setup_logger(log_file="logs/trading_bot.log", log_level=logging.INFO):
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, mode='a', encoding='utf-8'),  # Explicitly set encoding for FileHandler
            logging.StreamHandler(stream=io.TextIOWrapper(os.sys.stdout.buffer, encoding='utf-8')) # Wrap stdout with UTF-8 encoder
        ]
    )
    logging.info("🚀 Logger inicializado com sucesso")

# ✅ 2. Funções Auxiliares para Registro
def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

def log_critical(message):
    logging.critical(message)

def log_debug(message):
    logging.debug(message)

# ✅ 3. Execução de Teste
if __name__ == "__main__":
    setup_logger()
    log_info("Iniciando teste de logger")
    log_debug("Mensagem de depuração")
    log_warning("Aviso de teste")
    log_error("Erro simulado")
    log_critical("Erro crítico simulado")
    print("✅ Teste de logger concluído")
