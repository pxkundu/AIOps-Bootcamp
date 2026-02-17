# Week 5 Day 4: Reinforcement Learning (RL) for Ops

> **Duration:** 8 hours | **Difficulty:** Advanced (Conceptually)  
> **Focus:** Self-Correction, Dynamic Thresholds, and Autonomous Control.

---

## 🤖 Part 1: Why Rules Fail

You wrote `if CPU > 80: Scale Up`.
- What if demand spikes instantly? You scale too late.
- What if the spike is just 1 second? You scale wastefully.
- What if a new instance costs $10 but losing a user costs $1?
*Rules don't calculate "Value". RL does.*

**Reinforcement Learning:** An Agent learns to maximize a **Reward** by taking **Actions** in an **Environment**.

---

## 🔄 Part 2: The RL Loop

1.  **Environment (The Cloud):** The thing taking requests.
2.  **State ($S_t$):** Current situation. "Queue=50, Servers=2".
3.  **Action ($A_t$):** Add Server (+1), Remove Server (-1), or Wait (0).
4.  **Reward ($R_t$):** Did that help?
    - Served Request: +10 pts.
    - Dropped Request (Queue Full): -100 pts.
    - Active Server: -5 pts (Cost).
5.  **Next State ($S_{t+1}$):** "Queue=10, Servers=3".

The Agent loops forever, trying to get the highest score.

---

## 🧠 Part 3: Q-Learning (The Brain)

How does it decide?
It keeps a **Cheat Sheet (Q-Table)**.
- Rows = States (e.g., Load Low, Load High).
- Columns = Actions (Scale Up, Scale Down).
- Cells = Expected Future Reward.

| State | Action: +1 | Action: -1 | Action: 0 |
|---|---|---|---|
| **Load High** | +50 (Good!) | -100 (Crash!) | -10 (Risky) |
| **Load Low** | -5 (Waste) | +20 (Save $) | +10 (Stable) |

**The Algorithm:**
1.  Initialize Table with 0s.
2.  **Explore:** Try random actions initially.
3.  **Update:** If Action $A$ led to a good Reward, increase $Q(S, A)$.
4.  **Exploit:** Once trained, always pick max $Q$ for current state.

Equation: $Q_{new} = Q_{old} + \alpha \times (Reward + \gamma \times MaxQ_{next} - Q_{old})$
- $\alpha$: Learning Rate (How fast we learn).
- $\gamma$: Discount Factor (Future vs Immediate reward).

---

## ⚠️ Part 4: Safety in Ops

**RL is destructive.** It learns by crashing.
- Do NOT run a raw RL agent in Production.
- **Sim-to-Real:** Train in a Simulator (Digital Twin), then deploy the frozen policy.
- **Constraints:** Hard-code safety limits (Min 1 Server, Max 10 Servers) regardless of what the AI wants.

---

## 🔗 Next Steps

1.  Copy the Q-Learning snippet from [Cheat Sheet](cheatsheet.md).
2.  Manually balance the load in [Exercise 01](exercises/exercise-01-manual-control.md).
3.  Let the AI learn in [Project](project/README.md).
