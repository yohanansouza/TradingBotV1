# 🚀 Código Completo do `error_analyzer.py`
# =========================================

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

# ✅ 1. Analisador de Erros em Backtest
def analyze_errors(results, predictions):
    errors = results[predictions != results['actual']]
    error_rate = len(errors) / len(results)
    
    print(f"❌ Taxa de Erro: {error_rate:.2%}")
    print("📊 Relatório de Classificação:")
    print(classification_report(results['actual'], predictions))
    
    return errors

# ✅ 2. Identificação de Padrões de Erros Frequentes
def error_patterns(errors):
    pattern_summary = errors.groupby(['actual', 'predicted']).size().reset_index(name='count')
    print("📈 Padrões de Erros:")
    print(pattern_summary)
    
    return pattern_summary

# ✅ 3. Salvar Relatório de Erros
def save_error_report(errors, file_path='error_report.csv'):
    errors.to_csv(file_path, index=False)
    print(f"💾 Relatório de erros salvo em {file_path}")

# ✅ 4. Execução de Teste
if __name__ == "__main__":
    # Exemplo de dados fictícios
    results = pd.DataFrame({
        'actual': ['alta', 'baixa', 'lateral', 'alta', 'baixa'],
        'predicted': ['baixa', 'baixa', 'lateral', 'baixa', 'alta']
    })
    
    predictions = results['predicted']
    errors = analyze_errors(results, predictions)
    patterns = error_patterns(errors)
    save_error_report(errors)
