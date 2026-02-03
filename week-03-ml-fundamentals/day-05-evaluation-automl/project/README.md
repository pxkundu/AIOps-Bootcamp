# Week 3 Day 5 Project: The AutoML Challenge

> **Objective:** You are given a tough, "messy" AIOps dataset. Your goal is to build the best possible model using any tools you like (Manual Tuning, Optuna, or AutoML).

---

## 🏆 The Challenge

**Scenario:** Methods Inc. has provided a dataset of 10,000 server metrics with a label `is_failure`.
- **Constraint 1:** The data has missing values.
- **Constraint 2:** The data is highly imbalanced (2% failures).
- **Constraint 3:** There are categorical features (e.g., `server_type`).
- **Goal:** Maximize **Recall** while keeping **Precision > 0.5**.

---

## 📂 Project Structure

```
automl-challenge/
├── data/
│   ├── generate_messy_data.py  # Create the tough dataset
│   └── server_metrics.csv      # The data
├── src/
│   ├── manual_tuning.py        # Approach 1: GridSearch/Optuna
│   ├── automl_tpot.py          # Approach 2: TPOT
│   └── evaluate.py             # Compare results
├── notebook/
│   └── leaderboard.ipynb       # Analysis
└── README.md
```

---

## 🛠️ Step 1: Generate Messy Data

```python
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

def generate_messy_data():
    # Core data
    X, y = make_classification(n_samples=10000, n_features=20, n_informative=5, weights=[0.98, 0.02], random_state=42)
    df = pd.DataFrame(X, columns=[f"metric_{i}" for i in range(20)])
    
    # Add noise & mess
    # 1. Missing values
    for col in df.columns:
        if np.random.rand() > 0.5:
            df.loc[df.sample(frac=0.1).index, col] = np.nan
            
    # 2. Categorical feature
    df['server_type'] = np.random.choice(['db', 'app', 'cache', 'proxy'], size=len(df))
    
    # 3. Target
    df['is_failure'] = y
    
    return df

df = generate_messy_data()
df.to_csv('server_metrics.csv', index=False)
```

---

## 🛠️ Step 2: Approach 1 - The Data Scientist

Write a script `src/manual_tuning.py` that:
1. Preprocesses data (Impute missing values, One-Hot Encode `server_type`).
2. Uses **SMOTE** pipeline to handle imbalance.
3. Uses **Optuna** to tune an XGBoost or LightGBM model.
4. Reports the best F1 Score.

---

## 🛠️ Step 3: Approach 2 - The Lazy Engineer (AutoML)

Write a script `src/automl_tpot.py` that:
1. Feeds the raw data (or minimally processed) into **TPOTClassifier**.
2. Lets it run for 10 generations.
3. Exports the best pipeline.
4. Reports the score.

*Note: TPOT might need integer encoding for categoricals.*

---

## 🛠️ Step 4: Examination

Compare the two approaches in `notebook/leaderboard.ipynb`.
1. Which one got a better score?
2. Which one took longer to run?
3. Look at the TPOT exported code. Did it do something surprising (e.g., used PCA or a specific scaler)?
4. Use **SHAP** on the winner to explain the top 3 drivers of failure.

---

## 🚀 Submission
Submit the repository with:
1. The `generate_messy_data.py` script.
2. Your best model file (`.pkl`).
3. A `README.md` containing a "Leaderboard" table showing the F1 scores of your Manual attempt vs. AutoML attempt.
