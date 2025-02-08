# trading_bot/config.py
# Configuração global do sistema

# Chave da API para acesso à corretora (substituir pelo valor real)
API_KEY = "SUA_API_KEY"
API_SECRET = "SUA_API_SECRET"
BASE_URL = "https://api.bybit.com"

# Parâmetros de gestão de risco
MAX_DAILY_LOSS = -500  # Stop diário em USDT
MAX_DAILY_GAIN = 1000  # Meta diária de lucro
SEQUENCIA_MAXIMA_DE_PERDAS = 3  # Reduz posição após 3 perdas seguidas

# Lista de criptomoedas suportadas
crypto_list = ["BTCUSDT"]

# Definição do mínimo de dados necessários para iniciar o treinamento do modelo de Machine Learning
# Esse valor pode ser ajustado conforme a necessidade para acelerar ou tornar mais robusto o treinamento inicial
MIN_DATA_REQUIRED = 100  # Número mínimo de registros na tabela historical_data para iniciar o treinamento

# Parâmetros de treinamento evolutivo
FAMILIAS_DE_GERACOES = 10  # Número de famílias de gerações para otimizar o treinamento
GERACOES_POR_CRIPTO = 10  # Número de gerações antes de avaliar mudanças na criptomoeda
