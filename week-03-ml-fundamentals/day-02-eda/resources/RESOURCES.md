# Week 3 Day 2 Resources: Preprocessing & EDA

> Master the art of data preparation for high-reliability systems.

---

## 📚 Essential Reading

- **[Python for Data Analysis (3rd Ed)](https://wesmckinney.com/book/)** - The definitive guide by Wes McKinney (creator of Pandas). Focus on chapters on Missing Data and Time Series.
- **[Feature Engineering for Machine Learning](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/)** - Excellent coverage of scaling, binning, and seasonal transformations.
- **[AIOps: Data Preparation Patterns](https://www.moogsoft.com/resources/guides/aiops-data-preparation/)** - Industry perspective on cleaning observability data.

---

## 🛠️ Tools & Libraries

- **[Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)** - Official documentation for Scalers and Transformers.
- **[Statsmodels: Seasonal Decomposition](https://www.statsmodels.org/stable/generated/statsmodels.tsa.seasonal.seasonal_decompose.html)** - Documentation for STL and additive/multiplicative models.
- **[D-Tale](https://github.com/man-group/dtale)** - A brilliant tool that brings a "Tableau-like" interface to your Pandas DataFrames.
- **[Tsfresh](https://tsfresh.readthedocs.io/en/latest/)** - Automatic extraction of 100s of features from time-series.

---

## 🎥 Video Tutorials

- **[EDA with Pandas in 10 Minutes](https://www.youtube.com/watch?v=R67XuYc9NQ4)** - Fast-paced refresher on data exploration.
- **[Time Series Decompositon Explained](https://www.youtube.com/watch?v=yYfG7-1rR_s)** - Visual intuition for trend and seasonality.
- **[Handling Outliers in Python](https://www.youtube.com/watch?v=lpS-mYStlU0)** - Strategies for outlier detection and removal.

---

## 💡 Pro-Tips for the Data Alchemist

1.  **Always Visualize First:** A histogram or scatter plot will reveal more than a `.describe()` call ever can.
2.  **Imputation is a double-edged sword:** Filling gaps creates "fake" data. Always keep a column `is_imputed` so you know where your data was originally missing.
3.  **Domain Knowledge vs. Pure Stats:** If a spike in CPU correlates exactly with a scheduled cron job, don't label it as an anomaly—encode the cron job time as a feature so the model learns it's normal.
