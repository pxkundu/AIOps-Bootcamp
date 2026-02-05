# Exercise 01: The Tuning Lab

## 🎯 Objective
Learn to read the tea leaves (ACF/PACF plots) to determine the correct ARIMA parameters $(p,d,q)$ without relying on automation.

---

## 📊 The Data
We will generate a simple **AR(1)** process.
$$Y_t = 0.8 Y_{t-1} + \epsilon$$

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess

# Generate AR(1) data with alpha=0.9
np.random.seed(42)
ar = np.array([1, -0.9]) # Note: Signs are flipped in statsmodels
ma = np.array([1])
ar_process = ArmaProcess(ar, ma)
y = ar_process.generate_sample(nsample=1000)

df = pd.DataFrame({'value': y})
df.plot(title="Synthetic AR(1) Process")
plt.show()
```

## 🛠️ Step 1: Stationarity Check
Is `d` required?
Run the ADF test (from Day 1).
- If p-value < 0.05, $d=0$.
- Else, diff the data and check again ($d=1$).

## 🛠️ Step 2: The Diagnostic Plots
Plot ACF and PACF.

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plot_acf(df['value'], ax=ax1, lags=20)
plot_pacf(df['value'], ax=ax2, lags=20)
plt.show()
```

**Analysis Task:**
- Does **PACF** cut off sharply after lag 1? (This implies $p=1$).
- Does **ACF** tail off gradually? (This confirms AR process).

## 🛠️ Step 3: Train the Model
Train an `ARIMA(1,0,0)` model.

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(df['value'], order=(1,0,0))
result = model.fit()
print(result.summary())
```

**Check:** Look at the coefficient for `ar.L1`. Is it close to 0.9 (our generator value)?

## 🛠️ Step 4: Forecasting
Predict the next 10 steps and plot them.

```python
forecast = result.get_forecast(steps=10)
pred_ci = forecast.conf_int()

ax = df['value'].iloc[-50:].plot(label='History')
forecast.predicted_mean.plot(ax=ax, label='Forecast', color='red')
plt.legend()
plt.show()
```

## 📝 Deliverable
A notebook showing the ACF/PACF plots and your interpretation of why $(1,0,0)$ is the best choice.
