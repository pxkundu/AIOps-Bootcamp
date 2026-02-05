# Day 1 Project: The Capacity Planner

> **Challenge:** A startup's server is getting busier every day. Analyzing the past 30 days of data, predict **exactly what date** the server will hit 100% CPU usage and crash.

---

## 🎯 Objective
Use **Time Series Decomposition** and **Linear Regression on Trends** to forecast a "Time to Failure" (TTF).

**Why not just use Week 3 Regression?**
Because the raw data has daily cycles (high at noon, low at night). If you predict based on "noon" data, you'll think the server is crashing tomorrow. If you use "night" data, you'll think it's fine forever. You need to extract the **Core Trend** first.

---

## 📂 Project Structure

```
capacity-planner/
├── data/
│   ├── generator.py    # Create the workload dataset
│   └── usage_logs.csv  # The data
├── src/
│   ├── analyze.py      # Your decomposition logic
│   └── forecast.py     # Your prediction logic
└── README.md
```

## 🛠️ Step 1: Generate Data (`generator.py`)

Create a script that generates 60 days of data with:
- **Trend:** `y = 0.0005 * t + 30` (Starts at 30%, grows slowly).
- **Season:** Daily spikes.
- **Noise:** Random variance.
- **Crash Point:** The trend should hit 100% around Day 90.

## 🛠️ Step 2: Extract the Trend (`analyze.py`)
1. Load `usage_logs.csv`.
2. Resample to `1H` (Hourly) to reduce noise.
3. Use `seasonal_decompose` to separate the Trend component.
4. Save the Trend component to a new CSV (`trend_only.csv`).

## 🛠️ Step 3: Forecast the Crash (`forecast.py`)
1. Load `trend_only.csv`.
2. Fit a **Linear Regression** model ($y = mx + b$) on just the Trend data.
   - $X$ = Timestamp (converted to integer or ordinal).
   - $y$ = Trend Value.
3. Solve for $y = 100$.
   - Calculate the timestamp where the line hits 100.
4. Print the **Predicted Crash Date**.

## 📊 Evaluation
- **Visual:** Plot the Raw Data, the Extracted Trend, and your Forecast Line extending into the future.
- **Accuracy:** If your generator trend is `0.0005*t + 30`, the crash is at `t = (100-30)/0.0005`. Compare your calculated date with the theoretical truth.

## 🚀 Bonus Challenge
What if the trend isn't Linear (Straight line), but **Exponential** (Viral growth)?
- Try generating data with `y = 30 * e^(0.01*t)`.
- Use a Log Transformation (`np.log(y)`) before fitting the Linear Regression to linearize it.
