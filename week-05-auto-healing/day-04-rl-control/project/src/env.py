import numpy as np

class AutoscaleEnv:
    """
    A simulated cloud environment for an autoscaling Reinforcement Learning agent.
    
    State: (Queue_Bucket, Server_Count)
    Action: 0 (Scale Down), 1 (Hold), 2 (Scale Up)
    """
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
        Executes one step in the environment.
        """
        # 1. Apply Action
        if action == 0: # Down
            self.servers = max(1, self.servers - 1)
        elif action == 2: # Up
            self.servers = min(self.max_servers, self.servers + 1)
            
        # 2. Simulate Traffic (Sine Wave + Noise)
        # 24-hour cycle over 100 simulation steps
        hour = (self.time_step % 24)
        base_load = 10 + 20 * np.sin(2 * np.pi * hour / 24)
        base_load = max(0, base_load)
        arrival = np.random.poisson(base_load)
        
        # 3. Processing Logic
        capacity = self.servers * self.capacity_per_server
        total_available = self.queue + arrival
        served = min(total_available, capacity)
        self.queue = max(0, total_available - served)
        
        # 4. Reward Engineering
        # +1 revenue per served request
        # -0.5 cost per active server
        # -2.0 penalty per request waiting in queue
        reward = (served * 1.0) - (self.servers * 0.5) - (self.queue * 2.0)
        
        # Stability penalty for unnecessary scaling
        if action != 1:
            reward -= 0.1
            
        self.time_step += 1
        done = self.time_step >= 100 # Episode length
        
        return self._get_state(), reward, done
        
    def _get_state(self):
        # Discretize queue into 5 buckets for the Q-Table
        # 0: 0-10, 1: 10-20, 2: 20-30, 3: 30-40, 4: 40+
        q_bucket = min(4, int(self.queue / 10))
        # Server Index: 0-9 (for 1-10 servers)
        s_idx = self.servers - 1
        return (q_bucket, s_idx)
