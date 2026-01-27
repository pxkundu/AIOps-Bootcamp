# Preprocessing & EDA Cheat Sheet (AIOps)

> Essential snippets for cleaning and transforming operational data.

---

## 🧹 1. Handling Missing Values (Imputation)

```python
import pandas as pd

# Forward Fill (propagate last valid observation forward)
df['cpu'].fillna(method='ffill', inplace=True)

# Linear Interpolation (Bridge the gap)
df['mem'] = df['mem'].interpolate(method='linear')

# Zero fill (best for error counts)
df['errors'].fillna(0, inplace=True)
```

---

## ⚖️ 2. Scaling & Normalization

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Use StandardScaler for metrics with no fixed bounds (Latency)
scaler = StandardScaler()
df['latency_scaled'] = scaler.fit_transform(df[['latency']])

# Use MinMaxScaler for percentage-based metrics (CPU, RAM)
mm_scaler = MinMaxScaler()
df['cpu_norm'] = mm_scaler.fit_transform(df[['cpu_usage']])
```

---

## ⏳ 3. Time-Based Feature Engineering

```python
# Convert index to datetime
df.index = pd.to_datetime(df.index)

# Extract basic components
df['hour'] = df.index.hour
df['day_of_week'] = df.index.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

# Cyclic Encoding (The AIOps "Must-Have")
import numpy as np
df['hour_sin'] = np.sin(2 * np.pi * df.hour/24.0)
df['hour_cos'] = np.cos(2 * np.pi * df.hour/24.0)
```

---

## 🔍 4. Detecting Correlations (The Heatmap)

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Correlation matrix
corr = df.corr()

# Visualize
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Metrics Correlation Matrix")
plt.show()
```

---

## 🌊 5. Seasonal Decomposition

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Decompose a metric (e.g. traffic)
# Period is the number of points in a cycle (e.g. 24 if hourly)
result = seasonal_decompose(df['traffic'], model='additive', period=24)

# Plot components
result.plot()
plt.show()

# Get the 'Cleaned' data (Residuals)
anomalies_only = result.resid.dropna()
```

---

## 💡 Pro-Tips for the Data Alchemist

1.  **Check for Constant Features:** If a metric never changes (e.g., `is_active=1` for all rows), drop it. It adds noise but no information.
2.  **Window Functions:** Use `df.rolling(window=5).mean()` to smooth out jittery metrics before analysis.
3.  **Outlier Removal:** Use **Z-Scores**. Any point with `|Z| > 3` is usually a candidate for capping or investigation.
    `df['latency'] = df['latency'].clip(lower=lower_bound, upper=upper_bound)`
