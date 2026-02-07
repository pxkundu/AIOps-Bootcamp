# Day 3 Project: The Network Guardian 🛡️

> **Challenge:** You are the last line of defense. Hackers are launching subtle attacks (Port Scans, DDoS) against your servers. Build an **Unsupervised Anomaly Detection System** to catch them in real-time.

---

## 🎯 Objective
Use **Isolation Forest** and **Local Outlier Factor (LOF)** to detect malicious network traffic without using labeled data (Unsupervised Learning).

**Why Unsupervised?**
In reality, you don't have labeled "Attack" data. You only have "Normal" traffic (mostly). You need to detect *deviations*.

---

## 📂 Project Structure

```
network-guardian/
├── data/
│   ├── traffic_generator.py # Simulates normal web traffic + attacks
│   └── network_logs.csv     # The dataset
├── src/
│   ├── detect_if forest.py  # Isolation Forest model
│   ├── detect_lof.py        # Local Outlier Factor model
│   └── evaluate.py          # Precision/Recall curves
└── README.md
```

## 🛠️ Step 1: Simulated Traffic (`traffic_generator.py`)

Create a script that generates 10,000 requests with features:
- **Bytes Sent:** Normal ~ 500 bytes. Attack (Data Exfiltration) ~ 50,000 bytes.
- **Duration:** Normal ~ 0.1s. Attack (Slowloris) ~ 10s.
- **Source Port:** Normal = 80/443. Attack = random high ports.
- **Packets/Sec:** Normal ~ 10. Attack (DDoS) ~ 1000.

Inject 2% attacks. Save to CSV.

## 🛠️ Step 2: Isolation Forest (`detect_if.py`)

1. Load data.
2. Drop labels (pretend you don't know them).
3. Train `IsolationForest(contamination=0.02)`.
4. Predict anomalies (-1).
5. Compare predictions with actual labels (Ground Truth).

## 🛠️ Step 3: Local Outlier Factor (`detect_lof.py`)

1. Repeat with `LocalOutlierFactor(n_neighbors=20)`.
2. Does LOF catch different attacks than IF? (LOF is better for local density, IF for global outliers).

## 📊 Evaluation
- **Confusion Matrix:** How many attacks did you catch? (True Positives)
- **False Alarm Rate:** Did you block legitimate users? (False Positives)
- **Precision vs Recall:** Plot the curve.

## 🚀 Twist: Concept Drift
Modify the generator to increase normal traffic volume over time (Organic Growth).
- Does your model start flagging *everyone* as an attacker?
- How would you fix this? (Retraining? Sliding Window?)
