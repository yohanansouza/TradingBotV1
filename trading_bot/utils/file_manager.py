# 🚀 Código Corrigido do `file_manager.py`
# ==========================================

import os
import pandas as pd
import joblib

__all__ = ['save_results', 'save_csv', 'load_csv', 'save_model', 'load_model']

# ✅ 1. Salvar Resultados como CSV
def save_results(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if isinstance(data, pd.DataFrame):
        data.to_csv(file_path, index=False)
    elif isinstance(data, dict):
        pd.DataFrame([data]).to_csv(file_path, index=False)
    else:
        raise ValueError("Formato de dados inválido. Use DataFrame ou dict.")
    print(f"💾 Resultados salvos em: {file_path}")

# ✅ 2. Carregar CSV
def load_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"⚠️ Arquivo {file_path} não encontrado.")
        return pd.DataFrame()

# ✅ 3. Salvar Modelo (Checkpoints)
def save_model(model, model_path):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"💾 Modelo salvo em: {model_path}")

# ✅ 4. Carregar Modelo (Checkpoints)
def load_model(model_path):
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        print(f"⚠️ Modelo {model_path} não encontrado.")
        return None

# ✅ 5. Execução de Teste
if __name__ == "__main__":
    df = pd.DataFrame({'coluna1': [1, 2, 3], 'coluna2': ['A', 'B', 'C']})
    save_results(df, 'data/test_results.csv')
    loaded_df = load_csv('data/test_results.csv')
    print("📊 DataFrame Carregado:\n", loaded_df)
