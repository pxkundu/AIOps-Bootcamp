# 🛡️ The Guardian's Watch: Week 4 Day 3

> **System Alert:** The Oracle (Day 2) showed you the future. Now, intruders are manipulating the present. You must become **The Guardian**.

---

## 🎮 Phase 1: The Pre-Game (The Invisible Enemy)

**Scenario:**
You are monitoring a secure server.
- Traffic holds steady at 100 req/sec.
- Suddenly, it drops to 0. (Easy to catch).
- But then... it sends 100 req/sec at 3:00 AM (When it should be 0).
- Or... 100 requests arrive, but they are all 100ms slower than usual.

**The Failure:**
Your Dashboard (Threshold Alert `if CPU > 90%`) is silent. The enemy is inside, staying *under* the radar.

**Your Inventory (Unlocked for Day 3):**
- 🌲 **The Isolation Forest:** Traps anomalies by cutting them off from the herd.
- ⭕ **The One-Class SVM:** Draws a tight circle around "Normal." Anything outside is hostile.
- 🏘️ **Local Outlier Factor (LOF):** Compares a point's density to its neighbors.

---

## 🎮 Phase 2: The Verification Game ("The Three Intruders")

**Objective:**
Three attackers are trying to breach the system. You must deploy the correct algorithm to catch them.

| Level | Due Date | The Threat (Anomaly Type) | The Tool (Day 3 Skill) |
|-------|----------|-------------|------------------------|
| 1 | **The Spy** | A single data point is way off-scale (e.g., Latency=5000ms). | **Isolation Forest** |
| 2 | **The Sleeper** | A value is normal globally (e.g., CPU=50%) but abnormal *for this time of day*. | **Contextual Feature Engineering** |
| 3 | **The Swarm** | A cluster of points are slightly odd (Density drop). | **Local Outlier Factor (LOF)** |

**Win Condition:**
Run `python project/guardian_test.py`.
The script simulates the attacks. Your `def detect_intruder(data)` function must catch >95% of them.

**Reward:**
If you pass, you unlock **Day 4: Deep Learning for Time Series** (LSTM & Autoencoders).

---

## 🚀 How to Start

1.  **Learn:** Study the [Lecture Notes](lecture-notes.md) to understand Density vs Isolation.
2.  **Equip:** Copy the snippets from the [Cheat Sheet](cheatsheet.md).
3.  **Train:** Complete [Exercise 01](exercises/exercise-01-isolation-forest.md) to build your first trap.
4.  **Defend:** Build "The Network Guardian" in the main [Project](project/README.md).
