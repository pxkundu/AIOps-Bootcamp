# Exercise 01: Tuning and Explaining Models

## 🎯 Objective
Take a baseline Random Forest model, perform advanced hyperparameter tuning using **Optuna**, and then explain its predictions using **SHAP**.

---

## 📊 The Data
Use the `sklearn.datasets.make_classification` to generate a tricky dataset.

```python
from sklearn.datasets import make_classification
import pandas as pd

X, y = make_classification(
    n_samples=2000, 
    n_features=20, 
    n_informative=3, # Only 3 features actually matter!
    n_redundant=2, 
    n_classes=2, 
    weights=[0.9, 0.1], # Imbalanced (10% target)
    random_state=42
)

# Convert to DF for easier handling
feature_names = [f"feature_{i}" for i in range(20)]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y
```

---

## 🛠️ Step 1: Baseline Evaluation
Train a default RandomForest and evaluate it using Stratified K-Fold.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

# Your code here:
# 1. Initialize RF
# 2. Run cross_val_score with cv=5 and scoring='f1'
# 3. Print mean F1 score
```

---

## 🛠️ Step 2: Tune with Optuna
Use Optuna to find better parameters.

```python
import optuna

def objective(trial):
    # Search space
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    max_depth = trial.suggest_int('max_depth', 3, 30)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
    
    clf = RandomForestClassifier(
        n_estimators=n_estimators, 
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42,
        class_weight='balanced' # Crucial for imbalance
    )
    
    # 3-Fold for speed during search
    scores = cross_val_score(clf, X, y, cv=3, scoring='f1')
    return scores.mean()

# Run optimization
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=20)

print("Best params:", study.best_params)
print("Best F1:", study.best_value)
```

**Task:** Compare the Optuna result to your baseline. Did it improve?

---

## 🛠️ Step 3: Explain with SHAP
Retrain the model with the best parameters on the full dataset, then explain it.

```python
import shap

# 1. Train best model
best_model = RandomForestClassifier(**study.best_params, random_state=42)
best_model.fit(X, y)

# 2. Initialize Explainer
explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X)

# 3. Summary Plot
shap.summary_plot(shap_values[1], X, feature_names=feature_names) # Index 1 for positive class
```

**Task:**
1. Look at the Summary Plot.
2. Which are the top 3 features?
3. Since we generated the data with `n_informative=3`, does the model correctly identify the 3 real features, or is it using noise?

---

## 📝 Submission
Submit a notebook where you:
1. Show the baseline F1 score.
2. Run the Optuna study and show the improvement.
3. Display the SHAP summary plot and write a 1-sentence conclusion on whether the model found the "informative" features.
