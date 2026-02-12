# 🛠️ Panopticon Setup Guide

> Follow these steps to deploy your Anomaly Detection Platform and enter The War Room.

---

## 1. Environment Setup

It is recommended to use a virtual environment.

```bash
# Create venv
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install Dependencies
pip install pandas numpy scikit-learn statsmodels matplotlib
```

## 2. Project Structure

Ensure your folder looks like this:

```
panopticon/
├── data/
│   └── generator.py      # Creates synthetic history
├── src/
│   ├── __init__.py
│   ├── models.py         # The brains (IF, Regression)
│   ├── panopticon.py     # The central controller
│   └── utils.py          # Feature engineering helpers
├── run_simulation.py     # The War Room runner
└── SETUP.md
```

## 3. Generate Data

Before training, we need 30 days of "Normal" server history.

```bash
# Run the generator
python -m src.data.generator
```
*Note: This might take a few seconds. It creates `data/history.csv`.*

## 4. Run the War Room

Launch the simulation. The system will:
1.  Train on `history.csv`.
2.  Start receiving 100 live events.
3.  Attempt to block 5 attacks.

```bash
python run_simulation.py
```

## 5. Expected Output

You should see something like:

```text
TRAINING PHASE...
  -> Point Model (IsolationForest) Trained.
  -> Trend Model (LinearRegression) Trained. Threshold: 92.5

LIVE BATTLE PHASE...
[ATTACK] Type: slow_burn | CPU: 95.0
  ✅ BLOCKED! System detected: Trend Anomaly (CPU > 92.5)

[ATTACK] Type: flash_crash | CPU: 0.0
  ✅ BLOCKED! System detected: Point Anomaly (CPU=0)

FINAL SCORE: 5/5
🏆 MISSION ACCOMPLISHED.
```
