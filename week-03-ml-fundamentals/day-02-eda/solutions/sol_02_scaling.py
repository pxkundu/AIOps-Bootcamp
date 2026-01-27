import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Mock Data
data = {
    'cpu': np.random.uniform(0, 100, 1000),
    'latency': np.random.exponential(500, 1000),
    'io_ops': np.random.randint(100000, 500000, 1000)
}
df = pd.DataFrame(data)

# 1. Standard Scaling (Z-Score)
ss = StandardScaler()
df_ss = pd.DataFrame(ss.fit_transform(df), columns=df.columns)

# 2. Min-Max Scaling (Normalizing)
mm = MinMaxScaler()
df_mm = pd.DataFrame(mm.fit_transform(df), columns=df.columns)

print("--- Original Stats ---")
print(df.describe().loc[['mean', 'std']])

print("\n--- Standard Scaled Stats (Goal: Mean ~0, Std ~1) ---")
print(df_ss.describe().loc[['mean', 'std']])

print("\n--- Min-Max Scaled Stats (Goal: Min 0, Max 1) ---")
print(df_mm.describe().loc[['min', 'max']])
