# 🚀 Código Atualizado do `regime_classifier.py`
# =========================================

import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ✅ 1. Treinamento do Classificador de Regime com Salvamento de Modelo
def train_regime_classifier(data, model_path='regime_model.pkl'):
    X = data.drop(columns=['regime'])
    y = data['regime']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBClassifier(n_estimators=150, max_depth=5, learning_rate=0.03)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Acurácia: {accuracy:.2%}")
    print("📊 Relatório de Classificação:\n", classification_report(y_test, predictions))

    joblib.dump(model, model_path)
    print(f"💾 Modelo salvo em: {model_path}")
    
    return model

# ✅ 2. Carregar Modelo e Prever Regime
def predict_regime(model_path, new_data):
    model = joblib.load(model_path)
    return model.predict(new_data)

# ✅ 3. Execução de Teste
if __name__ == "__main__":
    sample_data = pd.DataFrame({
        'rsi': [30, 70, 40, 60, 50],
        'macd': [0.5, -0.3, 0.2, -0.1, 0.0],
        'volatility': [0.02, 0.03, 0.015, 0.025, 0.02],
        'regime': ['alta', 'baixa', 'lateral', 'alta', 'lateral']
    })

    model = train_regime_classifier(sample_data)
    test_sample = pd.DataFrame({'rsi': [45], 'macd': [0.1], 'volatility': [0.018]})
    prediction = predict_regime('regime_model.pkl', test_sample)
    print(f"🔮 Regime Previsto: {prediction[0]}")
