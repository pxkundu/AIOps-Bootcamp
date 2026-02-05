# Week 4 Day 2 Resources: Advanced Forecasting

> Deep dive into ARIMA, SARIMA, and Real-world Forecasting challenges.

---

## 📚 Essential Reading

### The Theory (Mathematical Depth)
- **[Forecasting: Principles and Practice (Ch 8: ARIMA)](https://otexts.com/fpp3/arima.html)** - The "Bible" of forecasting. Read sections 8.1 (Stationarity), 8.5 (Non-seasonal ARIMA), and 8.9 (SARIMA).
- **[Introduction to Time Series and Forecasting (Brockwell & Davis)](https://www.amazon.com/Introduction-Time-Series-Forecasting-Springer/dp/3319298522)** - Graduate-level diagrammatic math.
- **[A Gentle Introduction to SARIMA](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/)** - Practical Python tutorial.

### Diagnostics & Tuning
- **[Interpretation of ACF and PACF Plots](https://towardsdatascience.com/interpreting-acf-and-pacf-plots-for-time-series-forecasting-af0d6db4061c)** - Visual guide to guessing p and q.
- **[AIC vs BIC](https://medium.com/@analytics_harry/aic-vs-bic-for-model-selection-in-python-4d0484558506)** - When to use which criterion for model selection.
- **[Stationarity Tests beyond ADF](https://www.statsmodels.org/dev/examples/notebooks/generated/stationarity_detrending_adf_kpss.html)** - KPSS test and others.

---

## 🛠️ Tools & Libraries

### Python Ecosystem
- **[Statsmodels](https://www.statsmodels.org/stable/tsa.html)**
  - `statsmodels.tsa.arima.model.ARIMA`: The standard class.
  - `statsmodels.tsa.statespace.sarimax.SARIMAX`: For Seasonality + Exogenous variables (X).
- **[pmdarima](http://alkaline-ml.com/pmdarima/)**
  - `auto_arima()`: The function that automates the Grid Search (Exercise 02).
- **[Prophet](https://facebook.github.io/prophet/)** (Coming in Day 3)
  - Handles holidays and missing data better than ARIMA.
- **[NeuralProphet](https://neuralprophet.com/)**
  - PyTorch-based upgrade to Prophet.

### Visualization
- **[Plotly for Time Series](https://plotly.com/python/time-series/)** - Interactive zooming (crucial for long histories).

```bash
pip install pmdarima statsmodels plotly
```

---

## 📊 Datasets for Practice

- **[M-Competitions Data](https://mofc.unic.ac.cy/m5-competition/)** - The olympics of forecasting (Walmart sales data).
- **[Generic Cloud Cost Data](https://github.com/Azure/Azure-Public-Dataset)** - VM utilization traces (Azure).
- **[Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales)** - Predict sales (Seasonal + Holidays).

---

## 💡 Pro Tips for SREs

1.  **Exogenous Variables (ARIMAX):**
    - Regular ARIMA predicts $Y$ based on past $Y$.
    - **ARIMAX** predicts $Y$ based on past $Y$ AND external $X$ (e.g., predicted CPU load based on *Marketing Spend*).
    - Use `SARIMAX` in statsmodels for this.

2.  **Long-Term vs Short-Term:**
    - ARIMA is great for **short-term** (next hour/day).
    - It is terrible for **long-term** (next year) because errors compound. Use Trend Regression (Day 1) for distinct long-term capacity planning.

3.  **Holidays:**
    - ARIMA has no concept of "Christmas". If your data has holiday spikes, you must add "Holiday" as an exogenous variable.
