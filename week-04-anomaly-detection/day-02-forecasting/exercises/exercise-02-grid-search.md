# Exercise 02: Grid Search from Scratch

## 🎯 Objective
Understand how Automatic ARIMA works by building your own "Brute Force" parameter searcher. You will iterate through combinations of $(p, d, q)$, train models, and select the best one based on **AIC** (Akaike Information Criterion).

---

## 📊 The Data
Use the same `AirPassengers` dataset or a synthetic random walk with drift.

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")

# Load simple dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv'
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month')
series = df['Passengers']
```

## 🛠️ Task 1: The Loop

Write a triple nested loop:
- $p$ from 0 to 4
- $d$ from 0 to 2
- $q$ from 0 to 4

Inside the loop:
1. Try to fit `ARIMA(p,d,q)`.
2. Catch errors (some combinations are invalid).
3. Store the $(p,d,q)$ tuple and the resulting `result.aic`.

## 🛠️ Task 2: Selection

1. Sort your results by AIC (ascending).
2. Print the top 3 models.
3. Do they make sense? (e.g., if data has a trend, $d$ should probably be 1).

## 🛠️ Task 3: Validation

Train the "Best" model and plot the forecast against the actual data.

```python
# Helper to visualize
def evaluate_arima_model(data, order):
    # Train/Test Split
    train, test = data[0:-12], data[-12:]
    history = [x for x in train]
    predictions = []
    
    # Walk-forward validation
    for t in range(len(test)):
        model = ARIMA(history, order=order)
        model_fit = model.fit()
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])
        
    return predictions, test
```

## 📝 Deliverable
A script that outputs:
```text
Best ARIMA(2, 1, 2) AIC=1234.56
Top 3 Models: ...
```
And a plot of the best forecast.
