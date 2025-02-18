# 🚀 Código Corrigido do `retrainer.py`
# ==========================================

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

__all__ = ['ModelRetrainer']

# ✅ 1. Classe ModelRetrainer para Re-Treino de Modelos
class ModelRetrainer:
    def __init__(self, model_path='models/regime_model.pkl'):
        self.model_path = model_path

    def retrain(self, error_data):
        X = error_data.drop(columns=['actual', 'predicted'])
        y = error_data['actual']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.04)
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        print("📊 Relatório Pós-Re-Treino:")
        print(classification_report(y_test, predictions))
        
        joblib.dump(model, self.model_path)
        print(f"💾 Modelo re-treinado salvo em {self.model_path}")

# ✅ 2. Execução de Teste
if __name__ == "__main__":
    sample_errors = pd.DataFrame({
        'rsi': [45, 60, 55],
        'macd': [0.1, -0.2, 0.15],
        'volatility': [0.02, 0.03, 0.025],
        'actual': ['alta', 'baixa', 'lateral'],
        'predicted': ['baixa', 'alta', 'baixa']
    })
    
    retrainer = ModelRetrainer()
    retrainer.retrain(sample_errors)
