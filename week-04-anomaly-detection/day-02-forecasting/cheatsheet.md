# Forecasting Cheat Sheet

> **Libraries:** `statsmodels`, `pmdarima`  
> **Key Classes:** `ARIMA`, `SARIMAX`

---

## 🏗️ Building an ARIMA Model

### 1. Manual Configuration (Statsmodels)

```python
from statsmodels.tsa.arima.model import ARIMA

# 1. Define Model (p=1, d=1, q=1)
model = ARIMA(train_data, order=(1, 1, 1))

# 2. Train
result = model.fit()

# 3. Summary (Check P-values & AIC)
print(result.summary())

# 4. Forecast
forecast = result.forecast(steps=10)
print(forecast)
```

### 2. Auto-Discovery (Auto ARIMA)
The "Easy Button" for finding $(p,d,q)$. Requires `pip install pmdarima`.

```python
import pmdarima as pm

# Automatically finds best parameters
model = pm.auto_arima(train_data,
                      start_p=0, start_q=0,
                      max_p=5, max_q=5,
                      m=12,              # Seasonality (e.g. 12 months)
                      seasonal=True,     # SARIMA
                      d=None,            # Let model figure out 'd'
                      trace=True)

print(model.summary())
```

---

## 🔮 SARIMA (Seasonal ARIMA)

When data has cycles.

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Order = (p,d,q), Seasonal Order = (P,D,Q,s)
model = SARIMAX(train_data, 
                order=(1, 1, 1), 
                seasonal_order=(1, 1, 0, 12)) # 12-period cycle
result = model.fit()
```

---

## 📊 Diagnostics

### Check Residuals
A good model should have residuals that look like **White Noise** (No patterns left).

```python
result.plot_diagnostics(figsize=(10, 8))
plt.show()
```

### Visual Check

```python
# Plot actual vs forecast
plt.plot(test_data.index, test_data, label='Actual')
plt.plot(test_data.index, forecast, label='Forecast', color='red')
plt.legend()
plt.show()
```

---

## 📉 Error Metrics

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)

# MAPE (Manual calculation)
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
print(f"MAPE: {mape:.2f}%")
```

---

## ⚡ Common Pitfalls

| Error | Cause | Fix |
|---|---|---|
| **ConvergenceWarning** | Model can't find solution. | Data might be too messy. Try simplifying $(p,q)$ or increasing `d`. |
| **Flat line forecast** | $d=0$ on non-stationary data. | Increase $d$ to 1. |
| **Exploding forecast** | Unit root issue. | Data might need Log transformation mostly. |
