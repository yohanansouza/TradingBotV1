# 🚀 Código Completo do `regime_classifier.py`
# =========================================

import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ✅ 1. Treinamento do Classificador de Regime
def train_regime_classifier(data):
    X = data.drop(columns=['regime'])
    y = data['regime']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Acurácia do Classificador de Regime: {accuracy:.2%}")
    
    return model

# ✅ 2. Previsão de Regime
def predict_regime(model, new_data):
    return model.predict(new_data)

# ✅ 3. Execução de Teste
if __name__ == "__main__":
    # Exemplo de dados fictícios com colunas simuladas
    sample_data = pd.DataFrame({
        'rsi': [30, 70, 40, 60, 50],
        'macd': [0.5, -0.3, 0.2, -0.1, 0.0],
        'volatility': [0.02, 0.03, 0.015, 0.025, 0.02],
        'regime': ['alta', 'baixa', 'lateral', 'alta', 'lateral']
    })

    model = train_regime_classifier(sample_data)
    test_sample = pd.DataFrame({'rsi': [45], 'macd': [0.1], 'volatility': [0.018]})
    prediction = predict_regime(model, test_sample)
    print(f"🔮 Regime Previsto: {prediction[0]}")
