# Solution for Exercise 01: Tuning Lab
# Week 4 Day 2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

# ---------------------------------------------------------
# 1. GENERATE DATA
# ---------------------------------------------------------
print("Generating AR(1) process...")
np.random.seed(42)

# AR(1) with alpha = 0.9
# ArmaProcess expects [1, -alpha] for AR coefficients
ar = np.array([1, -0.9]) 
ma = np.array([1])

process = ArmaProcess(ar, ma)
y = process.generate_sample(nsample=1000)
df = pd.DataFrame({'value': y})

# ---------------------------------------------------------
# 2. DIAGNOSTICS
# ---------------------------------------------------------
print("Plotting ACF/PACF...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# PACF should cut off after lag 1 --> Indicates AR(1)
plot_pacf(df['value'], ax=ax1, lags=20, method='ywm')

# ACF should decay gradually (geometric decay)
plot_acf(df['value'], ax=ax2, lags=20)

plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# 3. TRAIN MODEL
# ---------------------------------------------------------
print("Training ARIMA(1,0,0)...")
# We choose (1,0,0) because PACF shows 1 significant lag
model = ARIMA(df['value'], order=(1, 0, 0))
result = model.fit()

print(result.summary())

# Verify Coefficient
# Look for 'ar.L1' in the output. It should be close to 0.9.
coef = result.params['ar.L1']
print(f"\nDiscovered AR Parameter: {coef:.4f} (True Value: 0.9)")

# ---------------------------------------------------------
# 4. FORECAST
# ---------------------------------------------------------
forecast = result.get_forecast(steps=20)
mean_forecast = forecast.predicted_mean
conf_int = forecast.conf_int()

print("\nForecast (Next 5 steps):")
print(mean_forecast.head())

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df.index[-50:], df['value'].tail(50), label='History')
plt.plot(mean_forecast.index, mean_forecast, label='Forecast', color='red')
plt.fill_between(mean_forecast.index, 
                 conf_int.iloc[:, 0], 
                 conf_int.iloc[:, 1], 
                 color='pink', alpha=0.3)
plt.title("ARIMA Forecast")
plt.legend()
plt.show()
