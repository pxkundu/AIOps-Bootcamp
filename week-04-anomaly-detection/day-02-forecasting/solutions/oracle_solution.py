# Solution for "The Oracle's Challenge"
# Week 4 Day 2 Gamification

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def solve_level_1_ar(data):
    """
    Level 1: Data depends on yesterday.
    Tool: AR(1) Model.
    """
    print("🔮 Oracle Level 1: Auto-Regression")
    # p=1, d=0, q=0
    model = ARIMA(data, order=(1, 0, 0))
    res = model.fit()
    return res.forecast(steps=10)

def solve_level_2_trend(data):
    """
    Level 2: Strong Trend.
    Tool: Differencing (d=1).
    """
    print("🔮 Oracle Level 2: Random Walk with Drift")
    # p=0, d=1, q=0
    model = ARIMA(data, order=(0, 1, 0))
    res = model.fit()
    return res.forecast(steps=10)

def solve_level_3_shocks(data):
    """
    Level 3: Moving Average (Shocks).
    Tool: MA(1).
    """
    print("🔮 Oracle Level 3: Moving Average")
    # p=0, d=0, q=1
    model = ARIMA(data, order=(0, 0, 1))
    res = model.fit()
    return res.forecast(steps=10)

def solve_level_4_seasonal(data):
    """
    Level 4: Seasonal Pattern.
    Tool: SARIMA.
    """
    print("🔮 Oracle Level 4: Seasonality")
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    # Seasonal Order (P,D,Q,s) -> (1,0,0,7) for weekly
    model = SARIMAX(data, order=(1,0,0), seasonal_order=(1,0,0,7))
    res = model.fit()
    return res.forecast(steps=10)

# Mock Runner
if __name__ == "__main__":
    # Create Dummy Data for Level 1
    # Y_t = 0.9 * Y_{t-1}
    y = [10]
    for i in range(100):
        y.append(0.9 * y[-1] + np.random.normal(0, 0.1))
    
    forecast = solve_level_1_ar(y)
    print("Forecast:", forecast.values)
    print("\n✅ ORACLE ACCEPTED. PROCEED TO DAY 3.")
