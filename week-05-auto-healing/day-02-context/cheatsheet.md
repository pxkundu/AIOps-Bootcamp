# Remediation Cheat Sheet: Decision Trees

> **Libraries:** `scikit-learn`, `joblib`, `pandas`  
> **Key Classes:** `DecisionTreeClassifier`, `export_text`

---

## 🌳 Creating a Decision Tree

The core logic of intelligent triage.

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# 1. Prepare Data
# Features: [CPU, Memory, DiskTotal]
X = [[95, 20, 10],   # Case 1
     [10, 95, 10],   # Case 2
     [10, 10, 95]]   # Case 3

# Actions: 0=Ignore, 1=KillApp, 2=RestartSvc, 3=CleanLogs
y = [1, 2, 3]

# 2. Train
clf = DecisionTreeClassifier(max_depth=3) # Limit depth to avoid overfitting
clf.fit(X, y)

# 3. Predict
result = clf.predict([[96, 22, 12]])
print(f"Recommended Action: {result[0]}")
```

---

## 📜 Interpreting the Logic

See exactly *why* the model made a decision.

```python
from sklearn.tree import export_text

# Text Representation
r = export_text(clf, feature_names=['cpu', 'mem', 'disk'])
print(r)

# Output:
# |--- cpu <= 50.00
# |   |--- mem <= 50.00
# |   |   |--- class: 3 (CleanLogs)
# |   |--- mem >  50.00
# |   |   |--- class: 2 (RestartSvc)
# |--- cpu >  50.00
# |   |--- class: 1 (KillApp)
```

---

## 💾 Saving & Loading Models

Deploy your "Smart Doctor" to production.

```python
import joblib

# Save
joblib.dump(clf, 'triage_model.pkl')

# Load (in your API or Script)
loaded_clf = joblib.load('triage_model.pkl')
action = loaded_clf.predict([[new_data]])
```

---

## 📅 Feature Engineering Context

Numbers are easy. Concepts are hard. Convert concepts to numbers.

```python
import pandas as pd

df = pd.DataFrame({'timestamp': ['2025-01-01 14:00', '2025-01-01 03:00']})
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 1. Hour of Day
df['hour'] = df['timestamp'].dt.hour
df['is_night'] = (df['hour'] < 6) | (df['hour'] > 22)

# 2. Day of Week
df['day'] = df['timestamp'].dt.dayofweek # 0=Mon, 6=Sun
df['is_weekend'] = df['day'] >= 5
```

---

## ⚡ Common Pitfalls

| Problem | Fix |
|---|---|
| **Overfitting** | If tree is too deep, it memorizes every incident. Set `max_depth=3` or `min_samples_leaf=5`. |
| **Imbalanced Classes** | Most incidents are "Ignore". Use `class_weight='balanced'`. |
| **New Features** | If you add a feature (e.g., Latency), you must retrain the model. |
