# Supervised Learning Cheat Sheet

> Quick reference for classification algorithms, metrics, and scikit-learn code.

---

## 🎯 Core Concepts

### Supervised Learning Formula
```
f(X) → y
X = Features (input)
y = Labels (output)
```

**Types:**
- **Classification:** Predict categories (NORMAL, CRITICAL)
- **Regression:** Predict numbers (response time, CPU usage)

---

## 🤖 Classification Algorithms

### 1. Logistic Regression
```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# ALWAYS scale features first!
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

model = LogisticRegression(
    class_weight='balanced',  # Handle imbalance
    max_iter=1000
)
model.fit(X_scaled, y_train)

# Predict
y_pred = model.predict(scaler.transform(X_test))
y_proba = model.predict_proba(scaler.transform(X_test))[:, 1]
```

**When to use:** Fast inference, interpretable coefficients.

---

### 2. Random Forest
```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,       # Number of trees
    max_depth=10,           # Prevent overfitting
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)

# Feature importance
importances = model.feature_importances_
```

**When to use:** Non-linear patterns, need feature importance.

---

### 3. XGBoost
```python
import xgboost as xgb

dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test)

params = {
    'objective': 'binary:logistic',
    'max_depth': 6,
    'eta': 0.1,
    'scale_pos_weight': 99  # Imbalance ratio
}

model = xgb.train(params, dtrain, num_boost_round=100)
y_pred = model.predict(dtest)
```

**When to use:** Maximum accuracy, large datasets.

---

## 📊 Evaluation Metrics

### Confusion Matrix
```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=['NORMAL', 'CRITICAL'])
disp.plot()
```

|                | Predicted 0 | Predicted 1 |
|----------------|-------------|-------------|
| **Actual 0**   | TN          | FP          |
| **Actual 1**   | FN          | TP          |

---

### Key Metrics

```python
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score

# All-in-one report
print(classification_report(y_test, y_pred))

# Individual metrics
precision = precision_score(y_test, y_pred)  # TP / (TP + FP)
recall = recall_score(y_test, y_pred)        # TP / (TP + FN)
f1 = f1_score(y_test, y_pred)                # Harmonic mean
```

**Formulas:**
- **Precision:** Of predicted failures, how many were real?
- **Recall:** Of real failures, how many did we catch?
- **F1-Score:** Balance between precision and recall

