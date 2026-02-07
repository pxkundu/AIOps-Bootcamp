# Anomaly Detection Cheat Sheet

> **Libraries:** `scikit-learn`, `pyod` (optional)  
> **Key Classes:** `IsolationForest`, `LocalOutlierFactor`, `OneClassSVM`

---

## 🌲 Isolation Forest (The Standard)

Best for high-dimensional data (CPU, Mem, Latency together).

```python
from sklearn.ensemble import IsolationForest

# 1. Initialize
# contamination='auto' or 0.01 (1% anomalies)
clf = IsolationForest(contamination=0.01, random_state=42)

# 2. Fit
clf.fit(X_train)

# 3. Predict (-1 = Anomaly, 1 = Normal)
y_pred = clf.predict(X_test)

# 4. Score (Lower is more anomalous)
scores = clf.decision_function(X_test)
```

**Crucial Tip:** Isolation Forest assumes anomalies are "rare and different". If your training data has many anomalies (e.g., >10%), set `contamination=0.1`.

---

## 🏘️ Local Outlier Factor (LOF)

Best for density-based outliers (e.g., a "loose" cluster).
It only works on *training* data (Novelty Detection is tricky with standard LOF, need `novelty=True`).

```python
from sklearn.neighbors import LocalOutlierFactor

# standard outlier detection (unsupervised)
clf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
y_pred = clf.fit_predict(X) 

# For Novelty Detection (train on clean, predict on dirty)
clf = LocalOutlierFactor(n_neighbors=20, novelty=True)
clf.fit(X_train_clean)
y_pred = clf.predict(X_test_dirty)
```

---

## ⭕ One-Class SVM

Best for when you have ONLY normal data to train on. (Semi-Supervised Anomaly Detection).

```python
from sklearn.svm import OneClassSVM

clf = OneClassSVM(nu=0.01, kernel="rbf", gamma=0.1)
clf.fit(X_train_clean)
y_pred = clf.predict(X_test)
```

**Warning:** Does not scale well to large datasets ($O(n^2)$). Use SGDOneClassSVM for big data.

---

## 📅 Contextual Features (Required for Time Series!)

You CANNOT feed raw timestamps.
Extract cyclic features.

```python
df['hour'] = df.index.hour
df['day'] = df.index.dayofweek

# Advanced: Cyclical Encoding (Sine/Cosine transform)
# 23:00 is close to 00:00, but 23 and 0 are far apart numerically.
import numpy as np

df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
```

---

## ⚡ Common Pitfalls

| Problem | Fix |
|---|---|
| **Curse of Dimensionality** | Distance metrics fail in high dimension. Use Isolation Forest (tree-based) or PCA first as preprocessing. |
| **Masking** | One huge outlier hides smaller anomalies. Remove the biggest outlier, re-run detection. |
| **Swamping** | Too many false positives. Reduce `contamination` parameter. |
