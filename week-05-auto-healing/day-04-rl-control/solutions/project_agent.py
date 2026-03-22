# Solution for Project Agent: The Q-Learning Brain
# Week 5 Day 4

import numpy as np

class QLearningAgent:
    def __init__(self, action_size=3, state_size=(5, 10)):
        self.action_size = action_size # Down, Hold, Up
        self.state_size = state_size   # (Queue_Buckets, Server_Count)
        
        # Hyperparameters
        self.alpha = 0.1   # Learning Rate
        self.gamma = 0.95  # Discount Factor
        self.epsilon = 1.0 # Initial Exploration Rate
        self.epsilon_decay = 0.995 # Decay per episode
        self.epsilon_min = 0.01
        
        # Initialize Q-Table (5 x 10 x 3)
        self.q_table = np.zeros(self.state_size + (self.action_size,))
        
    def choose_action(self, state):
        """
        Epsilon-Greedy Strategy.
        state: tuple (q_bucket, s_idx)
        """
        # Explore (Random)
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
            
        # Exploit (Best Action)
        return np.argmax(self.q_table[state])
        
    def learn(self, state, action, reward, next_state):
        """
        Update Q-Table using Bellman Equation.
        """
        old_val = self.q_table[state + (action,)]
        next_max = np.max(self.q_table[next_state])
        
        # Q_new = Q_old + Alpha * (Reward + Gamma * MaxQ_next - Q_old)
        new_val = old_val + self.alpha * (reward + self.gamma * next_max - old_val)
        
        self.q_table[state + (action,)] = new_val
        
    def decay_epsilon(self):
        """Reduces exploration rate over time."""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def save(self, filename="q_table.npy"):
        np.save(filename, self.q_table)
        print(f"Model saved to {filename}")
        
    def load(self, filename="q_table.npy"):
        self.q_table = np.load(filename)
        self.epsilon = 0.0 # Turn off exploration for testing
        print(f"Model loaded from {filename}")
