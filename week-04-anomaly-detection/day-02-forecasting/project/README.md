# Day 2 Project: The Budget Forecaster 💸

> **Challenge:** The CFO is panicking. AWS costs are rising. Predict the daily cloud bill for the next 30 days so we know if we'll bust the quarterly budget.

---

## 🎯 Objective
Build a **SARIMA** model to forecast daily cloud costs, capturing both the **Upward Trend** (team is launching more servers) and the **Weekly Cycle** (lower costs on weekends).

---

## 📂 Project Structure

```
budget-forecaster/
├── data/
│   ├── cost_generator.py # Creates the synthetic billing data
│   └── aws_costs.csv     # The dataset
├── src/
│   ├── tuning.py         # Script to find (p,d,q)
│   └── forecast.py       # Script to generate Future predictions
└── README.md
```

## 🛠️ Step 1: Generate Data (`cost_generator.py`)

Create a script that generates 365 days of billing data:
- **Baseline:** $1000/day.
- **Trend:** Grows by $5/day (Linear).
- **Seasonality:** Weekends dropped by 20% (Weekly cycle, period=7).
- **Noise:** Random variance of $50.

## 🛠️ Step 2: The Grid Search (`tuning.py`)

Use `pmdarima.auto_arima` or a manual loop to find the best parameters.
**Hint:** Since there is a weekly cycle, you must set `m=7` (Seasonality period).

Expected outcome:
- Order: $(p, 1, q)$ (Needs differencing for the trend)
- Seasonal Order: $(P, D, Q, 7)$

## 🛠️ Step 3: The Forecast (`forecast.py`)

1. Load data.
2. Train the SARIMA model with the best params found.
3. Forecast the next 30 days.
4. Calculate the **Total Predicted Bill** for next month (Sum of the 30 days).

## 📊 Evaluation
- Split the last 30 days of available data as a "Test Set".
- Train on Days 1-335.
- Forecast Days 336-365.
- Compare with actuals using **MAPE**.
- **Goal:** MAPE < 5%.

## 🚀 Twist: Sudden Spikes
Modify the generator to add a "Black Friday" spike. Does ARIMA catch it? Or does it smooth it out? This teaches the limitation of ARIMA vs Anomaly Detection.
