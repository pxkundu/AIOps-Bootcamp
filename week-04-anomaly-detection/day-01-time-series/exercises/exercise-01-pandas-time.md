# Exercise 01: Pandas Time Series Bootcamp

## 🎯 Objective
Master the art of manipulating time series data. In AIOps, logs arrive at random times (`12:01:03`, `12:01:55`). Your goal is to convert chaos into structured, regularly spaced data (`12:01:00`, `12:02:00`).

---

## 📊 The Data (`server_metrics_chaos.csv`)
Imagine a CSV with irregular timestamps and gaps.

```csv
timestamp,cpu_usage,memory_usage
2026-02-01 08:00:01, 45, 60
2026-02-01 08:00:05, 47, 61
2026-02-01 08:02:10, 80, 70  <-- Big gap!
2026-02-01 08:02:12, 82, 72
```

## 🛠️ Task 1: Generate Chaos
Run this snippet to create your training data.

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create irregular indices
base = datetime(2026, 2, 1, 8, 0, 0)
time_list = [base + timedelta(seconds=np.random.randint(1, 3600)) for _ in range(500)]
time_list.sort()

df = pd.DataFrame({
    'timestamp': time_list,
    'cpu': np.random.normal(50, 10, 500),
    'memory': np.random.normal(60, 5, 500)
})

# Save raw
df.to_csv('server_metrics_chaos.csv', index=False)
```

## 🛠️ Task 2: Taming the Chaos

1.  **Load** the CSV.
2.  **Convert** `timestamp` to datetime objects.
3.  **Set Index** to `timestamp`.
4.  **Resample** to `1-minute` buckets using the `mean()`.
    *   *Hint:* `df.resample('1min').mean()`
5.  **Check for Gaps:** Are there any `NaN` values? (There should be, due to the random gaps).
6.  **Interpolate:** Fill the gaps using `time` interpolation.

## 🛠️ Task 3: Smoothing

The data is noisy.
1.  Calculate a **5-minute Rolling Mean**.
2.  Plot the **Raw Data** (Blue) vs the **Rolling Mean** (Red).
3.  Notice how the Red line reveals the trend?

## 📝 Deliverable
A Python script that:
1. loads chaos,
2. resamples to 1min,
3. fills gaps,
4. plots comparisons.
