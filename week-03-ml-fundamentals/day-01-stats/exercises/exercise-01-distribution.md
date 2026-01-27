# Exercise: Analyzing Distribution of System Data

## 🎯 Objective
Learn how to identify the statistical profile of different system metrics and understand why "Average" is the enemy of AIOps.

---

## 📋 Prerequisites
- Python 3.10+
- `pip install pandas numpy matplotlib scipy`

---

## 🛠️ Step 1: Generate Scenarios
Create a python script `generate_data.py` to create three types of system behavior data:

```python
import pandas as pd
import numpy as np

# Scenario 1: Stable Memory Usage (Normal)
mem = np.random.normal(loc=70, scale=5, size=1000)

# Scenario 2: Web Latency (Log-Normal/Long Tail)
latency = np.random.lognormal(mean=2, sigma=0.8, size=1000)

# Scenario 3: Request Bursts (Poisson)
requests = np.random.poisson(lam=10, size=1000)

df = pd.DataFrame({
    'memory_pct': mem,
    'latency_ms': latency,
    'qps': requests
})
df.to_csv('system_metrics.csv', index=False)
```

---

## 📝 Step 2: The Statistical Deep Dive
Create a Jupyter notebook or a python script `analyze_stats.py`:

1.  **Calculate Central Tendencies:** For `latency_ms`, calculate Mean, Median, and Mode. Which one is the highest? Why?
2.  **Percentile mapping:** Find the P50, P95, and P99 of `latency_ms`.
3.  **Visualization:** Plot a histogram of all three metrics.
    *   Which one looks like a Bell?
    *   Which one has a long tail to the right?
4.  **Skewness & Kurtosis:** Calculate these for all three. How do they compare?

---

## 🧪 Step 3: Outlier Detection
Using the **IQR method** (Interquartile Range), identify how many "latency spikes" exist in your generated data.

```python
# Hint:
# Q1 = df['latency_ms'].quantile(0.25)
# Q3 = df['latency_ms'].quantile(0.75)
# IQR = Q3 - Q1
# Upper_Bound = Q3 + 1.5 * IQR
```

---

## ✅ Deliverable
A report (or commented script) answering:
1. Why is the Mean for latency so different from the Median?
2. Looking at the histogram of `qps`, does it look like a normal distribution? If not, what makes it different?
3. What is the P99 latency value in your dataset?
