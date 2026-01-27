import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# 1. Generate Synthetic Traffic (Daily seasonality + Trend + Spike)
time = pd.date_range("2024-01-01", periods=168, freq="H") # 1 week
trend = np.linspace(10, 20, 168)
season = 10 * np.sin(2 * np.pi * np.arange(168) / 24)
noise = np.random.normal(0, 1, 168)
traffic = trend + season + noise

# 2. Inject a "Real" Anomaly (The spike)
traffic[100] += 50 

df = pd.DataFrame({"time": time, "traffic": traffic})
df.set_index("time", inplace=True)

# 3. Decompose
result = seasonal_decompose(df['traffic'], model='additive', period=24)

# 4. Analyze Residuals
resid = result.resid.dropna()
z_score = (resid - resid.mean()) / resid.std()
anomalies = z_score[np.abs(z_score) > 3]

# 5. Plot
result.plot()
plt.show()

print(f"Anomalies detected in residual component: {len(anomalies)}")
print(anomalies)
