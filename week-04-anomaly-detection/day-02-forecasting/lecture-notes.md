# Week 4 Day 2: Forecasting with ARIMA

> **Duration:** 8 hours | **Difficulty:** Advanced  
> **Focus:** Predicting future values using statistical properties of the past.

---

## 🎯 Learning Objectives

By the end of today, you will be able to:
1.  **Understand** the components of ARIMA (AR, I, MA).
2.  **Determine** optimal parameters $(p,d,q)$ using ACF/PACF plots.
3.  **Train** a model to forecast server load or cloud costs.
4.  **Evaluate** forecasts using MAPE and RMSE.

---

## 🔮 Part 1: The Components of ARIMA

ARIMA stands for **AutoRegressive Integrated Moving Average**. It is the standard for non-seasonal data.

### 1. AR ($p$): Auto-Regression
"The future depends on the past."
$$Y_t = \alpha Y_{t-1} + \epsilon$$
- If today is hot, tomorrow is likely hot.
- **$p$**: Number of lag observations included (Lag order).

### 2. I ($d$): Integrated
"The trend must be removed."
- ARIMA only works on **Stationary** data (flat mean).
- **$d$**: Number of times raw observations are *differenced* ($\Delta Y$).
- Usually $d=1$ (Linear trend) or $d=0$ (Already stationary).

### 3. MA ($q$): Moving Average
"The future depends on past errors (shocks)."
$$Y_t = \beta \epsilon_{t-1} + \epsilon$$
- If we made a huge error yesterday, we adapt today.
- **$q$**: Size of the moving average window.

```mermaid
graph TD
    A[Raw Data] --> B{Is it Stationary?}
    B -->|No| C[Difference (d=1)]
    C --> B
    B -->|Yes| D[Identify AR (p) & MA (q)]
    D --> E[Train Model]
    E --> F[Forecast Future]
```

---

## 🛠️ Part 2: Tuning the Hyperparameters $(p,d,q)$

How do you pick the numbers?

### Method A: The Visual Way (ACF/PACF)
1.  **ACF (AutoCorrelation Function):** Helps determining $q$.
2.  **PACF (Partial ACF):** Helps determining $p$.

| Plot Pattern | Interpretation |
|---|---|
| PACF cuts off after lag $k$ | Suggests AR($k$), so set $p=k$. |
| ACF cuts off after lag $k$ | Suggests MA($k$), so set $q=k$. |

### Method B: The Brute Force Way (Grid Search)
Try every combination $(0..5, 0..2, 0..5)$ and pick the one with the lowest **AIC** (Akaike Information Criterion).
*Lower AIC = Better Model.*

---

## 📅 Part 3: SARIMA (Adding Seasonality)

If your data cycles every 24 hours, ARIMA will fail. You need **SARIMA**:
$$ARIMA(p,d,q) \times (P,D,Q)_m$$

- $m$: Season length (e.g., 24 for hourly data).
- $P, D, Q$: The AR/I/MA parts for the *seasonal* component.

---

## 📉 Part 4: Evaluation Metrics

How do you know if your "Oracle" is lying?

1.  **MAE (Mean Absolute Error):** "On average, I'm off by 5 CPUs."
2.  **MAPE (Mean Absolute Percentage Error):** "On average, I'm off by 2%." (Preferred for business).
3.  **RMSE (Root Mean Squared Error):** Penalizes large outliers heavily.

---

<p align="center">
  <a href="../day-01-time-series/lecture-notes.md">⬅️ Back: Day 1</a> | <strong>Day 2: Ops Forecasting</strong> | <a href="../day-03-algorithms/lecture-notes.md">Next: Day 3 ➡️</a>
</p>
