import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. Generate the same data as the exercise
np.random.seed(42)
mem = np.random.normal(loc=70, scale=5, size=1000)
latency = np.random.lognormal(mean=2, sigma=0.8, size=1000)
requests = np.random.poisson(lam=10, size=1000)

df = pd.DataFrame({
    'memory_pct': mem,
    'latency_ms': latency,
    'qps': requests
})

# 2. Central Tendencies
print("--- Central Tendency (Latency) ---")
print(f"Mean:   {df['latency_ms'].mean():.2f}")
print(f"Median: {df['latency_ms'].median():.2f}")
print(f"Mode:   {df['latency_ms'].mode()[0]:.2f}")
print("Note: Mean > Median. This is characteristic of a 'Right Skewed' (Long Tail) distribution.\n")

# 3. Percentiles
print("--- Percentiles (Latency) ---")
print(f"P50: {df['latency_ms'].quantile(0.50):.2f}")
print(f"P95: {df['latency_ms'].quantile(0.95):.2f}")
print(f"P99: {df['latency_ms'].quantile(0.99):.2f}\n")

# 4. Outlier Detection (IQR)
Q1 = df['latency_ms'].quantile(0.25)
Q3 = df['latency_ms'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
outliers = df[df['latency_ms'] > upper_bound]

print(f"--- Outlier Detection ---")
print(f"Upper Bound: {upper_bound:.2f}")
print(f"Number of outliers found: {len(outliers)}")
print(f"Percentage of data as outlier: {(len(outliers)/len(df))*100:.2f}%\n")

# 5. Skewness and Kurtosis
print("--- Shape ---")
for col in df.columns:
    print(f"{col}: Skew={stats.skew(df[col]):.2f}, Kurtosis={stats.kurtosis(df[col]):.2f}")

# Optional: Plotting
# df.hist(bins=50, figsize=(12, 8))
# plt.tight_layout()
# plt.show()
