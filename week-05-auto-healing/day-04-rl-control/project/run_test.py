import sys
import os
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from env import AutoscaleEnv
from agent import QLearningAgent

def test_agent():
    print("--- Running Self-Driving Autoscaler (Inference) ---")
    env = AutoscaleEnv()
    agent = QLearningAgent()
    
    if not agent.load("autoscaler_model.npy"):
        print("Error: No trained model found. Run `python run_training.py` first.")
        return

    state = env.reset()
    total_reward = 0
    done = False
    
    # Action labels
    actions = ["DOWN (-1)", "HOLD (0) ", "UP (+1)  "]
    
    print(f"{'Step':<5} | {'Queue':<5} | {'Servers':<7} | {'Action':<10} | {'Reward':<7}")
    print("-" * 50)
    
    while not done:
        # Choose best action (train=False)
        action = agent.choose_action(state, train=False)
        
        # Save old queue for display
        q_val = env.queue
        s_val = env.servers
        
        next_state, reward, done = env.step(action)
        
        print(f"{env.time_step:<5} | {int(q_val):<5} | {s_val:<7} | {actions[action]} | {reward:>6.1f}")
        
        state = next_state
        total_reward += reward
        # Slow down for visualization
        time.sleep(0.1)
        
    print("-" * 50)
    print(f"Total Test Reward: {total_reward:.1f}")

if __name__ == "__main__":
    test_agent()
