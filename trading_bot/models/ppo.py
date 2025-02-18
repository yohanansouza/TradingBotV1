# 🚀 Código Completo do `ppo.py`
# =========================================

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# ✅ 1. Definição da Rede Neural para a Política (Actor) e Crítica (Critic)
class Actor(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim):
        super(Actor, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Softmax(dim=-1)
        )

    def forward(self, state):
        return self.network(state)


class Critic(nn.Module):
    def __init__(self, state_dim, hidden_dim):
        super(Critic, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, state):
        return self.network(state)

# ✅ 2. Classe PPO Principal
class PPOAgent:
    def __init__(self, state_dim, action_dim, hidden_dim, lr=3e-4, gamma=0.99, clip_epsilon=0.2):
        self.actor = Actor(state_dim, action_dim, hidden_dim)
        self.critic = Critic(state_dim, hidden_dim)
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=lr)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=lr)
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon

    def compute_advantages(self, rewards, values):
        returns = []
        advantage = 0
        for reward, value in zip(reversed(rewards), reversed(values)):
            advantage = reward + self.gamma * advantage - value
            returns.insert(0, advantage)
        return returns

    def update(self, states, actions, log_probs, returns):
        values = self.critic(states).squeeze()
        advantages = torch.tensor(returns) - values.detach()
        
        new_log_probs = torch.log(self.actor(states).gather(1, actions.unsqueeze(1))).squeeze()
        ratio = torch.exp(new_log_probs - log_probs)
        
        surrogate1 = ratio * advantages
        surrogate2 = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
        actor_loss = -torch.min(surrogate1, surrogate2).mean()
        
        critic_loss = nn.MSELoss()(values, torch.tensor(returns))
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

# ✅ 3. Execução de Teste
if __name__ == "__main__":
    sample_state = torch.rand((32, 16))  # batch_size=32, state_dim=16
    agent = PPOAgent(state_dim=16, action_dim=3, hidden_dim=64)
    actions = agent.actor(sample_state)
    values = agent.critic(sample_state)
    print(f"Saída da Rede Actor: {actions.shape}")
    print(f"Saída da Rede Critic: {values.shape}")
