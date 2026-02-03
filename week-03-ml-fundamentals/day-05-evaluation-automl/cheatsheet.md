# Evaluation & AutoML Cheat Sheet

> Quick reference for validation strategies, hyperparameter tuning, and AutoML libraries.

---

## 🏗️ Cross-Validation (CV)

### Stratified K-Fold
**Use for:** Classification with imbalanced data (standard AIOps case).
```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
print(f"F1: {scores.mean():.3f} +/- {scores.std():.3f}")
```

### Time Series Split
**Use for:** Data with a time component (Logs, Metrics). **Crucial** to avoid look-ahead bias.
```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_index, test_index in tscv.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
```

---

## 🎛️ Hyperparameter Tuning

### RandomizedSearchCV
**Best balance** of speed and performance.
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(3, 20),
    'learning_rate': uniform(0.01, 0.3)
}

search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist,
    n_iter=50,  # Try 50 random combos
    cv=3,
    scoring='f1',
    n_jobs=-1
)
search.fit(X, y)
print(search.best_params_)
```

### Optuna (Bayesian Optimization)
**State-of-the-Art**. Smart search.
```python
import optuna

def objective(trial):
    # Define search space
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 30),
        'learning_rate': trial.suggest_loguniform('learning_rate', 1e-4, 1e-1)
    }
    
    model = XGBClassifier(**params)
    score = cross_val_score(model, X, y, cv=3, scoring='f1').mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
print(study.best_params)
```

---

## 🤖 AutoML

### TPOT (Genetic Algorithms)
```python
from tpot import TPOTClassifier

tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)
tpot.fit(X_train, y_train)
tpot.export('tpot_best_pipeline.py')
```

### Auto-Sklearn
```python
import autosklearn.classification

automl = autosklearn.classification.AutoSklearnClassifier(
    time_left_for_this_task=120, # seconds
    per_run_time_limit=30
)
automl.fit(X_train, y_train)
```

---

## 🔍 Interpretability (SHAP)

```python
import shap

# 1. Create Explainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# 2. Summary Plot (Global Importance)
shap.summary_plot(shap_values, X_test)

# 3. Waterfall Plot (Local Explanation for first row)
shap.plots._waterfall.waterfall_legacy(
    explainer.expected_value, 
    shap_values[0], 
    feature_names=X.columns
)
```

---

## ⚠️ Common Pitfalls

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| **Random Split on Time Data** | Model learns "future" trends to predict past. 99% accuracy in dev, 50% in prod. | Use `TimeSeriesSplit` or split by date (Train < Jan, Test > Jan). |
| **Grid Search Everything** | Wasted compute. Diminishing returns. | Use `RandomizedSearchCV` or `Optuna`. |
| **Leakage in CV** | Feature Engineering (like SMOTE or Scaling) done *before* splitting folds. | Use `sklearn.pipeline.Pipeline` inside CV loop. |
