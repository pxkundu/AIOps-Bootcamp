# Solution for Project Training Loop
# Week 5 Day 4

import numpy as np
from project_env import AutoscaleEnv
from project_agent import QLearningAgent

def train_agent():
    env = AutoscaleEnv()
    agent = QLearningAgent()
    
    print("Training started (1000 Episodes)...")
    rewards = []
    
    for episode in range(1000):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            # 1. Choose Action
            action = agent.choose_action(state)
            
            # 2. Step Environment
            next_state, reward, done = env.step(action)
            
            # 3. Learn
            agent.learn(state, action, reward, next_state)
            
            state = next_state
            total_reward += reward
            
        # Decay exploration
        agent.decay_epsilon()
        rewards.append(total_reward)
        
        if (episode + 1) % 100 == 0:
            avg_rew = np.mean(rewards[-100:])
            print(f"Episode {episode+1}/1000 | Reward: {avg_rew:.1f} | Epsilon: {agent.epsilon:.2f}")
            
    print("Training complete.")
    agent.save("autoscaler_model.npy")
    
    # Optional: Plotting
    try:
        import matplotlib.pyplot as plt
        plt.plot(rewards)
        plt.title("Q-Learning Training Progress")
        plt.xlabel("Episode")
        plt.ylabel("Total Reward")
        plt.show()
    except ImportError:
        pass

if __name__ == "__main__":
    train_agent()
