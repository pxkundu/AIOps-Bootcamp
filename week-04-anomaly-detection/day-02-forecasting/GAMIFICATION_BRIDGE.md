# 🔮 The Oracle's Gate: Week 4 Day 2

> **System Alert:** You have mastered the flow of time (Day 1). Now you must learn to **see what comes next.**

---

## 🎮 Phase 1: The Pre-Game (The Chaos Engine)

**Scenario:**
The Oracle presents you with a chaotic signal `x(t)`.
*"Tell me x(t+1),"* she demands.

You try to guess. You fail.
*"You are looking at the noise,"* she says. *"You must listen to the Echoes (Auto-Regression) and the Shockwaves (Moving Average)."*

**Your Inventory (Unlocked for Day 2):**
- 🎻 **The AR Violin:** Tune it to resonate with past values ($p$).
- 🌊 **The Integration Bridge:** Smooth out rough trends ($d$).
- 🔔 **The MA Bell:** Dampen recent shocks ($q$).

---

## 🎮 Phase 2: The Verification Game ("Predict or Perish")

**Objective:**
You are given 3 corrupted timelines. You must build an **ARIMA** model to fill in the future 10 steps.

| Level | Due Date | The Symptom | The Tool (Day 2 Skill) |
|-------|----------|-------------|------------------------|
| 1 | **Tomorrow** | Data depends heavily on yesterday's value. | **AR(1) Model** |
| 2 | **Next Week** | There is a strong upward trend. | **Differencing (d=1)** |
| 3 | **Next Month** | Data reacts to random shocks today, then stabilizes. | **MA(1) Model** |
| 4 | **Boss** | A 7-day seasonal pattern overrides everything. | **SARIMA (Seasonal)** |

**Win Condition:**
Run `python project/oracle_test.py`.
The script will hide the last 10 data points. Your model must predict them with **MAPE < 10%**.

**Reward:**
If you pass, you unlock **Day 3: Anomaly Detection Algorithms** (Isolation Forest, AutoEncoders).

---

## 🚀 How to Start

1.  **Read:** The [Lecture Notes](lecture-notes.md) on how to choose p, d, q.
2.  **Practice:** Use the [Cheat Sheet](cheatsheet.md) to grid search parameters.
3.  **Conquer:** Build the "Budget Forecaster" in the main [Project](project/README.md).
