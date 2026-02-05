# Week 4 Day 1 Resources: Time Series

> Essentials for Time Series Analysis, Forecasting, and Pandas manipulation.

---

## 📚 Essential Reading

### The Bible of Forecasting
- **[Forecasting: Principles and Practice (Hyndman)](https://otexts.com/fpp3/)** - Free online book. Read Chapter 1 (Getting Started) and Chapter 6 (Time series decomposition). This is the gold standard.

### Pandas & Analysis
- **[Pandas Time Series User Guide](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html)** - Official docs.
- **[A Comprehensive Guide to Time Series Analysis](https://www.kaggle.com/prashant111/complete-guide-on-time-series-analysis-in-python)** - Great Kaggle backgrounder.

### Concepts
- **[Stationarity in Time Series](https://towardsdatascience.com/stationarity-in-time-series-analysis-90c94f27322)** - Why mean/variance must be constant.
- **[Decomposing Time Series](https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/)** - MachineLearningMastery tutorial.

---

## 🛠️ Tools & Libraries

### Core
- **[Pandas](https://pandas.pydata.org/)** - For `resample`, `rolling`, `shift`.
- **[Statsmodels](https://www.statsmodels.org/stable/tsa.html)** - For `seasonal_decompose` and `adfuller`.

### Advanced (For later in the week)
- **[Prophet (Meta)](https://facebook.github.io/prophet/)** - Automatic forecasting.
- **[Darts](https://unit8co.github.io/darts/)** - Unified interface for Time Series (Prophet, ARIMA, PyTorch).

```bash
pip install pandas statsmodels matplotlib seaborn
```

---

## 📊 Datasets

- **[Air Passengers Data](https://www.kaggle.com/rakannimer/air-passengers)** - The "Hello World" of time series (Trend + Seasonality).
- **[Wikipedia Web Traffic](https://www.kaggle.com/c/web-traffic-time-series-forecasting)** - Real world chaotic traffic.
- **[Numenta Anomaly Benchmark (NAB)](https://github.com/numenta/NAB)** - Real streams with anomalies.

---

## 💡 Pro Tips

1.  **Always Set the Index:** If your dataframe index isn't `DatetimeIndex`, Pandas won't treat it as a time series.
2.  **Date Parsing is Hard:** Use `pd.to_datetime(col, format='%Y-%m-%d...')` explicitly to speed it up.
3.  **Visualization First:** Never model a time series without plotting it first. You might see obvious seasonality that a model would miss.
4.  **UTC Always:** Store data in UTC. Convert to local time only for visualization.
