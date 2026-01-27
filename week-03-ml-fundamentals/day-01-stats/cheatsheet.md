# Statistical Cheat Sheet for AIOps (Python)

> Quick formulas and `scipy.stats` patterns for analyzing operational data.

---

## 📊 1. Descriptive Statistics with Pandas/Scipy

```python
import pandas as pd
import numpy as np
from scipy import stats

# Load metrics
df = pd.read_csv('metrics.csv')

# The "SRE Basics"
mean = df['latency'].mean()
median = df['latency'].median()
p95 = df['latency'].quantile(0.95)
p99 = df['latency'].quantile(0.99)

# Higher Moments
skew = stats.skew(df['latency'])      # If > 0, tail is on the right
kurtosis = stats.kurtosis(df['latency']) # If high, frequent outliers
```

---

## 🎲 2. Probability Distributions

| Distribution | When to use it | Scipy call |
|--------------|----------------|------------|
| **Normal** | Balanced resources (RAM) | `stats.norm` |
| **Poisson** | Request arrivals (Traffic) | `stats.poisson` |
| **Exponential** | Time between failures (MTTF) | `stats.expon` |
| **Log-Normal** | Accurate latency modeling | `stats.lognorm` |

---

## 🧪 3. Hypothesis Testing (A/B Deployment)

Check if Version B is significantly slower than Version A.

```python
# T-Test (Assumes normality)
t_stat, p_val = stats.ttest_ind(version_a_latency, version_b_latency)

# Mann-Whitney U Test (Use for non-normal latency data - Recommended!)
u_stat, p_val = stats.mannwhitneyu(version_a_latency, version_b_latency)

if p_val < 0.05:
    print("Regression Detected! Version B is different.")
```

---

## 📐 4. Entropy Calculation (For Logs)

```python
import math
from collections import Counter

def calculate_entropy(data):
    counts = Counter(data)
    total = len(data)
    entropy = 0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

# Usage: High entropy means diverse, unpredictable logs.
# Low entropy means monotonous, repetitive logs.
```

---

## 💡 AIOps Tips

1. **Log-Transform Latency:** Latency data is usually skewed. Applying `np.log(df['latency'])` often makes it look normal, which helps traditional ML models perform better.
2. **Coefficient of Variation (CV):** `CV = std / mean`. If CV > 1, your system is highly volatile (vulnerable to spikes).
3. **Outlier Detection (IQR):** 
   `Q1 = df.quantile(0.25); Q3 = df.quantile(0.75); IQR = Q3 - Q1`
   `Outliers = (df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))`
