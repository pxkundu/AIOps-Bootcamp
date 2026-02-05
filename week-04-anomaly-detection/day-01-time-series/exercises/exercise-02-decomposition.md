# Exercise 02: The Decomposition Lab

## 🎯 Objective
Use **Seasonal Decomposition** to X-Ray a time series. You will uncover hidden patterns (Seasonality) embedded in noisy data.

---

## 📊 The Data
We will generate a synthetic signal that combines:
1.  **Trend:** Linear growth.
2.  **Seasonality:** A sine wave (daily cycle).
3.  **Noise:** Random jitter.

## 🛠️ Step 1: Create the Signal

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Time: 14 days, minute-by-minute
minutes = np.arange(0, 14*1440)
dates = pd.date_range('2026-01-01', periods=len(minutes), freq='T')

# 1. Trend: CPU grows as userbase grows
trend = minutes * 0.001 + 20

# 2. Seasonality: Daily sine wave (1440 mins = 2*pi)
seasonality = 10 * np.sin(2 * np.pi * minutes / 1440)

# 3. Noise: Random fluctuation
noise = np.random.normal(0, 2, len(minutes))

# Combine
y = trend + seasonality + noise

df = pd.DataFrame({'cpu': y}, index=dates)
df.plot(title="Raw Synthetic Data")
plt.show()
```

## 🛠️ Step 2: Decompose It
Use `statsmodels` to reverse-engineer the components.

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Period = 1440 (Minutes in a day)
decomposition = seasonal_decompose(df['cpu'], model='additive', period=1440)

decomposition.plot()
plt.show()
```

## 🛠️ Task 3: The Challenge (The Broken Sensor)
Imagine standard "Anomaly Detection" was running on the raw data.
- The `Trend` pushes the CPU higher every day.
- Eventually, it crosses the `CPU > 80%` threshold.
- Is this an anomaly? No, it's expected growth.

**Your Goal:**
1. Subtract the **Trend** and **Seasonality** from the raw data.
2. You are left with just the **Residuals** (Noise).
3. Plot the Residuals. Is the mean close to 0?
4. This "Residual" series is what you should run Anomaly Detection on!

## 📝 Deliverable
A Notebook showing the Decomposition plot and the extracted Residual plot.
