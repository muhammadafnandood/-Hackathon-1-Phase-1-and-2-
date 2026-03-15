---
title: "Chapter 8: Machine Learning for Robotics"
sidebar_label: "ML for Robotics"
---

# Chapter 8: Machine Learning for Robotics

## Overview

Machine learning enables robots to learn from experience rather than being explicitly programmed for every scenario.

## Reinforcement Learning

### Fundamentals

**Markov Decision Process (MDP)**:
- States (S)
- Actions (A)
- Transition function (P)
- Reward function (R)
- Discount factor (γ)

**Goal**: Find policy π that maximizes expected return

### Q-Learning

Value-based RL algorithm:

```python
class QLearning:
    def __init__(self, n_states, n_actions, lr=0.1, gamma=0.99, epsilon=0.1):
        self.q_table = np.zeros((n_states, n_actions))
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_actions = n_actions
    
    def get_action(self, state):
        """Epsilon-greedy action selection"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state):
        """Update Q-value"""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.lr * td_error
```

### Deep Q-Networks (DQN)

Neural network approximation of Q-function:

```python
import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
    
    def forward(self, x):
        return self.network(x)

class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99, 
                 buffer_size=10000, batch_size=64):
        self.gamma = gamma
        self.batch_size = batch_size
        
        self.q_network = DQN(state_dim, action_dim)
        self.target_network = DQN(state_dim, action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=lr)
        self.replay_buffer = ReplayBuffer(buffer_size)
    
    def select_action(self, state, epsilon=0.1):
        if np.random.random() < epsilon:
            return np.random.randint(self.q_network.output_dim)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                q_values = self.q_network(state_tensor)
                return q_values.argmax().item()
    
    def train_step(self):
        if len(self.replay_buffer) < self.batch_size:
            return
        
        # Sample batch
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)
        
        # Compute Q values
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        current_q = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        with torch.no_grad():
            next_q = self.target_network(next_states).max(1)[0]
            target_q = rewards + self.gamma * next_q * (1 - dones)
        
        # Update network
        loss = nn.MSELoss()(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
    
    def update_target_network(self):
        self.target_network.load_state_dict(self.q_network.state_dict())
```

### Policy Gradient Methods

Directly optimize policy:

```python
class PolicyGradient:
    def __init__(self, state_dim, action_dim, lr=1e-3, gamma=0.99):
        self.gamma = gamma
        self.policy = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Softmax(dim=-1)
        )
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
    
    def select_action(self, state):
        state_tensor = torch.FloatTensor(state)
        probs = self.policy(state_tensor)
        dist = torch.distributions.Categorical(probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)
    
    def update(self, states, actions, rewards):
        # Compute returns
        returns = []
        G = 0
        for reward in reversed(rewards):
            G = reward + self.gamma * G
            returns.insert(0, G)
        
        returns = torch.FloatTensor(returns)
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # Compute policy loss
        log_probs = []
        for state, action in zip(states, actions):
            _, log_prob = self.select_action(state)
            log_probs.append(log_prob)
        
        log_probs = torch.stack(log_probs)
        policy_loss = -(log_probs * returns).mean()
        
        # Update policy
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()
        
        return policy_loss.item()
```

### Proximal Policy Optimization (PPO)

State-of-the-art policy gradient method:

```python
class PPOAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, 
                 clip_epsilon=0.2, c1=0.5, c2=0.01):
        self.gamma = gamma
        self.clip_epsilon = clip_epsilon
        self.c1 = c1  # Value loss coefficient
        self.c2 = c2  # Entropy coefficient
        
        # Actor-Critic network
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.Tanh(),
            nn.Linear(256, 256),
            nn.Tanh(),
            nn.Linear(256, action_dim)
        )
        
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.Tanh(),
            nn.Linear(256, 256),
            nn.Tanh(),
            nn.Linear(256, 1)
        )
        
        self.optimizer = torch.optim.Adam(
            list(self.actor.parameters()) + list(self.critic.parameters()),
            lr=lr
        )
    
    def select_action(self, state):
        state_tensor = torch.FloatTensor(state)
        action_mean = self.actor(state_tensor)
        action_std = torch.exp(torch.zeros_like(action_mean) * -1)
        dist = torch.distributions.Normal(action_mean, action_std)
        action = dist.sample()
        return action, dist.log_prob(action)
    
    def compute_gae(self, rewards, values, dones, gae_lambda=0.95):
        """Generalized Advantage Estimation"""
        advantages = []
        gae = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
            
            delta = rewards[t] + self.gamma * next_value * (1 - dones[t]) - values[t]
            gae = delta + self.gamma * gae_lambda * (1 - dones[t]) * gae
            advantages.insert(0, gae)
        
        returns = [adv + val for adv, val in zip(advantages, values)]
        return advantages, returns
    
    def update(self, states, actions, old_log_probs, rewards, dones, n_epochs=10):
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        old_log_probs = torch.FloatTensor(old_log_probs)
        rewards = torch.FloatTensor(rewards)
        dones = torch.FloatTensor(dones)
        
        # Compute values and advantages
        with torch.no_grad():
            values = self.critic(states).squeeze().tolist()
        
        advantages, returns = self.compute_gae(rewards, values, dones)
        advantages = torch.FloatTensor(advantages)
        returns = torch.FloatTensor(returns)
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # PPO update for multiple epochs
        for _ in range(n_epochs):
            # Compute current log probs
            action_means = self.actor(states)
            action_stds = torch.exp(torch.zeros_like(action_means) * -1)
            dist = torch.distributions.Normal(action_means, action_stds)
            log_probs = dist.log_prob(actions).sum(dim=-1)
            
            # Compute ratio
            ratio = torch.exp(log_probs - old_log_probs)
            
            # Clipped surrogate objective
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * advantages
            policy_loss = -torch.min(surr1, surr2).mean()
            
            # Value loss
            values_pred = self.critic(states).squeeze()
            value_loss = nn.MSELoss()(values_pred, returns)
            
            # Entropy bonus
            entropy = dist.entropy().mean()
            
            # Total loss
            loss = policy_loss + self.c1 * value_loss - self.c2 * entropy
            
            # Update
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        
        return loss.item()
```

