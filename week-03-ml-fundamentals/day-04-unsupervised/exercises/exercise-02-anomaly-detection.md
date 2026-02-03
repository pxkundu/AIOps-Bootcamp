# Exercise 02: Detecting Anomalies in Metrics (Isolation Forest)

## 🎯 Objective
Use **Isolation Forest** to detect anomalies in server metrics (CPU and Memory). You will learn to identify "multivariate" anomalies—states that are abnormal not because one metric is high, but because the *combination* is unusual.

---

## 📊 The Scenario
You have 1000 data points representing server state every minute.
- **Normal:** Low CPU, High Memory (Database caching)
- **Normal:** High CPU, High Memory (Active processing)
- **Anomaly:** High CPU, **Low** Memory (Potential infinite loop leak or cache failure? Unusual.)

---

## 🛠️ Step 1: Generate Synthetic Data

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

# Generate "Normal" Cluster 1: Idle state
cpu_idle = np.random.normal(loc=10, scale=5, size=500)
mem_idle = np.random.normal(loc=10, scale=5, size=500)

# Generate "Normal" Cluster 2: Heavy Load
cpu_load = np.random.normal(loc=80, scale=10, size=400)
mem_load = np.random.normal(loc=80, scale=10, size=400)

# Generate "Anomalies": High CPU, Low Memory
cpu_anom = np.random.normal(loc=85, scale=5, size=20)
mem_anom = np.random.normal(loc=15, scale=5, size=20)

# Combine
cpu = np.concatenate([cpu_idle, cpu_load, cpu_anom])
mem = np.concatenate([mem_idle, mem_load, mem_anom])
X = np.column_stack((cpu, mem))

plt.scatter(X[:,0], X[:,1], s=10)
plt.xlabel("CPU %")
plt.ylabel("Memory %")
plt.title("Server Metrics")
plt.show()
```

**Task:** Run this and look at the plot. Can you spot the outliers visually?

---

## 🛠️ Step 2: Train Isolation Forest

Isolation Forest works by randomly splitting data. Anomalies are easier to isolate (require fewer splits) than normal clusters.

```python
from sklearn.ensemble import IsolationForest

# Config: contamination represents the approximate % of anomalies we expect
clf = IsolationForest(contamination=0.03, random_state=42)
preds = clf.fit_predict(X)

# preds: 1 for Normal, -1 for Anomaly
df = pd.DataFrame({'cpu': cpu, 'mem': mem, 'anomaly': preds})

print("Anomaly Counts:")
print(df['anomaly'].value_counts())
```

---

## 🛠️ Step 3: Visualize Boundaries

Let's visualize exactly what the model considers "anomalous".

```python
# Create a meshgrid to plot decision boundary
xx, yy = np.meshgrid(np.linspace(0, 100, 100), np.linspace(0, 100, 100))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(10, 6))
plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

# Plot data points
anomalies = df[df['anomaly'] == -1]
normal = df[df['anomaly'] == 1]

plt.scatter(normal['cpu'], normal['mem'], c='white', s=20, edgecolor='k', label='Normal')
plt.scatter(anomalies['cpu'], anomalies['mem'], c='red', s=50, edgecolor='k', label='Anomaly')

plt.xlabel('CPU %')
plt.ylabel('Memory %')
plt.title('Isolation Forest Decision Boundary')
plt.legend()
plt.show()
```

**Task:** Analyze the plot. Did it catch the High CPU/Low Memory group? Did it flag any false positives in the normal clusters?

---

## 🛠️ Step 4: Comparison with Standard Thresholds

Traditional monitoring uses static thresholds (e.g., `CPU > 90%`).

**Task:**
1. Define a rule: `if cpu > 90: alert`.
2. Compare how many "true anomalies" (from our generated set) this rule catches vs. the Isolation Forest.
3. Compare how many false positives it triggers.

**Reflection:** Why is the specific case of High CPU + Low Memory hard to catch with simple thresholds?

---

## 📝 Submission
Submit a notebook showing:
1. The data generation and visualization.
2. The Isolation Forest training and result plot.
3. A brief answer to the reflection question above.
