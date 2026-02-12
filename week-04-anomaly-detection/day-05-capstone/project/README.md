# Week 4 Capstone: The Panopticon Platform 🏙️

> **Challenge:** Build a unified AIOps Platform that monitors a production environment in real-time. Detect anomalies across Trend, Point, Context, and Pattern layers simultaneously.

---

## 🎯 Objective
Integrate ARIMA, Isolation Forest, and LSTM (or similar) into a single Python class `Panopticon` that can:
1.  Train on historical data.
2.  Serve predictions in < 10ms per request.
3.  Correlate alerts to reduce noise.

---

## 📂 Project Structure

```
panopticon/
├── data/
│   ├── generator.py     # Creates training history + live attack stream
│   └── history.csv      # The "Normal" baseline (last 30 days)
├── src/
│   ├── panopticon.py    # The Main Class (Your Code)
│   ├── models.py        # Wrapper classes for ARIMA/IF/LSTM
│   └── utils.py         # Feature Engineering (Hour, Day, Diff)
└── README.md
```

## 🛠️ Step 1: The Simulator (`generator.py`)

Create a script that outputs:
- **History:** 30 days of metrics (CPU, Memory, Latency) at 1-min intervals.
    - Day/Night cycle + Linear Trend + Noise.
- **Live Stream:** An iterator that yields new metrics one by one.
    - Inject 5 types of attacks (Slow Burn, Flash Crash, etc.) randomly.

## 🛠️ Step 2: The Panopticon Class (`panopticon.py`)

```python
class Panopticon:
    def __init__(self):
        self.trend_model = ... # e.g. Linear Regression or ARIMA
        self.point_model = ... # Isolation Forest
        self.pattern_model = ... # LSTM or Autoencoder
        
    def train(self, history_df):
        # 1. Feature Engineering (Add 'hour', 'diff')
        # 2. Train Trend Model (on 'cpu')
        # 3. Train Point Model (on ['cpu', 'mem', 'lat'])
        # 4. Train Pattern Model (on sequences)
        print("System Armed.")

    def detect(self, live_data_point):
        # returns dict: {'is_anomaly': Bool, 'severity': Int, 'cause': Str}
        ...
```

## 🛠️ Step 3: The Integration

1.  **Trend Check:** Is current value > predicted trend? (Catch Slow Burn).
2.  **Point Check:** Is Isolation Forest score < -0.5? (Catch Flash Crash).
3.  **Pattern Check:** Is Reconstruction Error > Threshold? (Catch complex failures).
4.  **Vote:** If 2 models trigger, Severity = HIGH. If 1, Severity = LOW.

## 📊 The War Room (`test_war_room.py`)

I have provided a testing script. It will import your `Panopticon`, train it, and then bombard it with 100 live events (5 attacks hidden inside).
- **Score:** +1 for correct detection. -1 for False Positive.
- **Goal:** Score > 3.

## 🚀 Bonus: Explainability
When you alert, output *why*: "Anomaly detected: CPU is 90% (Point Model) but expected 40% (Trend Model)". This context is gold for SREs.
