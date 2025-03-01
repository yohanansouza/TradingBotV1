# 📂 Módulo: `validator.py`
# 🚀 Correção do Erro: "KeyError: 'actual'"
# ==================================================

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

__all__ = ['ErrorValidator']

# ✅ 1. Classe ErrorValidator para Validação Pós-Backtest
class ErrorValidator:
    def __init__(self):
        pass

    def analyze_errors(self, backtest_results):
        if 'actual' not in backtest_results.columns or 'predicted' not in backtest_results.columns:
            print("⚠️ Erro: As colunas 'actual' ou 'predicted' não estão presentes no DataFrame.")
            return pd.DataFrame()
        
        errors = backtest_results[backtest_results['actual'] != backtest_results['predicted']]
        error_rate = len(errors) / len(backtest_results) if len(backtest_results) > 0 else 0
        print(f"❌ Taxa de Erro: {error_rate:.2%}")
        print("📊 Relatório de Classificação:")
        print(classification_report(backtest_results['actual'], backtest_results['predicted']))
        return errors

    def identify_error_patterns(self, errors):
        if errors.empty:
            print("✅ Nenhum erro detectado.")
            return pd.DataFrame()
        
        pattern_summary = errors.groupby(['actual', 'predicted']).size().reset_index(name='count')
        print("📈 Padrões de Erros:")
        print(pattern_summary)
        return pattern_summary

    def save_error_report(self, errors, file_path='logs/error_report.csv'):
        if errors.empty:
            print("⚠️ Nenhum erro para salvar.")
            return
        
        errors.to_csv(file_path, index=False)
        print(f"💾 Relatório de erros salvo em: {file_path}")

# ✅ 2. Execução de Teste
if __name__ == "__main__":
    sample_results = pd.DataFrame({
        'actual': ['alta', 'baixa', 'lateral', 'alta', 'baixa'],
        'predicted': ['baixa', 'baixa', 'lateral', 'baixa', 'alta']
    })

    validator = ErrorValidator()
    errors = validator.analyze_errors(sample_results)
    patterns = validator.identify_error_patterns(errors)
    validator.save_error_report(errors)
