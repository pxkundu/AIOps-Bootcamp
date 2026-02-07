# Exercise 02: The Contextual Trap (LOF vs IF)

## 🎯 Objective
Understand why Point Anomaly detection (Isolation Forest) fails on **Contextual Anomalies** and why Feature Engineering is critical.

---

## 📊 The Challenge Data
Imagine CPU usage:
- **Day (9 AM - 5 PM):** High Usage (80%) is NORMAL.
- **Night (5 PM - 9 AM):** Low Usage (10%) is NORMAL.
- **Attack:** High Usage (80%) at 3 AM.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate Time Series (24 hours * 7 days)
hours = np.tile(np.arange(24), 7)
day_mask = (hours >= 9) & (hours <= 17)

# Normal Traffic
cpu = np.where(day_mask, 
               np.random.normal(80, 5, len(hours)), # Day: ~80%
               np.random.normal(10, 5, len(hours))) # Night: ~10%

# Add Attack (The Sleeper)
# At index 3 (3 AM on Day 1), inject high CPU
cpu[3] = 85 

df = pd.DataFrame({'hour': hours, 'cpu': cpu})

# Plot
plt.figure(figsize=(12, 4))
plt.plot(df['cpu'], label='CPU Usage')
plt.scatter(3, df['cpu'][3], color='red', s=100, label='Attack')
plt.legend()
plt.show()
```

## 🛠️ Fail Attempt 1: Raw Isolation Forest
Train `IsolationForest` on just `df[['cpu']]`.

```python
from sklearn.ensemble import IsolationForest
clf = IsolationForest(contamination=0.01)
df['if_raw'] = clf.fit_predict(df[['cpu']])
```

**Question:** Did it catch the attack at index 3?
**Hypothesis:** It likely WON'T. Why? Because 85% is "Normal" context-wise (Daytime). The algorithm doesn't know it's 3 AM.

## 🛠️ Success Attempt 2: Engineered Features
Train `IsolationForest` on `df[['cpu', 'hour']]`.

```python
clf = IsolationForest(contamination=0.01)
df['if_context'] = clf.fit_predict(df[['cpu', 'hour']])
```

**Task:**
1. Check if `df.loc[3]` is flagged as -1.
2. Plot the results. The 3 AM spike should be red.

## 📝 Deliverable
A notebook proving that `IF(cpu)` fails but `IF(cpu, hour)` succeeds. This is proof you understand **Contextual Anomalies**.
