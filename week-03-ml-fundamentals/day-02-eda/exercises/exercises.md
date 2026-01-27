# Exercise 01: The Imputation Lab (Healing Gaps)

## 🎯 Objective
Learn how to repair broken time-series data using different imputation strategies and understand the impact of each choice.

---

## 🛠️ Step 1: Create Corrupted Data
Run this script `make_gaps.py`:

```python
import pandas as pd
import numpy as np

# 1. Generate clean sine wave
time = pd.date_range("2024-01-01", periods=100, freq="H")
values = np.sin(np.linspace(0, 10, 100)) + 10

# 2. Inject Gaps (Simulate agent downtime)
df = pd.DataFrame({"timestamp": time, "cpu": values})
df.loc[10:20, 'cpu'] = np.nan
df.loc[50:55, 'cpu'] = np.nan
df.to_csv("corrupted_metrics.csv", index=False)
```

---

## 📝 Step 2: The Repair Task
Create a script `repair_data.py`:

1.  **Forward Fill:** Fill the gaps using the `ffill` method.
2.  **Linear Interpolation:** Fill the gaps using `interpolate`.
3.  **Visualization:** Plot the original (with gaps), the Forward Fill version, and the Interpolated version on the same chart.

---

## 🧪 Step 3: Discussion
Answer in your notes:
-   Which method looks more "Natural" for a CPU usage metric?
-   If you were dealing with "Total Error Count", would you use interpolation or just fill with 0? Why?

---

# Exercise 02: Scaling the Heights (Normalization)

## 🎯 Objective
Prepare multi-variate metrics for ML models by bringing them into the same scale.

---

## 🛠️ Step 1: Baseline Data
You have three metrics:
-   `cpu`: 0 to 100%
-   `latency`: 10 to 5000ms
-   `io_ops`: 100,000 to 500,000 ops

---

## 📝 Step 2: Scaling
1.  Apply `StandardScaler` to all 3 features.
2.  Apply `MinMaxScaler` to all 3 features.
3.  Compare the **Mean** and **Standard Deviation** of the results.

---

# Exercise 03: The Time Circle (Cyclic Encoding)

## 🎯 Objective
Convert hour and day-of-week into machine-understandable cyclic features.

---

## 🛠️ Task
Create a function `encode_time(dt)` that:
1.  Takes a datetime object.
2.  Calculates `hour_sin`, `hour_cos`, `day_sin`, and `day_cos`.
3.  Apply this to a series of 24 hours and plot the result in a 2D scatter plot. 
    *   **Hint:** It should form a perfect circle!

---

# Exercise 04: Correlation Matrix (Finding the Culprit)

## 🎯 Objective
Identify which infrastructure metrics are most closely linked to application latency.

---

## 🛠️ Step 1: Load Data
Use the `system_metrics.csv` from Day 1 or create a new one.

---

## 📝 Step 2: Heatmap
1.  Generate a Spearman correlation matrix.
2.  Visualize it with a Seaborn Heatmap.
3.  **Identify:** Which feature has the highest correlation with `latency`? Is it positive or negative?

---

# Exercise 05: Seasonal Decomposition (The Residual Search)

## 🎯 Objective
Extract the "Signal" from the "Seasonality".

---

## 🛠️ Task
1.  Load a dataset with clear daily patterns (e.g., website traffic).
2.  Use `statsmodels.tsa.seasonal.seasonal_decompose`.
3.  Plot the **Residual** component.
4.  Standardize the residual data. Any point with a value $> 3$ or $< -3$ is a "Statistical Anomaly".

---

## ✅ Deliverable
Submit your Python scripts and a few screenshots of your circular time plot and your correlation heatmap.
