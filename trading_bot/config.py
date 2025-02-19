# ==========================#
# 📊 CONFIGURAÇÃO GLOBAL    #
# ==========================#

### 📌 1. Configuração da API ByBit
API_KEY = "SUA_API_KEY"
API_SECRET = "SUA_API_SECRET"
BASE_URL = "https://api.bybit.com"

### 📌 2. Configurações de Ativos
# 1 = Ativar, 0 = Desativar
CriptAtive_Dinamic_Apply = 0  # Ativos dinâmicos (Top Gainers/Losers)
Enable_Vet_Symbol = 0         # Vetor de symbols dinâmico (Top Movers)

crypto_list = ["BTCUSDT"]  # Treinamento
crypto_list_test = ["USUALUSDT"]      # Backtest

### 📌 3. Datas de Treinamento e Teste
Train_Date_Start = "2024-09-01"
Train_Date_End = "2024-12-30"
Test_Date_Start = "2025-02-01"
Test_Date_End = "2025-02-16"

### 📌 4. Configuração de Batch para Treinamento
Batch_Method = 1              # 1 = Unique, 0 = Pack
QTD_Pack_Batch = 1            # Total de Batchs no modo Pack
QTD_Unique_Batch = 500        # Velas por Batch (modo Unique)

### 📌 5. XGBoost (Classificação de Regime)
XGB_n_estimators = 100
XGB_max_depth = 4
XGB_learning_rate = 0.05

### 📌 6. Ensemble (Pesos dos Modelos)
ensemble_weight_informer = 0.4
ensemble_weight_patchtst = 0.4
ensemble_weight_lstm = 0.2

### 📌 7. Gestão de Risco Adaptativa
max_drawdown = 0.2            # Máx. Drawdown permitido (20%)
risk_per_trade = 0.01         # 1% de risco por trade
volatility_threshold = 0.03   # Volatilidade limite para alta alavancagem

### 📌 8. Backtest
initial_balance = 10000       # Saldo inicial (USD)
slippage = 0.0005             # Desvio (0.05%)
commission_rate = 0.0006      # Taxa (0.06%)

### 📌 9. Re-Treino
early_stopping_patience = 5   # Paciencia para Early Stopping
replay_buffer_size = 10000    # Tamanho do Replay Buffer

### 📌 10. Logs
log_level = "INFO"            # INFO, DEBUG, WARNING, ERROR
log_to_file = True            # Salvar logs em arquivo
log_file_path = "logs/trading_bot.log"
