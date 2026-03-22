import sys
import os
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from env import AutoscaleEnv
from agent import QLearningAgent

def main():
    print("--- Training the Self-Driving Autoscaler ---")
    env = AutoscaleEnv()
    agent = QLearningAgent()
    
    episodes = 1000
    all_rewards = []
    
    for ep in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.learn(state, action, reward, next_state)
            
            state = next_state
            total_reward += reward
            
        agent.decay_epsilon()
        all_rewards.append(total_reward)
        
        if (ep + 1) % 100 == 0:
            avg = np.mean(all_rewards[-100:])
            print(f"Episode {ep+1}/{episodes} | Avg Reward: {avg:.1f} | Epsilon: {agent.epsilon:.2f}")
            
    print("\nTraining Complete.")
    agent.save("autoscaler_model.npy")
    print("Run `python run_test.py` to see the results.")

if __name__ == "__main__":
    main()
