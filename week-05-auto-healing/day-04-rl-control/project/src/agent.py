import numpy as np
import os

class QLearningAgent:
    def __init__(self, action_size=3, state_size=(5, 10)):
        self.action_size = action_size 
        self.state_size = state_size   
        
        # Hyperparameters
        self.alpha = 0.1   # Learning Rate
        self.gamma = 0.95  # Discount Factor
        self.epsilon = 1.0 # Initial Exploration Rate
        self.epsilon_decay = 0.995 
        self.epsilon_min = 0.01
        
        # Q-Table: (QueueBuckets, ServerCount, Actions)
        self.q_table = np.zeros(self.state_size + (self.action_size,))
        
    def choose_action(self, state, train=True):
        """
        Epsilon-greedy selection.
        """
        if train and (np.random.rand() <= self.epsilon):
            return np.random.randint(self.action_size)
        return np.argmax(self.q_table[state])
        
    def learn(self, state, action, reward, next_state):
        """
        Q-Learning Update Rule.
        """
        old_val = self.q_table[state + (action,)]
        next_max = np.max(self.q_table[next_state])
        
        # New Q = Old Q + Alpha * (Reward + Gamma * MaxNextQ - Old Q)
        new_val = old_val + self.alpha * (reward + self.gamma * next_max - old_val)
        self.q_table[state + (action,)] = new_val
        
    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def save(self, filename="autoscaler_model.npy"):
        np.save(filename, self.q_table)
        print(f"Agent saved to {filename}")
        
    def load(self, filename="autoscaler_model.npy"):
        if os.path.exists(filename):
            self.q_table = np.load(filename)
            self.epsilon = self.epsilon_min
            print(f"Agent loaded from {filename}")
            return True
        return False
