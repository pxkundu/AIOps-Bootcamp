# Week 4 Day 5: AIOps Capstone - Production Architecture

> **Duration:** 8 hours | **Difficulty:** Expert (Integration)
> **Focus:** Putting it all together. Scalable, low-latency Anomaly Detection.

---

## 🏗️ Part 1: The Batch vs Streaming Dilemma

You have 5 models (ARIMA, IF, LOF, LSTM, AE). How do you run them?

| Type | Example | When to Run | Latency | Tool |
|---|---|---|---|---|
| **Batch (Forecast)** | ARIMA (Disk Usage) | Once/Day (Midnight) | High (Mins) | Airflow / Cron + Pandas |
| **Stream (Detect)** | Isolation Forest (DDoS) | Every Event | Low (<50ms) | Flink / Kafka Streams / API |
| **Near-Realtime** | Autoencoder (Vibration) | As Micro-batches (1 min) | Medium (secs) | Spark Streaming |

**Golden Rule:** Train in Batch (Offline). Predict in Stream (Online).

---

## 🏭 Part 2: The Architecture Pattern

```mermaid
graph TD
    A[Log/Metric Stream] --> B{Stream Processor}
    B -->|Fast Path| C[Inference Engine .pkl]
    B -->|Slow Path| D[Data Lake / DB]
    
    D --> E[Training Job (Weekly)]
    E --> F[Model Registry (S3/MLflow)]
    F -->|Hot Swap| C
    
    C --> G{Anomaly Score > Threshold?}
    G -->|Yes| H[Alert Manager]
    G -->|No| I[Ignore]
```

### 1. The Training Job
- Runs every night/week.
- Loads 30 days of history.
- Trains `IsolationForest` or `LSTM`.
- Validates accuracy (Backtesting).
- Saves `model_v2.pkl`.

### 2. The Inference Engine
- A lightweight API (FastAPI) or Stream Consumer.
- Loads `model_v2.pkl` into RAM on startup.
- Receives `{"cpu": 90, "mem": 40}`.
- Returns `{"anomaly": True, "score": -0.8}`.
- **Latency Requirement:** < 50ms. (Use `scikit-learn-intelex` or ONNX for speed).

---

## 🚨 Part 3: Alert Fatigue & Correlation

If your `LSTM` flags an anomaly every minute, SREs will mute you.
**You must suppress noise.**

1.  **Time-based Deduplication:** If alert sent at 10:00, don't send again until 10:30.
2.  **Correlated Alerts:** If `CPU High` and `Latency High` trigger at the same time, send **1 Alert** ("Database Overload"), not 2 separate ones.
3.  **Severity Levels:**
    - `Score > 0.9`: P1 (Page Human).
    - `Score > 0.7`: P3 (Log Ticket).

---

## 📉 Part 4: Handling Concept Drift

The definition of "Normal" changes.
- **Sudden Drift:** Black Friday traffic. (Model panics).
- **Gradual Drift:** Userbase grows 1% per week. (Model degrades slowly).

**Solution:**
- **Retrain Frequency:** Weekly is standard.
- **Shadow Mode:** Run `model_v2` silently alongside `model_v1`. Only promote v2 if it performs better than v1 on live data.

---

<p align="center">
  <a href="../day-04-deep-learning/lecture-notes.md">⬅️ Back: Day 4</a> | <strong>Day 5: Capstone Project</strong> | <a href="../../week-05-remediation/README.md">Begin Week 5 ➡️</a>
</p>
