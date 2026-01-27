import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Setup
time = pd.date_range("2024-01-01", periods=100, freq="H")
values = np.sin(np.linspace(0, 10, 100)) + 10
df = pd.DataFrame({"timestamp": time, "cpu": values})

# Inject Gaps
df.loc[10:25, 'cpu'] = np.nan
df.loc[50:60, 'cpu'] = np.nan

# 2. Imputation
df['ffill'] = df['cpu'].fillna(method='ffill')
df['interpolated'] = df['cpu'].interpolate(method='linear')

# 3. Visualization
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['cpu'], 'o', label='Original (with Gaps)', markersize=4)
plt.plot(df['timestamp'], df['ffill'], '--', label='Forward Fill', alpha=0.7)
plt.plot(df['timestamp'], df['interpolated'], '-', label='Linear Interpolation', alpha=0.7)
plt.title("AIOps Data Healing: Imputation Comparison")
plt.legend()
plt.show()

print("AIOps Context:")
print("- Forward fill creates 'steps'. Good for binary states or resource clamps.")
print("- Interpolation creates 'slopes'. Better for gradual metrics like temperature or slow RAM growth.")