**AIOps Rule:** Prioritize **Recall** (can't miss failures!)

---

### ROC Curve & AUC
```python
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

fpr, tpr, thresholds = roc_curve(y_test, y_proba)
auc = roc_auc_score(y_test, y_proba)

plt.plot(fpr, tpr, label=f'AUC = {auc:.2f}')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()
```

**AUC Interpretation:**
- 0.5 = Random guessing
- 0.7-0.8 = Acceptable
- 0.8-0.9 = Good
- 0.9+ = Excellent

---

## ⚖️ Handling Imbalanced Data

### 1. Class Weighting
```python
# Automatic balancing
model = RandomForestClassifier(class_weight='balanced')

# Manual weights
class_weights = {0: 1, 1: 99}  # CRITICAL is 99x more important
model = RandomForestClassifier(class_weight=class_weights)
```

---

### 2. SMOTE (Oversampling)
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(sampling_strategy=0.1, random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

---

### 3. Undersampling
```python
from imblearn.under_sampling import RandomUnderSampler

rus = RandomUnderSampler(sampling_strategy=0.5, random_state=42)
X_resampled, y_resampled = rus.fit_resample(X_train, y_train)
```

---

### 4. Threshold Tuning
```python
# Default threshold: 0.5
# For high recall, lower it

y_proba = model.predict_proba(X_test)[:, 1]
y_pred_custom = (y_proba > 0.3).astype(int)  # More sensitive
```

---

## 🛠️ Feature Engineering

### Time-based Features
```python
import pandas as pd

df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)
```

---

### Categorical Encoding
```python
# Label Encoding
df['level_encoded'] = df['level'].map({
    'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4
})

# One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=['service'], prefix='service')
```

---

### Text Features
```python
df['message_length'] = df['message'].str.len()
df['has_error'] = df['message'].str.contains('error', case=False).astype(int)
df['has_timeout'] = df['message'].str.contains('timeout', case=False).astype(int)
```

---

### Rolling Window Features
```python
# Error rate in last 5 minutes
df['error_rate_5min'] = df.groupby('service')['is_error'].rolling(
    window='5min', on='timestamp'
).mean().reset_index(0, drop=True)

# Request count in last hour
df['request_count_1h'] = df.groupby('service')['timestamp'].rolling(
    window='1h', on='timestamp'
).count().reset_index(0, drop=True)
```

---

## 🔄 Train/Test Split

### Basic Split
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 80% train, 20% test
    stratify=y,         # Maintain class distribution
    random_state=42
)
```

---

### Time-based Split (for time series)
```python
# Don't shuffle! Use chronological order
split_date = '2026-01-01'
train_df = df[df['timestamp'] < split_date]
test_df = df[df['timestamp'] >= split_date]
```

---

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(
    model, X, y, 
    cv=5,              # 5-fold CV
    scoring='f1'       # Use F1 score
)

print(f"F1: {scores.mean():.2f} (+/- {scores.std():.2f})")
```

---

## 💾 Model Persistence

### Save Model
```python
import joblib

# Save
joblib.dump(model, 'failure_predictor.pkl')

# Load
loaded_model = joblib.load('failure_predictor.pkl')
predictions = loaded_model.predict(X_new)
```

---

### Save with Metadata
```python
import pickle
from datetime import datetime

model_artifact = {
    'model': model,
    'scaler': scaler,
    'feature_names': feature_cols,
    'trained_at': datetime.now(),
    'metrics': {'f1': 0.85, 'recall': 0.92}
}

with open('model_v1.pkl', 'wb') as f:
    pickle.dump(model_artifact, f)
```

---

## 🚀 Hyperparameter Tuning

### Grid Search
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    scoring='f1',
    n_jobs=-1  # Use all CPU cores
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best F1: {grid_search.best_score_:.2f}")
```

---

### Random Search (faster)
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_dist = {
    'n_estimators': randint(50, 300),
    'max_depth': randint(5, 20),
    'min_samples_split': randint(2, 20)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_dist,
    n_iter=20,  # Try 20 random combinations
    cv=3,
    scoring='f1',
    random_state=42
)

random_search.fit(X_train, y_train)
```

---

## 🎯 Quick Decision Guide

| Scenario | Algorithm | Why |
|----------|-----------|-----|
| Need speed (< 1ms) | Logistic Regression | Simplest, fastest |
| Need interpretability | Random Forest | Feature importance |
| Need max accuracy | XGBoost | State-of-the-art |
| Severe imbalance (1:1000) | XGBoost + SMOTE | Handles rare classes |
| Small dataset (< 1000 samples) | Logistic Regression | Less prone to overfitting |
| Large dataset (> 1M samples) | XGBoost (GPU) | Scalable |

---

## 🐛 Common Pitfalls

### ❌ Forgetting to Scale
```python
# WRONG
model = LogisticRegression()
model.fit(X_train, y_train)  # Features have different scales!

# RIGHT
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
model.fit(X_train_scaled, y_train)
```

---

### ❌ Data Leakage
```python
# WRONG - Scaling before split!
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled, y)

# RIGHT - Fit scaler only on training data
X_train, X_test, y_train, y_test = train_test_split(X, y)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Use same scaler!
```

---

### ❌ Using Accuracy for Imbalanced Data
```python
# WRONG
accuracy = (y_test == y_pred).mean()  # 99% but useless!

# RIGHT
from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_pred)  # Accounts for imbalance
```

---

## 📚 Essential Imports

```python
# Data manipulation
import pandas as pd
import numpy as np

# Modeling
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

# Evaluation
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    precision_score, 
    recall_score, 
    f1_score,
    roc_auc_score,
    roc_curve
)

# Imbalanced data
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# Persistence
import joblib
import pickle

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
```

---

## 🔗 Resources

- [Scikit-learn Cheat Sheet](https://scikit-learn.org/stable/tutorial/machine_learning_map/)
- [Imbalanced-learn Documentation](https://imbalanced-learn.org/)
- [XGBoost Parameters](https://xgboost.readthedocs.io/en/stable/parameter.html)
