# Solution for Exercise 02: The Learned Triage
# Week 5 Day 2

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
import joblib
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. GENERATE SYNTHETIC DATA
# ---------------------------------------------------------
print("Generating 1000 incident logs...")
np.random.seed(42)

# Features
n_samples = 1000
cpu = np.random.randint(0, 100, n_samples)
mem = np.random.randint(0, 100, n_samples)
hour = np.random.randint(0, 24, n_samples)
is_deploy = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])
# Backup Window: 2AM - 4AM
is_backup = ((hour >= 2) & (hour <= 4)).astype(int)

# Labels (Action Logic)
# 0: IGNORE
# 1: SCALE_UP
# 2: ROLLBACK
# 3: RESTART
# 4: ESCALATE (Default)

actions = []
for i in range(n_samples):
    # Rule 1: Backup (High CPU) -> Ignore
    if is_backup[i] == 1 and cpu[i] > 80:
        actions.append(0) # IGNORE
    # Rule 2: Normal High CPU -> Scale Up
    elif is_backup[i] == 0 and cpu[i] > 80:
        actions.append(1) # SCALE_UP
    # Rule 3: Deploy Failure (High Mem) -> Rollback
    elif is_deploy[i] == 1 and mem[i] > 80:
        actions.append(2) # ROLLBACK
    # Rule 4: Normal Mem Leak -> Restart
    elif is_deploy[i] == 0 and mem[i] > 80:
        actions.append(3) # RESTART
    else:
        actions.append(4) # ESCALATE

# Create DataFrame
df = pd.DataFrame({
    'cpu': cpu,
    'mem': mem,
    'hour': hour,
    'is_backup': is_backup,
    'is_deploy': is_deploy,
    'action': actions
})

# Save CSV
df.to_csv('triage_history.csv', index=False)
print("Saved triage_history.csv")

# ---------------------------------------------------------
# 2. TRAIN MODEL
# ---------------------------------------------------------
print("Training Semantic Decision Tree...")

X = df[['cpu', 'mem', 'is_backup', 'is_deploy']] # Ignoring 'hour' as 'is_backup' captured it
y = df['action']

clf = DecisionTreeClassifier(max_depth=4, random_state=42)
clf.fit(X, y)

# Save Model
joblib.dump(clf, 'doctor_model.pkl')
print("Saved doctor_model.pkl")

# ---------------------------------------------------------
# 3. VISUALIZE LOGIC
# ---------------------------------------------------------
tree_rules = export_text(clf, feature_names=['cpu', 'mem', 'is_backup', 'is_deploy'])
print("\n--- Learned Logic ---")
print(tree_rules)

# Insight Check
# Look for: "is_backup > 0.5" near the top.
# This proves the model learned "Context Context Matters".
