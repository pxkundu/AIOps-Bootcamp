# Exercise 01: The Isolation Forest Lab

## 🎯 Objective
Use **Isolation Forest** to detect anomalies in a dataset containing normal server metrics and injected attacks. Visualize how the algorithm "isolates" outliers.

---

## 📊 The Data
Generate synthetic server metrics (CPU, Memory) with 2 clusters (Day Shift, Night Shift) and some random attacks.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# 1. Normal Traffic (Two Clusters)
# Cluster 1: Night Shift (Low CPU, Low Mem)
X1 = 0.3 * np.random.randn(100, 2)
X_train = np.r_[X1 + 2, X1 - 2] # Two blobs

# 2. Add Anomalies (Attacks)
# Outliers far from clusters
X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))

X = np.r_[X_train, X_outliers]
```

## 🛠️ Step 1: Detect Global Outliers
Train an Isolation Forest.

```python
clf = IsolationForest(contamination=0.1, random_state=42)
clf.fit(X)
y_pred = clf.predict(X) 
# -1 for outliers, 1 for inliers
```

## 🛠️ Step 2: Visualization
Plot the decision boundary.

```python
# Create a meshgrid to plot regions
xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.title("IsolationForest")
plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

# Plot data points
plt.scatter(X[:, 0], X[:, 1], c='white', s=20, edgecolor='k')
# Highlight anomalies
anomalies = X[y_pred == -1]
plt.scatter(anomalies[:, 0], anomalies[:, 1], c='red', s=20, edgecolor='k')
plt.show()
```

**Task:**
1.  How many red dots (anomalies) are inside the blue regions (normal)? Ideally none.
2.  Change `contamination` to 0.01. What happens? (Fewer red dots).
3.  Change `contamination` to 0.3. What happens? (Many normal points get flagged - False Positives).

## 📝 Deliverable
A notebook with the plot showing the boundary and red dots correctly identified as outliers.