## Imitation Learning

Learning from demonstrations:

### Behavioral Cloning

```python
class BehavioralCloning:
    def __init__(self, state_dim, action_dim):
        self.policy = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, action_dim),
            nn.Tanh()
        )
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=1e-3)
    
    def train(self, states, actions, n_epochs=100, batch_size=64):
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        
        dataset = torch.utils.data.TensorDataset(states, actions)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        for epoch in range(n_epochs):
            total_loss = 0
            for batch_states, batch_actions in dataloader:
                predicted_actions = self.policy(batch_states)
                loss = nn.MSELoss()(predicted_actions, batch_actions)
                
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                
                total_loss += loss.item()
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss / len(dataloader):.4f}")
```

### Dataset Aggregation (DAgger)

Iterative improvement with expert feedback:

```python
class DAgger:
    def __init__(self, policy, expert, env):
        self.policy = policy
        self.expert = expert
        self.env = env
        self.dataset_states = []
        self.dataset_actions = []
    
    def collect_rollout(self):
        """Collect trajectory using current policy"""
        state = self.env.reset()
        states = [state]
        
        for _ in range(100):
            action = self.policy.select_action(state)
            next_state, reward, done, _ = self.env.step(action)
            states.append(next_state)
            state = next_state
            
            if done:
                break
        
        return states
    
    def query_expert(self, states):
        """Get expert actions for collected states"""
        expert_actions = [self.expert.get_action(state) for state in states]
        return expert_actions
    
    def train(self, n_iterations=10, rollouts_per_iter=5):
        for iteration in range(n_iterations):
            # Collect states using current policy
            new_states = []
            for _ in range(rollouts_per_iter):
                states = self.collect_rollout()
                new_states.extend(states)
            
            # Query expert
            expert_actions = self.query_expert(new_states)
            
            # Aggregate dataset
            self.dataset_states.extend(new_states)
            self.dataset_actions.extend(expert_actions)
            
            # Train on aggregated dataset
            self.policy.train(
                self.dataset_states,
                self.dataset_actions,
                n_epochs=50
            )
            
            print(f"Iteration {iteration + 1} complete. Dataset size: {len(self.dataset_states)}")
```

## Sim-to-Real Transfer

### Domain Randomization

Train with varied simulation parameters:

```python
class DomainRandomization:
    def __init__(self, env, param_ranges):
        self.env = env
        self.param_ranges = param_ranges  # Dict of (min, max) for each parameter
    
    def randomize(self):
        """Randomize environment parameters"""
        for param_name, (min_val, max_val) in self.param_ranges.items():
            value = np.random.uniform(min_val, max_val)
            self.env.set_parameter(param_name, value)
    
    def train_with_randomization(self, agent, n_episodes=1000):
        for episode in range(n_episodes):
            # Randomize at start of each episode
            self.randomize()
            
            state = self.env.reset()
            total_reward = 0
            
            for step in range(1000):
                action = agent.select_action(state)
                next_state, reward, done, _ = self.env.step(action)
                agent.replay_buffer.add(state, action, reward, next_state, done)
                
                state = next_state
                total_reward += reward
                
                agent.train_step()
                
                if done:
                    break
            
            if episode % 100 == 0:
                print(f"Episode {episode}, Reward: {total_reward}")
```

## Summary

Machine learning, especially deep reinforcement learning, enables robots to learn complex behaviors through trial and error. Sim-to-real transfer techniques allow policies trained in simulation to work on real robots.
