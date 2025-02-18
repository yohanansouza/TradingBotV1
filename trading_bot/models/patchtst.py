# 🚀 Código Completo do `patchtst.py`
# =========================================

import torch
import torch.nn as nn
import torch.nn.functional as F

# ✅ 1. Bloco Conv1D para Captura de Padrões Locais
class ConvBlock(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv1d(input_dim, hidden_dim, kernel_size=3, padding=1)
        self.norm = nn.BatchNorm1d(hidden_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x.transpose(1, 2))
        x = self.norm(x)
        x = self.relu(x)
        return x.transpose(1, 2)

# ✅ 2. Patch Embedding com Overlapping
class PatchEmbedding(nn.Module):
    def __init__(self, input_dim, patch_size, embed_size):
        super(PatchEmbedding, self).__init__()
        self.projection = nn.Conv1d(input_dim, embed_size, kernel_size=patch_size, stride=patch_size)
        
    def forward(self, x):
        return self.projection(x.transpose(1, 2)).transpose(1, 2)

# ✅ 3. Codificador PatchTST (Transformer Encoder)
class PatchTSTEncoder(nn.Module):
    def __init__(self, embed_size, heads, forward_expansion):
        super(PatchTSTEncoder, self).__init__()
        self.attention = nn.MultiheadAttention(embed_size, heads)
        self.norm1 = nn.LayerNorm(embed_size)
        self.norm2 = nn.LayerNorm(embed_size)
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, forward_expansion * embed_size),
            nn.ReLU(),
            nn.Linear(forward_expansion * embed_size, embed_size)
        )

    def forward(self, x):
        attn_output, _ = self.attention(x, x, x)
        x = self.norm1(attn_output + x)
        ff_output = self.feed_forward(x)
        return self.norm2(ff_output + x)

# ✅ 4. Modelo Completo PatchTST
class PatchTST(nn.Module):
    def __init__(self, input_dim, embed_size, patch_size, heads, forward_expansion, num_layers):
        super(PatchTST, self).__init__()
        self.embedding = PatchEmbedding(input_dim, patch_size, embed_size)
        self.encoders = nn.ModuleList([
            PatchTSTEncoder(embed_size, heads, forward_expansion) for _ in range(num_layers)
        ])
        self.fc_out = nn.Linear(embed_size, 1)

    def forward(self, x):
        x = self.embedding(x)
        for encoder in self.encoders:
            x = encoder(x.transpose(0, 1)).transpose(0, 1)
        return self.fc_out(x.mean(dim=1))

if __name__ == "__main__":
    sample_input = torch.rand((32, 100, 16))  # batch_size=32, sequence_length=100, input_features=16
    model = PatchTST(input_dim=16, embed_size=64, patch_size=4, heads=4, forward_expansion=4, num_layers=3)
    output = model(sample_input)
    print(f"Saída do Modelo PatchTST: {output.shape}")
