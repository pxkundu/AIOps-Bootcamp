# Remediation Cheat Sheet: Q-Learning

> **Libraries:** `numpy`, `random`  
> **Concept:** Bellman Equation, Q-Tables

---

## 🎲 The Q-Learning Template

This is the standard algorithm for discrete problems (e.g., Autoscaling: +1, -1, 0).

```python
import numpy as np

# 1. Initialize Q-Table
# Rows = Number of States (e.g., 10 Load Levels)
# Columns = Number of Actions (3: -1, 0, +1)
Q_table = np.zeros((10, 3))

# Hyperparameters
alpha = 0.1   # Learning Rate (How fast overrides old)
gamma = 0.9   # Discount Factor (Cares about future via Next State)
epsilon = 0.1 # Exploration Rate (10% random moves)

def choose_action(state):
    """
    Epsilon-Greedy Strategy:
    Sometimes explore (random), usually exploit (best known).
    """
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice([0, 1, 2]) # Random Action
    else:
        return np.argmax(Q_table[state])   # Best Action

def update_q_table(state, action, reward, next_state):
    """
    Bellman Equation:
    NewQ = OldQ + LearnRate * (Reward + Discount * MaxNextQ - OldQ)
    """
    old_value = Q_table[state, action]
    next_max = np.max(Q_table[next_state])
    
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    Q_table[state, action] = new_value
```

---

## 🌍 Building a Custom Environment (Gym Style)

To train an agent, you need a simulation. Standard interface:

```python
class CloudEnv:
    def __init__(self):
        self.servers = 1
        self.queue = 0
        
    def step(self, action):
        """
        Takes action, advances time step.
        Returns: next_state, reward, done
        """
        # Apply Action
        if action == 0: change = -1
        elif action == 1: change = 0
        elif action == 2: change = 1
        
        self.servers = max(1, min(10, self.servers + change))
        
        # Simulate Traffic (Stochastic)
        arrival = np.random.poisson(5) # 5 requests/sec
        capacity = self.servers * 2    # Each server handles 2 req/sec
        
        served = min(self.queue + arrival, capacity)
        self.queue = max(0, self.queue + arrival - served)
        
        # Calculate Reward
        # Reward = +Served - Cost - Penalty(Queue)
        reward = served * 1.0 - (self.servers * 0.5) - (self.queue * 2.0)
        
        # State: Quantize queue length (0-9)
        state = min(9, self.queue)
        
        return state, reward, False # Never 'Done' unless crashed
```

---

## 💡 Troubleshooting

| Problem | Cause |
|---|---|
| **Agent does nothing** | Learning Rate too low? Epsilon too low (stuck in local init)? |
| **Agent oscillates** | Reward for Action (+1 / -1) cancels out. Penalize instability (-0.1 for changing). |
| **Exploding Q-Values** | Normal. Q-Values represent *total future reward*. If infinite horizon, normalize or use small gamma (< 1). |
