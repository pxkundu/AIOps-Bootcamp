# Solution for Exercise 01: Pandas Time Series Bootcamp
# Week 4 Day 1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. GENERATE CHAOS (Same as Exercise code)
# ---------------------------------------------------------
print("Generating chaotic data...")
np.random.seed(42)
base = datetime(2026, 2, 1, 8, 0, 0)
time_list = [base + timedelta(seconds=np.random.randint(1, 3600)) for _ in range(500)]
time_list.sort()

df = pd.DataFrame({
    'timestamp': time_list,
    'cpu': np.random.normal(50, 10, 500), # Mean 50, Std 10
    'memory': np.random.normal(60, 5, 500)
})

# Add some real gaps (NaNs) just to be sure we handle them
df.loc[100:110, 'cpu'] = np.nan 

# ---------------------------------------------------------
# 2. TAMING THE CHAOS
# ---------------------------------------------------------
print("Cleaning data...")

# A. Set Index
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# B. Resample to 1-minute buckets
# This aggregates multiple points in the same minute using mean()
# It also creates empty rows for minutes with no data!
df_1min = df.resample('1min').mean()

print(f"Original shape: {df.shape}")
print(f"Resampled shape: {df_1min.shape}")

# C. Check for Gaps
missing = df_1min.isnull().sum()
print(f"Missing values after resampling:\n{missing}")

# D. Interpolate
# 'time' method is best for irregular intervals, but requires DatetimeIndex
df_clean = df_1min.interpolate(method='time')

print("Gaps after interpolation:", df_clean.isnull().sum().sum())

# ---------------------------------------------------------
# 3. SMOOTHING & VISUALIZATION
# ---------------------------------------------------------
# Calculate Rolling Mean
df_clean['cpu_rolling_5min'] = df_clean['cpu'].rolling(window=5).mean()

# Plot
plt.figure(figsize=(12, 6))
plt.plot(df_clean.index, df_clean['cpu'], label='Raw (Resampled)', alpha=0.4, color='blue')
plt.plot(df_clean.index, df_clean['cpu_rolling_5min'], label='5min Moving Avg', color='red', linewidth=2)
plt.title("Server CPU: Taming the Chaos")
plt.xlabel("Time")
plt.ylabel("CPU Usage (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("Done! Check the plot.")
