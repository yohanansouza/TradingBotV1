# trading_bot/models/ml_forecast_logs.py
# Módulo responsável pelo gerenciamento e registro dos logs de treinamento do modelo de Machine Learning.

import os

TRAINING_LOG_PATH = "logs/training_versions"
GENERAL_LOG_FILE = "logs/general_training_log.csv"


# Criar pastas e arquivos de log, se não existirem
if not os.path.exists(TRAINING_LOG_PATH):
    os.makedirs(TRAINING_LOG_PATH)
if not os.path.exists(GENERAL_LOG_FILE):
    with open(GENERAL_LOG_FILE, "w") as log:
        log.write("Versão,Registros,Win Rate (%),Take Profit (%),Stop Loss (%),Lucro Médio\n")

# Criar uma nova pasta de versão para armazenar logs e modelos
def create_training_version():
    existing_versions = [d for d in os.listdir(TRAINING_LOG_PATH) if d.startswith("version_")]
    next_version = f"version_{len(existing_versions) + 1:03d}"
    new_version_path = os.path.join(TRAINING_LOG_PATH, next_version)
    os.makedirs(new_version_path)
    return new_version_path

def save_training_log(version_path, message):
    """
    Salva um log individual para uma versão de treinamento específica.
    """
    log_file = os.path.join(version_path, "training_log.txt")
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(message + "\n")

# Atualizar log geral consolidado de todas as versões
def update_general_log(version, registros, win_rate, take_profit, stop_loss, lucro_medio):
    with open(GENERAL_LOG_FILE, "a", encoding="utf-8") as gen_log:
        gen_log.write(f"{version},{registros},{win_rate},{take_profit},{stop_loss},{lucro_medio}\n")
