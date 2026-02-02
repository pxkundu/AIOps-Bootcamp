# Exercise 02: Multi-Class Severity Classification

## 🎯 Objective
Build a **multi-class classifier** to predict incident severity levels: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.

This is more realistic than binary classification, as production systems have multiple alert levels.

---

## 📊 The Dataset

`severity_logs.csv` contains:

| Column | Description | Example |
|--------|-------------|---------|
| `cpu_usage` | CPU % | `0.65` |
| `memory_usage` | Memory % | `0.78` |
| `disk_io` | Disk I/O (MB/s) | `120` |
| `network_latency` | Network latency (ms) | `45` |
| `error_rate` | Errors per minute | `5` |
| `request_rate` | Requests per second | `1200` |
| `severity` | **Label:** `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` | `MEDIUM` |

**Distribution:**
- LOW: 7,000 (70%)
- MEDIUM: 2,000 (20%)
- HIGH: 800 (8%)
- CRITICAL: 200 (2%)

---

## 🛠️ Step 1: Load and Encode Labels

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('severity_logs.csv')

# Encode labels
label_encoder = LabelEncoder()
df['severity_encoded'] = label_encoder.fit_transform(df['severity'])

# Mapping
print("Label Mapping:")
for i, label in enumerate(label_encoder.classes_):
    print(f"{i}: {label}")

# Class distribution
print("\nClass Distribution:")
print(df['severity'].value_counts())
```

---

## 🛠️ Step 2: Train a Multi-Class Classifier

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Prepare data
feature_cols = ['cpu_usage', 'memory_usage', 'disk_io', 'network_latency', 'error_rate', 'request_rate']
X = df[feature_cols]
y = df['severity_encoded']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    class_weight='balanced',  # Handles imbalance
    random_state=42
)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=label_encoder.classes_, 
            yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
```

---

## 🛠️ Step 3: Analyze Misclassifications

```python
# Find misclassified samples
misclassified_idx = y_test != y_pred
misclassified_df = X_test[misclassified_idx].copy()
misclassified_df['actual'] = label_encoder.inverse_transform(y_test[misclassified_idx])
misclassified_df['predicted'] = label_encoder.inverse_transform(y_pred[misclassified_idx])

print("Sample Misclassifications:")
print(misclassified_df.head(10))

# Most common misclassification
from collections import Counter
misclass_pairs = list(zip(
    label_encoder.inverse_transform(y_test[misclassified_idx]),
    label_encoder.inverse_transform(y_pred[misclassified_idx])
))
print("\nMost Common Misclassifications:")
print(Counter(misclass_pairs).most_common(5))
```

**Question:** Are most errors between adjacent severity levels (e.g., MEDIUM ↔ HIGH)?

---

## 🛠️ Step 4: Use XGBoost for Better Performance

```python
import xgboost as xgb

# Calculate class weights
from sklearn.utils.class_weight import compute_sample_weight
sample_weights = compute_sample_weight('balanced', y_train)

# Train
model_xgb = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=8,
    learning_rate=0.1,
    objective='multi:softmax',  # Multi-class
    num_class=4,
    random_state=42
)
model_xgb.fit(X_train, y_train, sample_weight=sample_weights)

# Predict
y_pred_xgb = model_xgb.predict(X_test)

# Evaluate
print("=== XGBoost ===")
print(classification_report(y_test, y_pred_xgb, target_names=label_encoder.classes_))
```

---

## 🎯 Challenge: Ordinal Classification

**Problem:** The model treats severity levels as independent categories. But they're **ordinal** (LOW < MEDIUM < HIGH < CRITICAL).

**Task:** Penalize predictions that are "far off" more than those that are "close".

**Hint:** Use a custom loss function or convert to regression:
```python
# Treat as regression problem
severity_map = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2, 'CRITICAL': 3}
df['severity_numeric'] = df['severity'].map(severity_map)

from sklearn.ensemble import RandomForestRegressor
model_reg = RandomForestRegressor(n_estimators=200, random_state=42)
model_reg.fit(X_train, df.loc[X_train.index, 'severity_numeric'])

# Predict and round
y_pred_reg = model_reg.predict(X_test)
y_pred_reg_rounded = np.round(y_pred_reg).clip(0, 3).astype(int)

# Evaluate
print(classification_report(df.loc[X_test.index, 'severity_numeric'], y_pred_reg_rounded))
```

---

## 📝 Deliverables

1. Confusion matrix for Random Forest and XGBoost
2. Analysis of top 3 most common misclassifications
3. Comparison: Does ordinal regression improve results?
4. Feature importance plot

---

## 🔗 Resources

- [Scikit-learn Multi-class Classification](https://scikit-learn.org/stable/modules/multiclass.html)
- [XGBoost Multi-class](https://xgboost.readthedocs.io/en/stable/tutorials/multiclass.html)
