# Exercise 01: Build Your First Incident Classifier

## 🎯 Objective
Build a binary classifier to predict whether a log event will lead to a CRITICAL incident within the next 5 minutes.

---

## 📊 The Dataset

You have access to `incident_logs.csv` with the following structure:

| Column | Description | Example |
|--------|-------------|---------|
| `timestamp` | Event time | `2026-01-20 14:30:00` |
| `service` | Microservice name | `api-gateway` |
| `level` | Log level | `ERROR` |
| `cpu_usage` | CPU % at event time | `0.85` |
| `memory_usage` | Memory % | `0.72` |
| `error_count_5min` | Errors in last 5 min | `12` |
| `response_time_p95` | 95th percentile latency (ms) | `450` |
| `is_critical` | **Label:** 1 if incident occurred | `0` or `1` |

**Data Distribution:**
- Total samples: 10,000
- CRITICAL incidents: 150 (1.5%)
- NORMAL events: 9,850 (98.5%)

---

## 🛠️ Step 1: Load and Explore

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('incident_logs.csv')

# Basic exploration
print(df.head())
print(df.info())
print(df['is_critical'].value_counts())

# Visualize class imbalance
df['is_critical'].value_counts().plot(kind='bar')
plt.title('Class Distribution')
plt.xlabel('Class')
plt.ylabel('Count')
plt.xticks([0, 1], ['NORMAL', 'CRITICAL'], rotation=0)
plt.show()
```

**Question 1:** What percentage of events are CRITICAL?

---

## 🛠️ Step 2: Feature Engineering

Create additional features to improve model performance:

```python
# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Time-based features
df['hour'] = df['timestamp'].dt.hour
df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 17)).astype(int)

# Encode log level
level_map = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3, 'CRITICAL': 4}
df['level_encoded'] = df['level'].map(level_map)

# Interaction features
df['cpu_memory_product'] = df['cpu_usage'] * df['memory_usage']
df['error_rate_per_cpu'] = df['error_count_5min'] / (df['cpu_usage'] + 0.01)  # Avoid division by zero

# Display engineered features
print(df[['hour', 'is_business_hours', 'level_encoded', 'cpu_memory_product']].head())
```

**Question 2:** Why do we add 0.01 in the denominator for `error_rate_per_cpu`?

---

## 🛠️ Step 3: Prepare Data for Training

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Select features
feature_cols = [
    'cpu_usage', 'memory_usage', 'error_count_5min', 'response_time_p95',
    'hour', 'is_business_hours', 'level_encoded', 
    'cpu_memory_product', 'error_rate_per_cpu'
]

X = df[feature_cols]
y = df['is_critical']

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print(f"CRITICAL in train: {y_train.sum()} ({y_train.mean():.2%})")
print(f"CRITICAL in test: {y_test.sum()} ({y_test.mean():.2%})")
```

**Question 3:** Why do we use `stratify=y` in the split?

---

## 🛠️ Step 4: Train a Baseline Model (Logistic Regression)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Train
model_lr = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
model_lr.fit(X_train_scaled, y_train)

# Predict
y_pred_lr = model_lr.predict(X_test_scaled)

# Evaluate
print("=== Logistic Regression ===")
print(classification_report(y_test, y_pred_lr, target_names=['NORMAL', 'CRITICAL']))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred_lr))
```

**Question 4:** What is the recall for CRITICAL incidents? Is this acceptable for AIOps?

---

## 🛠️ Step 5: Train a Random Forest

```python
from sklearn.ensemble import RandomForestClassifier

# Train
model_rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    class_weight='balanced',
    random_state=42
)
model_rf.fit(X_train, y_train)  # No scaling needed for tree-based models!

# Predict
y_pred_rf = model_rf.predict(X_test)

# Evaluate
print("=== Random Forest ===")
print(classification_report(y_test, y_pred_rf, target_names=['NORMAL', 'CRITICAL']))

