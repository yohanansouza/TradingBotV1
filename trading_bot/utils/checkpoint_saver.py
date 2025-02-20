# 📂 Módulo: `checkpoint_saver.py`
# 🚀 Responsável por salvar e carregar checkpoints do modelo para evitar retrabalho.
# ======================================================

import os
import joblib
import numpy as np

def save_checkpoint(model, checkpoint_path="models/checkpoints/model_checkpoint.pkl"):
    """Salva o modelo em um checkpoint para evitar perda de progresso."""
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    joblib.dump(model, checkpoint_path)
    print(f"💾 Checkpoint salvo em {checkpoint_path}")

def load_checkpoint(checkpoint_path="models/checkpoints/model_checkpoint.pkl"):
    """Carrega um modelo salvo do checkpoint, se disponível."""
    if os.path.exists(checkpoint_path):
        print(f"🔄 Checkpoint encontrado! Carregando de {checkpoint_path}")
        return joblib.load(checkpoint_path)
    print("⚠️ Nenhum checkpoint encontrado. Iniciando do zero.")
    return None

def validate_labels(y):
    """Corrige rótulos inválidos, transformando-os em valores numéricos."""
    unique_values = np.unique(y)
    if not np.issubdtype(y.dtype, np.number):
        print(f"⚠️ Corrigindo rótulos inválidos: {unique_values}")
        label_map = {label: i for i, label in enumerate(unique_values)}
        return np.array([label_map[label] for label in y]), label_map
    return y, None