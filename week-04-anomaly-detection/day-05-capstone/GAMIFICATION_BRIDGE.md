# 🏙️ The Panopticon: Week 4 Capstone

> **System Alert:** The separate tools (Day 1-4) were just training. Now, the entire City is under attack. You must build **The Panopticon**—an all-seeing AIOps Platform.

---

## 🎮 Phase 1: The Pre-Game (Integration Hell)

**Scenario:**
You have a great ARIMA model (Day 2) script... on your laptop.
You have a great LSTM model (Day 4) script... in a notebook.
The Production System produces 10,000 logs/sec.
**How do you run your Python scripts against that stream?**

**The Challenge:**
1.  **Latency:** If detection takes > 1 minute, the server is already dead.
2.  **Scale:** You can't fit all data in RAM.
3.  **Drift:** The "Normal" changes every week.

**Your Inventory (Unlocked for Day 5):**
- 🏭 **The Pipeline:** Streaming data ingestion (Simulation).
- 🧠 **The Model Registry:** Hot-swapping models without downtime.
- 🚨 **The Alert Router:** Sending the *right* alert to the *right* human.

---

## 🎮 Phase 2: The Verification Game ("The 5-Front War")

**Objective:**
You launch your `panopticon.py`. We launch 5 different attacks against it simultaneously.

| Attack Vector | The Symptom | Required Defense |
|---|---|---|
| **1. The Slow Burn** | Disk usage creeps up 1% per hour. | **Trend Forecasting (ARIMA/Regression)** |
| **2. The Flash Crash** | CPU drops to 0 for 5 seconds. | **Point Anomaly (Isolation Forest)** |
| **3. The Night Raid** | High Traffic at 3 AM. | **Contextual Features + IF** |
| **4. The Heart Attack** | Sine wave rhythm breaks. | **LSTM Forecasting / AE** |
| **5. The Cooldown** | Temp rises but Fan speed drops. | **Multi-variate Autoencoder** |

**Win Condition:**
Run `python project/war_room.py`.
Your system must output correct alerts for at least **4 out of 5** attacks.
If you flag "Normal" behavior as an attack (False Positive), you lose points.

**Reward:**
Passing this Capstone completes the **Anomaly Detection Module**. You graduate to **Week 5: Automatic Remediation (Self-Healing Systems)**.

---

## 🚀 How to Start

1.  **Design:** Read [Lecture Notes: AIOps Architecture](lecture-notes.md).
2.  **Build:** Implement the `Panopticon` class in `project/main.py`.
3.  **Integrate:** Import your models from previous days.
4.  **Battle:** Run the simulation.
