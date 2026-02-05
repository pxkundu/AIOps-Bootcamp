# Time Series Cheat Sheet

> **Pandas Toolkit**: `resample`, `shift`, `rolling`, `diff`  
> **Stats Toolkit**: `seasonal_decompose`, `adfuller`, `acf/pacf`

---

## 📅 Pandas Time Manipulation

### 1. Setting the Index
Time series analysis REQUIRES the DateTime to be the index.

```python
import pandas as pd

df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
df.sort_index(inplace=True) # CRITICAL!
```

### 2. Resampling (Frequency Conversion)

| Symbol | Freq | code |
|---|---|---|
| 'S' | Seconds | `df.resample('S').mean()` |
| 'T' / 'min' | Minutes | `df.resample('5min').max()` |
| 'H' | Hours | `df.resample('1H').sum()` |
| 'D' | Days | `df.resample('1D').mean()` |
| 'W' | Weeks | `df.resample('W').mean()` |

### 3. Missing Data (Interpolation)
When you have gaps in your logs.

```python
# Forward Fill (propagate last valid observation)
df.fillna(method='ffill')

# Linear Interpolation (draw a line between points)
df.interpolate(method='time')
```

### 4. Rolling Windows (Smoothing)

```python
# Simple Moving Average (SMA)
df['sma_24h'] = df['cpu'].rolling(window='24h').mean()

# Exponential Weighted Moving Average (EWMA) - better for recent trends
df['ewma'] = df['cpu'].ewm(span=12).mean()
```

### 5. Shift & Diff (Feature Engineering)

```python
# Lag (What happened 1 step ago?)
df['lag_1'] = df['cpu'].shift(1)

# Difference (Change from last step) - MAKES DATA STATIONARY
df['diff_1'] = df['cpu'].diff(1)
```

---

## 🔬 Statsmodels & Analysis

### 1. Seasonal Decomposition (STL)
Visualizing Trend vs Noise.

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# model='additive' if amplitude is constant
# model='multiplicative' if amplitude is growing
result = seasonal_decompose(df['cpu'], model='additive', period=1440) # 1440 mins/day

result.plot()
plt.show()

# Access components
trend = result.trend
seasonal = result.seasonal
residual = result.resid
```

### 2. Stationarity Test (ADF)
Checking if you can forecast.

```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(df['cpu'].dropna())
print(f"ADF Statistic: {result[0]}")
print(f"p-value: {result[1]}")

# Interpretation
if result[1] < 0.05:
    print("✅ Stationary (Ready for Modeling)")
else:
    print("❌ Non-Stationary (Needs Differencing)")
```

### 3. Autocorrelation Plots (ACF/PACF)
Checking how correlated past data is with future data.

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# ACF: Correlation with lagged values
plot_acf(df['cpu'], lags=50)

# PACF: Correlation excluding indirect influence
plot_pacf(df['cpu'], lags=50)
```

---

## 🚀 Common Patterns

| Use Case | Method |
|---|---|
| Remove daily noise | `rolling('24H').mean()` |
| Fix irregular timestamps | `resample('5min').mean().interpolate()` |
| Remove trend | `diff()` |
| Extract daily cycle | `seasonal_decompose()` |
