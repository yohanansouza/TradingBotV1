# 🚀 Código Completo do `informer.py`
# =========================================

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

# ✅ 1. Bloco de Atenção Multi-Head
def attention(query, key, value, mask=None):
    scores = torch.matmul(query, key.transpose(-2, -1)) / torch.sqrt(torch.tensor(query.size(-1), dtype=torch.float32))
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    attn = F.softmax(scores, dim=-1)
    return torch.matmul(attn, value), attn

class MultiHeadAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(MultiHeadAttention, self).__init__()
        self.heads = heads
        self.embed_size = embed_size
        self.query = nn.Linear(embed_size, embed_size)
        self.key = nn.Linear(embed_size, embed_size)
        self.value = nn.Linear(embed_size, embed_size)
        self.fc_out = nn.Linear(embed_size, embed_size)

    def forward(self, x):
        q = self.query(x)
        k = self.key(x)
        v = self.value(x)
        out, _ = attention(q, k, v)
        return self.fc_out(out)

# ✅ 2. Codificador Informer (Encoder)
class InformerEncoder(nn.Module):
    def __init__(self, embed_size, heads, forward_expansion):
        super(InformerEncoder, self).__init__()
        self.attention = MultiHeadAttention(embed_size, heads)
        self.norm = nn.LayerNorm(embed_size)
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, forward_expansion * embed_size),
            nn.ReLU(),
            nn.Linear(forward_expansion * embed_size, embed_size)
        )

    def forward(self, x):
        attn = self.attention(x)
        x = self.norm(attn + x)
        forward = self.feed_forward(x)
        return self.norm(forward + x)

# ✅ 3. Modelo Completo Informer
class Informer(nn.Module):
    def __init__(self, input_dim, embed_size, heads, forward_expansion, num_layers):
        super(Informer, self).__init__()
        self.embed = nn.Linear(input_dim, embed_size)
        self.encoders = nn.ModuleList([
            InformerEncoder(embed_size, heads, forward_expansion) for _ in range(num_layers)
        ])
        self.fc_out = nn.Linear(embed_size, 1)

    def forward(self, x):
        x = self.embed(x)
        for encoder in self.encoders:
            x = encoder(x)
        return self.fc_out(x)

if __name__ == "__main__":
    sample_input = torch.rand((32, 50, 16))  # batch_size=32, sequence_length=50, input_features=16
    model = Informer(input_dim=16, embed_size=64, heads=4, forward_expansion=4, num_layers=3)
    output = model(sample_input)
    print(f"Saída do Modelo Informer: {output.shape}")
