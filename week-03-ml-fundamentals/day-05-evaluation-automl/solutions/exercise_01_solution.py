# Solution for Exercise 01: Tuning and Explaining Models
# Week 3 Day 5

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
import optuna
import shap
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. GENERATE DATA
# ---------------------------------------------------------
print("Generating data...")
X, y = make_classification(
    n_samples=2000, 
    n_features=20, 
    n_informative=3, # Only 3 features actually matter!
    n_redundant=2, 
    n_classes=2, 
    weights=[0.9, 0.1], # Imbalanced (10% target)
    random_state=42
)

feature_names = [f"feature_{i}" for i in range(20)]

# ---------------------------------------------------------
# 2. BASELINE EVALUATION
# ---------------------------------------------------------
print("\n--- Baseline Evaluation ---")
baseline_model = RandomForestClassifier(random_state=42, class_weight='balanced')
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
baseline_scores = cross_val_score(baseline_model, X, y, cv=cv, scoring='f1')

print(f"Baseline F1 Score: {baseline_scores.mean():.4f} (+/- {baseline_scores.std():.4f})")

# ---------------------------------------------------------
# 3. OPTUNA TUNING
# ---------------------------------------------------------
print("\n--- Optuna Tuning (Running 20 trials) ---")
optuna.logging.set_verbosity(optuna.logging.WARNING) # Shhh

def objective(trial):
    n_estimators = trial.suggest_int('n_estimators', 50, 300)
    max_depth = trial.suggest_int('max_depth', 3, 30)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
    
    clf = RandomForestClassifier(
        n_estimators=n_estimators, 
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42,
        class_weight='balanced'
    )
    
    # Use 3-fold for faster search
    scores = cross_val_score(clf, X, y, cv=3, scoring='f1')
    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=20)

print("Best Parameters:", study.best_params)
print(f"Best Tuned F1 Score: {study.best_value:.4f}")

# ---------------------------------------------------------
# 4. SHAP EXPLANATION
# ---------------------------------------------------------
print("\n--- SHAP Explanation ---")
print("Training final model with best parameters...")
best_model = RandomForestClassifier(**study.best_params, random_state=42, class_weight='balanced')
best_model.fit(X, y)

explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X)

print("Plotting SHAP summary (close window to finish)...")
# Note: shap_values[1] is for the positive class (failure)
shap.summary_plot(shap_values[1], X, feature_names=feature_names)

# Insight Check
# Since n_informative=3, we expect 3 features to dominate.
# Check feature importance manually if plot doesn't show
importances = best_model.feature_importances_
indices = np.argsort(importances)[::-1]
print("\nTop 5 Feature Importances found by RF:")
for f in range(5):
    print(f"{feature_names[indices[f]]}: {importances[indices[f]]:.4f}")
