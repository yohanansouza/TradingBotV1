# 🚀 Código Completo do `ensemble.py`
# =========================================

import torch
import torch.nn as nn
from trading_bot.models.informer import Informer
from trading_bot.models.patchtst import PatchTST
from trading_bot.models.lstm import LSTMModel
from trading_bot.models.ppo import PPOAgent

# ✅ 1. Definição do Modelo Ensemble
class EnsembleModel(nn.Module):
    def __init__(self, informer, patchtst, lstm, ppo, weights):
        super(EnsembleModel, self).__init__()
        self.informer = informer
        self.patchtst = patchtst
        self.lstm = lstm
        self.ppo = ppo
        self.weights = weights  # Ex: {'informer': 0.3, 'patchtst': 0.3, 'lstm': 0.2, 'ppo': 0.2}

    def forward(self, x):
        informer_pred = self.informer(x).squeeze()
        patchtst_pred = self.patchtst(x).squeeze()
        lstm_pred = self.lstm(x).squeeze()
        ppo_action = self.ppo.actor(x).argmax(dim=1).float()  # PPO retorna ações, usamos como proxy de decisão
        
        ensemble_output = (
            self.weights['informer'] * informer_pred +
            self.weights['patchtst'] * patchtst_pred +
            self.weights['lstm'] * lstm_pred +
            self.weights['ppo'] * ppo_action
        )
        return ensemble_output

# ✅ 2. Execução de Teste
if __name__ == "__main__":
    sample_input = torch.rand((32, 100, 16))  # batch_size=32, seq_len=100, input_features=16
    informer = Informer(input_dim=16, embed_size=64, heads=4, forward_expansion=4, num_layers=3)
    patchtst = PatchTST(input_dim=16, embed_size=64, patch_size=4, heads=4, forward_expansion=4, num_layers=3)
    lstm = LSTMModel(input_dim=16, hidden_dim=64, num_layers=2, output_dim=1)
    ppo = PPOAgent(state_dim=16, action_dim=3, hidden_dim=64)
    
    ensemble = EnsembleModel(
        informer, patchtst, lstm, ppo,
        weights={'informer': 0.3, 'patchtst': 0.3, 'lstm': 0.2, 'ppo': 0.2}
    )
    
    output = ensemble(sample_input)
    print(f"Saída do Modelo Ensemble: {output.shape}")
