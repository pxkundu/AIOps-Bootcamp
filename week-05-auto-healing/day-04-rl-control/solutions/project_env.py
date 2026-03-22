# Solution for Project Environment: The Cloud Simulation
# Week 5 Day 4

import numpy as np

class AutoscaleEnv:
    def __init__(self):
        self.max_servers = 10
        self.capacity_per_server = 5
        self.reset()
        
    def reset(self):
        self.servers = 1
        self.queue = 0
        self.time_step = 0
        return self._get_state()
        
    def step(self, action):
        """
        Action: 0=Down, 1=Hold, 2=Up
        """
        # 1. Apply Scaling Action (takes effect next step)
        if action == 0:
            self.servers = max(1, self.servers - 1)
        elif action == 2:
            self.servers = min(self.max_servers, self.servers + 1)
            
        # 2. Simulate Traffic (Sine Wave + Noise)
        # Hour of Day (0-23 cycle over 100 steps)
        hour = (self.time_step % 24)
        base_load = 10 + 20 * np.sin(2 * np.pi * hour / 24) # Peak at 12
        base_load = max(0, base_load)
        arrival = np.random.poisson(base_load)
        
        # 3. Serve Requests
        capacity = self.servers * self.capacity_per_server
        served = min(self.queue + arrival, capacity)
        self.queue = max(0, self.queue + arrival - served)
        
        # 4. Calculate Reward
        # Minimize Queue, Minimize Servers, Maximize Served
        # Weighting is tricky. Let's try:
        # +1 per served
        # -0.5 per server (Cost)
        # -2.0 per queued (Penalty)
        reward = served * 1.0 - (self.servers * 0.5) - (self.queue * 2.0)
        
        # Stability Penalty (small) for changing servers
        if action != 1:
            reward -= 0.1
            
        self.time_step += 1
        done = self.time_step >= 100 # End episode after 100 ticks
        
        return self._get_state(), reward, done
        
    def _get_state(self):
        # Discretize Queue into 5 buckets: 0-10, 10-20, 20-30, 30-40, >40
        q_bucket = min(4, int(self.queue / 10))
        # Server Index: 0-9 (for 1-10 servers)
        s_idx = self.servers - 1
        return (q_bucket, s_idx)
