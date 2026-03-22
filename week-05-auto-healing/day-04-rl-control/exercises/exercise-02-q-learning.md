# Exercise 02: The Q-Learning Agent (First Steps)

## 🎯 Objective
Replace your manual keyboard inputs with an **Intelligent Agent** that learns from its mistakes.

---

## 🛠️ Step 1: The Environment (`env.py`)

Create a class `CloudEnv` that simulates your cloud.
- **State:** `(Active_Servers, Queue_Length)`
- **Action:** `0 (Down), 1 (Hold), 2 (Up)`
- **Step Function:**
    - Increase/Decrease servers based on action.
    - Add random requests (Poisson).
    - Serve requests (Capacity = Servers * 5).
    - Calculate Reward:
        - `Served * 2.0` (Revenue)
        - `Servers * -0.5` (Cost)
        - `Queue * -1.0` (Penalty)
    - Return `next_state, reward, done`.

*(See Cheat Sheet for template)*

## 🛠️ Step 2: The Agent (`agent.py`)

1.  Initialize a Q-Table (`numpy.zeros((20, 3))`). 
    - Why 20? Maximum reasonable queue length (or 10 servers + 10 queue buckets).
    - Let's simplify state to `Queue Length (0-19)`. If queue > 19, clip to 19.
2.  Implement `choose_action(state)`: Epsilon-Greedy.
3.  Implement `update_q_table(state, action, reward, next_state)`.

## 🛠️ Step 3: Train It

Run a loop for 1000 episodes.
- Reset Environment (`queue=0, servers=1`).
- Loop `t=0 to 100`.
- Choose Action -> Step Env -> Update Q -> Next State.
- Every 100 episodes, print "Total Reward". It should go up!

## 📝 Deliverable
Run the training.
Does the Total Reward improve?
At the end, print the Q-Table row for `State=10` (High Queue).
What action has the highest value? (Should be Action 2: Scale Up).
