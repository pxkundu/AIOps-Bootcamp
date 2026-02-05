# Solution for Exercise 02: Decomposition Lab
# Week 4 Day 1

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# ---------------------------------------------------------
# 1. CREATE SYNTHETIC SIGNAL
# ---------------------------------------------------------
print("Generating synthetic metrics...")
minutes = np.arange(0, 14*1440) # 14 days
dates = pd.date_range('2026-01-01', periods=len(minutes), freq='T')

# Components
trend = minutes * 0.001 + 20                 # Linear Growth
seasonality = 10 * np.sin(2 * np.pi * minutes / 1440) # Daily Sine Wave
noise = np.random.normal(0, 2, len(minutes)) # Stochastic Noise

y = trend + seasonality + noise

df = pd.DataFrame({'cpu': y}, index=dates)

# ---------------------------------------------------------
# 2. DECOMPOSE
# ---------------------------------------------------------
print("Decomposing signal...")

# We know the period is daily (1440 minutes)
result = seasonal_decompose(df['cpu'], model='additive', period=1440)

# ---------------------------------------------------------
# 3. EXTRACTION (The "Broken Sensor" Challenge)
# ---------------------------------------------------------
# Reconstruct Reciduals manually to verify
# Residual = Observed - Trend - Seasonal
extracted_residuals = df['cpu'] - result.trend - result.seasonal

print(f"Residual Mean: {extracted_residuals.mean():.4f} (Expected ~0)")
print(f"Residual Std: {extracted_residuals.std():.4f} (Expected ~2.0)")

# ---------------------------------------------------------
# 4. VISUALIZATION
# ---------------------------------------------------------
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

result.observed.plot(ax=ax1, title='Observed (Raw Data)', color='black')
result.trend.plot(ax=ax2, title='Trend (Growth)', color='blue')
result.seasonal.plot(ax=ax3, title='Seasonality (Daily Cycle)', color='green')
result.resid.plot(ax=ax4, title='Residuals (True Anomalies)', color='red', marker='.', linestyle='None', alpha=0.3)

# Add a fake anomaly threshold to the residual plot
ax4.axhline(y=6, color='orange', linestyle='--', label='Anomaly Threshold (+3 sigma)')
ax4.axhline(y=-6, color='orange', linestyle='--')
ax4.legend()

plt.tight_layout()
plt.show()
