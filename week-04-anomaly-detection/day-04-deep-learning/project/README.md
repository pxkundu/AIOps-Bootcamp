# Day 4 Project: The Predictive Maintenance System 🏭

> **Challenge:** You are monitoring a mission-critical turbine ($10M asset). Detecting failure *after* it explodes is useless. You must predict failure by detecting subtle shifts in sensor patterns **hours before** the crash.

---

## 🎯 Objective
Use an **LSTM Autoencoder** to monitor multi-variate sensor data (Vibration, Temperature) and flag anomalies *before* catastrophic failure.

**Why Deep Learning?**
Simple thresholds (Temp > 100°C) miss the "Vibration rising *while* Temperature is falling" correlation. An Autoencoder learns the complex *relationship* between sensors.

---

## 📂 Project Structure

```
predictive-maintenance/
├── data/
│   ├── bearing_sim.py   # Generates sensor data (Normal -> Degrading -> Failure)
│   └── sensor_logs.csv  # The dataset
├── src/
│   ├── train_ae.py      # Train Autoencoder on Normal data
│   ├── detect.py        # Streaming anomaly detection
│   └── visualize.py     # Plot Reconstruction Error vs Time
└── README.md
```

## 🛠️ Step 1: Simulate Degradation (`bearing_sim.py`)

Create a script that generates 10,000 timestamps for 4 sensors:
1.  **Vibration:** Normal (Gaussian, mean=0, std=1). Degrading (std increases to 5).
2.  **Temperature:** Normal (Sine wave around 50°C). Degrading (Drifts up to 90°C).
3.  **Power:** Correlated with Temp.
4.  **Rotation:** Constant, then erratic.

Timeline:
- **0-6000 steps:** Healthy. (Train on this).
- **6000-8000 steps:** Early Degradation. (Test recall here).
- **8000-10000 steps:** Critical Failure. (Must detect way before this).

## 🛠️ Step 2: The Autoencoder (`train_ae.py`)

1.  Load `sensor_logs.csv`.
2.  **Split:** Use only the first 6000 steps (Healthy) for training.
3.  **Scale:** `MinMaxScaler` is mandatory.
4.  **Reshape:** Create sliding windows (e.g., `window_size=50`).
5.  **Train:** LSTM Autoencoder to minimize `MSE(Input, Output)`.
6.  **Save:** The model and the Threshold (e.g., Max Train MAE).

## 🛠️ Step 3: Deployment (`detect.py`)

1.  Load the saved model.
2.  Feed the full 10,000 steps.
3.  Calculate `Reconstruction Error` for each window.
4.  **Alert:** If Error > Threshold, flag as Anomaly.
5.  **Root Cause Analysis:** Which sensor contributed most to the error? (Advanced)

## 📊 Evaluation
- **Visual:** Plot the "Anomaly Score" over time.
- **Metric:** `Time-to-Detection`. How early did you catch the degradation? (Ideally around step 6100).

## 🚀 Twist: False Alarms
Add random noise spikes (sensor glitches) to the healthy data. Ensure your Autoencoder is robust (doesn't panic on single spikes) but catches sustained degradation.
