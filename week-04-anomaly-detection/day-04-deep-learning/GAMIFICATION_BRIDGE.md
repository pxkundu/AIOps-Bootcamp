# 🧠 The Neural Link: Week 4 Day 4

> **System Alert:** Standard algorithms (ARIMA, Isolation Forest) have reached their limit. The complexity of the signal exceeds linear models. You must activate **The Neural Link**.

---

## 🎮 Phase 1: The Pre-Game (The Non-Linear Trap)

**Scenario:**
You are monitoring a complex biological server (or a chaotic microservice).
- It doesn't follow a simple trend ($y = mx+b$).
- It doesn't have a clean daily cycle (SARIMA fails).
- It has intricate patterns: "If A happens, then B happens 10 steps later, but only if C didn't happen."

**The Failure:**
Your ARIMA model predicts a straight line. Your Isolation Forest flags everything as noise.
You need a model with **Memory**.

**Your Inventory (Unlocked for Day 4):**
- 🧬 **The LSTM Cell:** A neuron that remembers the distant past (Long Short-Term Memory).
- 🪞 **The Autoencoder:** A neural network that learns to copy normal data. If it fails to copy something, that thing is an anomaly.

---

## 🎮 Phase 2: The Verification Game ("The Mirror Test")

**Objective:**
You must build an **Autoencoder** (The Mirror) to protect the core.

| Level | Due Date | The Threat | The Defense (Day 4 Skill) |
|-------|----------|-------------|------------------------|
| 1 | **The Wave** | Predict the next step of a complex sine wave. | **RNN / LSTM Forecasting** |
| 2 | **The Mirror** | Train a network to compress and reconstruct normal data. | **Autoencoder Training** |
| 3 | **The Crack** | Feed an anomaly into the Mirror. Measure the **Reconstruction Error**. If Error > Threshold, ALARM. | **Thresholding** |

**Win Condition:**
Run `python project/neural_test.py`.
The script will feed your model "Normal" heartbeats and "Arrhythmia" heartbeats.
Your model must silently reconstruct the normal ones but **shatter** (high error) on the arrhythmias.

**Reward:**
If you pass, you unlock **Day 5: Week 4 Capstone** (Building a complete AIOps Platform).

---

## 🚀 How to Start

1.  **Read:** The [Lecture Notes](lecture-notes.md) to understand LSTM gates and Autoencoder bottlenecks.
2.  **Equip:** Copy the Keras snippets from the [Cheat Sheet](cheatsheet.md).
3.  **Train:** Complete [Exercise 01](exercises/exercise-01-lstm-forecast.md) to predict the future.
4.  **Defend:** Build "The Predictive Maintenance System" in the [Project](project/README.md).