# Feature importance
importances = pd.DataFrame({
    'feature': feature_cols,
    'importance': model_rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 Features:")
print(importances.head())
```

**Question 5:** Which feature is most important? Does this make sense?

---

## 🛠️ Step 6: Handle Imbalance with SMOTE

```python
from imblearn.over_sampling import SMOTE

# Apply SMOTE
smote = SMOTE(sampling_strategy=0.3, random_state=42)  # Make CRITICAL 30% of NORMAL
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)

print(f"Before SMOTE: {len(y_train)} samples, {y_train.sum()} CRITICAL")
print(f"After SMOTE: {len(y_train_smote)} samples, {y_train_smote.sum()} CRITICAL")

# Retrain Logistic Regression
model_lr_smote = LogisticRegression(max_iter=1000, random_state=42)  # No class_weight needed now
model_lr_smote.fit(X_train_smote, y_train_smote)

# Evaluate
y_pred_lr_smote = model_lr_smote.predict(X_test_scaled)
print("\n=== Logistic Regression + SMOTE ===")
print(classification_report(y_test, y_pred_lr_smote, target_names=['NORMAL', 'CRITICAL']))
```

**Question 6:** Did SMOTE improve recall? What about precision?

---

## 🛠️ Step 7: Tune the Decision Threshold

```python
from sklearn.metrics import precision_recall_curve
import numpy as np

# Get probabilities
y_proba_rf = model_rf.predict_proba(X_test)[:, 1]

# Find optimal threshold
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba_rf)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(thresholds, precisions[:-1], label='Precision')
plt.plot(thresholds, recalls[:-1], label='Recall')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.title('Precision-Recall vs Threshold')
plt.legend()
plt.grid(True)
plt.show()

# Use custom threshold (e.g., 0.3 for high recall)
threshold = 0.3
y_pred_custom = (y_proba_rf > threshold).astype(int)

print(f"\n=== Random Forest (Threshold = {threshold}) ===")
print(classification_report(y_test, y_pred_custom, target_names=['NORMAL', 'CRITICAL']))
```

**Question 7:** What threshold gives you 95% recall? What's the trade-off?

---

## 🛠️ Step 8: Save Your Best Model

```python
import joblib

# Save model and scaler
joblib.dump(model_rf, 'incident_classifier.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Test loading
loaded_model = joblib.load('incident_classifier.pkl')
loaded_scaler = joblib.load('scaler.pkl')

# Make a prediction on new data
new_event = [[0.92, 0.88, 25, 650, 14, 1, 3, 0.81, 27.2]]  # High CPU, many errors
new_event_scaled = loaded_scaler.transform(new_event)
prediction = loaded_model.predict(new_event_scaled)
probability = loaded_model.predict_proba(new_event_scaled)[:, 1]

print(f"\nPrediction: {'CRITICAL' if prediction[0] == 1 else 'NORMAL'}")
print(f"Confidence: {probability[0]:.2%}")
```

---

## 🎯 Challenge Tasks

### Task 1: Beat the Baseline
**Goal:** Achieve F1-score > 0.80 for CRITICAL class.

**Hints:**
- Try XGBoost
- Experiment with different SMOTE ratios
- Add more engineered features (e.g., rolling averages)

---

### Task 2: Minimize False Negatives
**Goal:** Achieve recall > 0.95 while keeping precision > 0.50.

**Hints:**
- Lower the decision threshold
- Use `scale_pos_weight` in XGBoost
- Consider ensemble methods (voting classifier)

---

### Task 3: Explain Predictions
**Goal:** For a misclassified sample, explain why the model got it wrong.

**Hints:**
- Use SHAP values
- Analyze feature values for false positives/negatives
- Compare to correctly classified samples

```python
import shap

explainer = shap.TreeExplainer(model_rf)
shap_values = explainer.shap_values(X_test)

# Explain a specific prediction
idx = 42  # Index of sample to explain
shap.force_plot(explainer.expected_value[1], shap_values[1][idx], X_test.iloc[idx])
```

---

## 📝 Submission

Create a Jupyter notebook with:
1. Your final model code
2. Evaluation metrics (confusion matrix, classification report)
3. Feature importance plot
4. At least one SHAP explanation
5. A brief writeup (200 words) on your approach and results

**Evaluation Criteria:**
- F1-score for CRITICAL class (40%)
- Code quality and documentation (30%)
- Feature engineering creativity (20%)
- Insights and analysis (10%)

---

## 💡 Bonus: Real-time Prediction API

Deploy your model as a Flask API:

```python
from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('incident_classifier.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array([data['features']])
    features_scaled = scaler.transform(features)
    
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0, 1]
    
    return jsonify({
        'prediction': 'CRITICAL' if prediction == 1 else 'NORMAL',
        'probability': float(probability)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

Test it:
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.92, 0.88, 25, 650, 14, 1, 3, 0.81, 27.2]}'
```

---

## 🔗 Resources

- [Scikit-learn Classification Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics)
- [Handling Imbalanced Data](https://imbalanced-learn.org/stable/over_sampling.html)
- [SHAP Documentation](https://shap.readthedocs.io/)
