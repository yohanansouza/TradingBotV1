# 🚀 Código Completo do `lstm.py`
# =========================================

import torch
import torch.nn as nn

# ✅ 1. Definição da Camada LSTM
class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.3):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        out = self.fc(lstm_out[:, -1, :])  # Usando apenas a última saída da sequência
        return out

# ✅ 2. Execução de Teste com Input de Exemplo
if __name__ == "__main__":
    sample_input = torch.rand((32, 100, 16))  # batch_size=32, sequence_length=100, input_features=16
    model = LSTMModel(input_dim=16, hidden_dim=64, num_layers=2, output_dim=1)
    output = model(sample_input)
    print(f"Saída do Modelo LSTM: {output.shape}")
