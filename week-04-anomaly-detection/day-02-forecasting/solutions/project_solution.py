# Solution for Day 2 Project: The Budget Forecaster
# Week 4 Day 2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pmdarima as pm
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error

# ---------------------------------------------------------
# 1. GENERATE COST DATA
# ---------------------------------------------------------
def generate_costs(days=365):
    np.random.seed(42)
    dates = pd.date_range(start='2025-01-01', periods=days)
    
    # Baseline + Trend
    trend = np.linspace(1000, 2825, days) # Grows by ~5/day
    
    # Seasonality (Weekly)
    # 0=Mon, 6=Sun. Weekends are lower.
    day_of_week = dates.dayofweek
    seasonality = np.where(day_of_week >= 5, -200, 0) # Drop $200 on weekends
    
    # Noise
    noise = np.random.normal(0, 50, days)
    
    costs = trend + seasonality + noise
    return pd.Series(costs, index=dates)

print("Generating AWS Costs...")
data = generate_costs()
train, test = data.iloc[:-30], data.iloc[-30:]

# ---------------------------------------------------------
# 2. AUTO-TUNE (Grid Search)
# ---------------------------------------------------------
print("Searching for best SARIMA parameters (this may take a moment)...")

# m=7 for Weekly seasonality
model_auto = pm.auto_arima(train,
                           m=7,
                           seasonal=True,
                           start_p=0, start_q=0,
                           max_p=3, max_q=3,
                           d=1, # We know there is a trend
                           trace=True,
                           error_action='ignore',  
                           suppress_warnings=True)

print("\nBest Model Found:")
print(model_auto.summary())

# ---------------------------------------------------------
# 3. FORECAST
# ---------------------------------------------------------
print("\nForecasting next 30 days...")
forecast = model_auto.predict(n_periods=30)
forecast = pd.Series(forecast, index=test.index)

# ---------------------------------------------------------
# 4. EVALUATION
# ---------------------------------------------------------
mape = mean_absolute_percentage_error(test, forecast)
print(f"\nMAPE: {mape:.4f} (Goal < 0.05)")

total_bill_pred = forecast.sum()
total_bill_actual = test.sum()
print(f"Predicted Bill: ${total_bill_pred:,.2f}")
print(f"Actual Bill:    ${total_bill_actual:,.2f}")
print(f"Difference:     ${total_bill_pred - total_bill_actual:,.2f}")

# ---------------------------------------------------------
# 5. VISUALIZATION
# ---------------------------------------------------------
plt.figure(figsize=(12, 6))
plt.plot(train.index[-60:], train.tail(60), label='Train (Last 60 days)')
plt.plot(test.index, test, label='Actual Costs', color='green')
plt.plot(forecast.index, forecast, label='Forecast', color='red', linestyle='--')
plt.title(f"Cloud Cost Forecast (MAPE: {mape*100:.2f}%)")
plt.ylabel("Cost ($)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
