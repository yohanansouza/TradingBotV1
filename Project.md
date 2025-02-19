# 📂 Módulo: `Project Overview`
# 🚀 Descrição Completa das Funções e Variáveis em Cada Módulo
# ==========================================================

### 📁 `config.py`
- **Variáveis:** Define listas de criptomoedas e datas.
- `crypto_list`, `crypto_list_test`, `Train_Date_Start`, `Train_Date_End`, `Test_Date_Start`, `Test_Date_End`.

### 📁 `db_manager.py`
- **Funções:**
  - `create_database()`: Cria o banco e tabela `historical_data`.
  - `store_historical_data()`: Armazena dados no banco.
  - `get_existing_date_range()`: Consulta datas armazenadas.
- **Variáveis:** `DB_PATH`: Caminho do banco.

### 📁 `data_manager.py`
- **Funções:**
  - `import_data_for_symbol()`: Baixa e salva dados de mercado.
  - `import_training_data()`, `import_testing_data()`: Utiliza datas e listas do `config.py`.

### 📁 `bybit_api.py`
- **Funções:**
  - `get_historical_data()`: Obtém dados via API.
  - `request_with_retries()`: Lida com tentativas automáticas.
- **Variáveis:** `BASE_URL`: URL da API.

### 📁 `indicators.py`
- **Funções:**
  - `compute_rsi()`, `compute_macd()`, `compute_bollinger_bands()`: Calcula indicadores técnicos.

### 📁 `informer.py`
- **Funções:**
  - `train()`, `predict()`: Implementa o modelo Informer para séries temporais.

### 📁 `patchtst.py`
- **Funções:**
  - `train()`, `predict()`: Modelo PatchTST especializado em padrões de séries temporais.

### 📁 `lstm.py`
- **Funções:**
  - `train()`, `predict()`: Modelo LSTM para previsões curtas.

### 📁 `ppo.py`
- **Funções:**
  - `train()`, `select_action()`: Modelo PPO para decisões baseadas em reforço.

### 📁 `ensemble.py`
- **Funções:**
  - `combine_predictions()`: Faz ensemble das previsões (`informer`, `patchtst`, `lstm`, `ppo`).
  - `evaluate()`: Avalia resultados combinados.

### 📁 `risk_manager.py`
- **Funções:**
  - `calculate_risk()`: Define tamanho da posição.
  - `adjust_risk()`: Ajusta com base no drawdown.

### 📁 `regime_classifier.py`
- **Funções:**
  - `train_regime_classifier()`: Treina um classificador de regime com `XGBoost`.
  - `predict_regime()`: Classifica regimes de mercado.

### 📁 `error_analyzer.py`
- **Funções:**
  - `analyze_errors()`: Identifica falhas nas previsões.
  - `generate_error_report()`: Gera relatório de erros.

### 📁 `main.py`
- **Funções:**
  - `initialize()`: Executa pipeline completo (importação, treino, teste, validação, re-treino).
  - Utiliza todos os módulos, cria logs e salva resultados.

### 📁 `informer.py`
- **Funções:**
  - `Informer()`: Constrói o modelo de previsão baseado em attention.
  - `forward()`: Executa a previsão no modelo.
- **Variáveis:** `input_dim`, `embed_size`, `num_layers`, `heads`.

### 📁 `patchtst.py`
- **Funções:**
  - `PatchTST()`: Implementa Transformer com patching para séries temporais.
  - `train()`: Treina o modelo com dados históricos.
- **Variáveis:** `patch_size`, `input_dim`, `heads`, `num_layers`.

### 📁 `lstm.py`
- **Funções:**
  - `LSTMModel()`: Constrói a rede LSTM.
  - `predict()`: Realiza previsões baseadas em séries temporais.
- **Variáveis:** `input_dim`, `hidden_dim`, `num_layers`, `output_dim`.

### 📁 `ensemble.py`
- **Funções:**
  - `EnsembleModel()`: Combina previsões de `Informer`, `PatchTST`, `LSTM`, e `PPO`.
  - `predict()`: Gera decisão final ponderada.
- **Variáveis:** `weights`, `models`.

### 📁 `ppo.py`
- **Funções:**
  - `PPOAgent()`: Implementa o algoritmo Proximal Policy Optimization.
  - `train()`: Treina o agente com base em recompensas.
- **Variáveis:** `state_dim`, `action_dim`, `hidden_dim`, `lr`.

### 📁 `risk_manager.py`
- **Funções:**
  - `calculate_risk()`: Calcula tamanho de posição com base em volatilidade.
  - `adjust_risk()`: Ajusta risco com base no drawdown.
- **Variáveis:** `risk_per_trade`, `max_drawdown`.

### 📁 `regime_classifier.py`
- **Funções:**
  - `train_regime_classifier()`: Treina modelo (`XGBoost`) para classificar regimes.
  - `predict_regime()`: Classifica novo regime.
- **Variáveis:** `X`, `y`, `model_path`.

### 📁 `error_analyzer.py`
- **Funções:**
  - `analyze_errors()`: Analisa erros entre previsões e realidade.
  - `identify_error_patterns()`: Gera padrões de erro mais comuns.
- **Variáveis:** `errors`, `error_rate`.

### 📁 `main.py`
- **Funções:**
  - `initialize_pipeline()`: Inicia pipeline completo.
  - `execute_trading_strategy()`: Executa estratégia de trading completa.
- **Variáveis:** `ensemble`, `risk_manager`, `validator`, `retrainer`.
