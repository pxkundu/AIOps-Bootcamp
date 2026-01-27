# Exercise 02: Detecting Deployment Regressions

## 🎯 Objective
Use Statistical Hypothesis Testing (T-Test and Mann-Whitney U) to determine if a software deployment caused a significant performance regression or if the change is just "noise".

---

## 📋 The Scenario
You just deployed Version 2.1 of the *Checkout Service*. You have latency samples from both the old version (A) and the new version (B).

**Data (`deployment_test.py`):**
```python
import numpy as np
import pandas as pd

np.random.seed(42)
# Version A: Mean 100ms, Std 10
version_a = np.random.normal(100, 10, 100)
# Version B: Mean 105ms, Std 12 (Is this 5ms increase significant?)
version_b = np.random.normal(105, 12, 100)

df = pd.DataFrame({"vA": version_a, "vB": version_b})
df.to_csv("deployment_latency.csv", index=False)
```

---

## 🛠️ Step 1: Normality Check
Before choosing a test, you must know if your data is "Normal".
- Use `scipy.stats.shapiro` to test for normality.
- If `p-value > 0.05`, the data is Normal.

---

## 🧪 Step 2: The Hypothesis Test

1. **The Null Hypothesis (H0):** There is no difference between Version A and B.
2. **The Alternative Hypothesis (H1):** Version B is slower than Version A.

### Task:
- Run a **Student's T-Test** (`stats.ttest_ind`).
- Run a **Mann-Whitney U Test** (`stats.mannwhitneyu`).
- Compare the p-values.

---

## ✅ Deliverable
Answer these questions in your solution:
1. Was the 5ms increase "Statistically Significant" at a 95% confidence level?
2. Why might the Mann-Whitney U test be better for real-world production latency data than the T-Test?
3. If the p-value was 0.08, would you roll back the deployment? Why or why not?
