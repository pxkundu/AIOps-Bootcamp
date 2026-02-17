# 🚦 The Gridlock: Week 5 Day 4

> **System Alert:** Your Webhooks (Day 3) are fast, but they are dumb. They scale up blindly and burn money. You need a **Brain**.

---

## 🎮 Phase 1: The Pre-Game (The Traffic Jam)

**Scenario:**
You manage a toll booth (Kubernetes Cluster).
- **08:00 AM:** Rush hour starts. Cars pile up.
- **Action:** You open 10 lanes manually. Traffic flows.
- **10:00 AM:** Rush hour ends. 10 lanes are open. You are paying 10 clerks.
- **Result:** You saved the traffic, but went bankrupt.

**The Lesson:**
Scaling is a **Trade-off**.
- Too few servers = Failures (Lost Revenue).
- Too many servers = Waste (Cloud Bill).
Rules (`if CPU > 80`) are rigid. **Reinforcement Learning** (RL) finds the perfect balance dynamically.

**Your Inventory (Unlocked for Day 4):**
- 🤖 **The Agent:** An AI that learns by trial and error.
- 🎲 **The Environment:** A simulation of your cloud cluster.
- 💰 **The Reward Function:** The scorecard (+Revenue -Cost).

---

## 🎮 Phase 2: The Verification Game ("The Self-Driving Autoscaler")

**Objective:**
We simulate a traffic wave (Load Pattern).
You must build an Agent that learns to add servers *before* gridlock happens, and remove them *after* it clears.

| Level | Controller | Strategy | Result |
|---|---|---|---|
| **1. The Human** | You press Up/Down keys. | Reactionary | ⚠️ Stressful |
| **2. The Bot** | Random Actions. | Chaos | ❌ Fails |
| **3. The Q-Learner** | Learns to predict demand. | Optimal | ✅ Profit |

**Win Condition:**
Run `python project/run_autoscaler.py`.
The RL Agent must achieve a **total reward > 500** over 1000 steps.
(Meaning it served traffic efficiently without wasting money).

**Reward:**
Unlocks **Day 5: Capstone** (The Self-Healing Loop).

---

## 🚀 How to Start

1.  **Study:** Read [Lecture Notes: RL for Ops](lecture-notes.md).
2.  **Equip:** Copy the Q-Table snippet from [Cheat Sheet](cheatsheet.md).
3.  **Practice:** Play the game manually in [Exercise 01](exercises/exercise-01-manual-control.md).
4.  **Train:** Build the Q-Learner in the [Project](project/README.md).
