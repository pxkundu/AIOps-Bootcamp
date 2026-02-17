# Week 5 Day 4 Project: The Self-Driving Autoscaler 🚗

> **Challenge:** You are tasked with managing a global web service. Traffic follows a Day/Night cycle. Can you train an AI to scale resources perfectly without human intervention?

---

## 🎯 Objective
Build a Reinforcement Learning Agent that:
1.  **Learns** the optimal scaling policy by interacting with a simulation.
2.  **Balances** Cost vs Performance (SLA).
3.  **Adapts** to changing traffic patterns (Sine Wave).

---

## 📂 Project Structure

```
autoscaler/
├── src/
│   ├── env.py          # The Cloud Environment (Simulation)
│   ├── agent.py        # The Q-Learning Logic
│   └── run_training.py # The Training Loop (1000 Episodes)
└── README.md
```

## 🛠️ Step 1: The Environment (`src/env.py`)

Create a class `AutoscaleEnv` with:
- **State:** `(Queue_Level, Active_Servers)`
    - `Queue_Level`: Discretize queue length into 5 buckets (0-10, 10-20, ... , >50).
    - `Active_Servers`: 1 to 10.
- **Actions:** 0 (Scale Down), 1 (Hold), 2 (Scale Up).
- **Reward Function:**
    - `+1` per request served.
    - `-0.5` per active server (Cost).
    - `-2.0` per dropped request (if Queue > 50).
    - `-0.1` stability penalty (for changing servers too often).

## 🛠️ Step 2: The Agent (`src/agent.py`)

Implementation of Q-Learning with Epsilon-Greedy strategy.
- `choose_action(state)`
- `update(state, action, reward, next_state)`
- `save(filename)` and `load(filename)`

## 🛠️ Step 3: Training Loop (`src/run_training.py`)

Run for 1,000 "Days" (Episodes).
- Initially `epsilon = 1.0` (Full Random).
- Use `epsilon_decay = 0.995` per episode. By Episode 500, it should be exploiting.
- Plot `Total Reward` over episodes. It should define an upward curve.

## 🚀 Twist: Flash Crowd!
After training, simulate a "Black Friday" event (Traffic x5).
Does your trained agent handle it? (It should scale to Max Servers immediately).
Run a test script `run_test.py` to verify this behavior.

## 📝 Deliverable
A plot showing Reward increasing over training episodes.
A final "Run" output showing the agent scaling up/down perfectly with the Sine Wave traffic.
