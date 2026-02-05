# ⏳ The Temporal Bridge: Entering Week 4

> **System Alert:** You are leaving the realm of *Static Predictions* (Week 3) and entering the volatile **Temporal Domain** (Week 4). Your previous tools may not work here.

---

## 🎮 Phase 1: The Pre-Game (The Naive Predictor's Trap)

**Scenario:**
The Chief SRE hands you a dataset of CPU usage for the last 30 days.
*"The logic is simple,"* she says. *"If CPU was high yesterday, it will be high today. Just train a Random Forest on the raw numbers."*

**The Challenge:**
1. You try to predict tomorrow's load using standard Week 3 regression.
2. **The Failure:** Your model predicts a flat line. It fails to catch the "Morning Spike" and the "Weekend Drop."
3. **The realization:** You cannot shuffle time. $T_1$ depends on $T_0$.

**Your Inventory (Unlocked for Day 1):**
- 🗝️ **The Pandas Calendar:** Ability to manipulate time indices.
- 🔭 **The Decomposer:** Ability to split signal into Trend + Season + Noise.
- 📉 **The Stationarity Shield:** Ability to make chaotic data predictable.

---

## 🎮 Phase 2: The Verification Game (The Time Fixer)

After completing Day 1's content, you must play **"The Time Fixer"**.

**Objective:**
You are presented with 5 broken timelines. You must diagnose and fix them.

| Level | The Glitch | Symptom | The Fix (Day 1 Skill) |
|-------|------------|---------|-----------------------|
| 1 | **The Jitter** | Data arrives at random intervals (1s, 5s, 10s). | **Resample** to uniform frequency (1min). |
| 2 | **The Void** | Missing chunks of data at night. | **Interpolate** (Linear vs Time). |
| 3 | **The Drift** | Mean value keeps increasing mathematically. | **Difference** $(\Delta y)$ to make it Stationary. |
| 4 | **The Ghost** | A periodic spike happens every 24h. | extract **Seasonality** via STL Decomposition. |
| 5 | **The Rolling Fog** | Data is too noisy to see the trend. | Apply **Rolling Window** smoothing. |

**Win Condition:**
Run `python project/time_fixer.py`. If you successfully stabilize all 5 streams, you unlock **Day 2: ARIMA & Forecasting**.

---

## 🚀 How to Start

1. **Fail First:** Run `exercises/00_why_ml_fails.py` to see why simple regression breaks.
2. **Learn:** Study the [Lecture Notes](lecture-notes.md) to acquire the "Time" skill tree.
3. **Win:** Complete the **Capacity Planning Project**.
