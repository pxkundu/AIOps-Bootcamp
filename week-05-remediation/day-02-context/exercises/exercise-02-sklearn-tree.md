# Exercise 02: The Learned Triage (Scikit-Learn)

## 🎯 Objective
Instead of writing 100 `if` statements, **Train** a Decision Tree to learn the triage rules from historical data. This is creating a "Machine Learning Based Expert System".

---

## 📊 The Data
You have a history of 1,000 incidents.
- **Features (Input):**
    - `cpu_percent` (0-100)
    - `memory_percent` (0-100)
    - `is_backup_hour` (0 or 1)
    - `is_deploy_running` (0 or 1)
- **Labels (Output / Correct Action):**
    - 0: `IGNORE` (False Alarm)
    - 1: `RESTART`
    - 2: `SCALE_UP`

**The Hidden Rules (Ground Truth):**
- If `backup=1`, Action is `IGNORE` (regardless of CPU).
- If `backup=0` AND `cpu > 80`, Action is `SCALE_UP`.
- If `mem > 80` AND `deploy=0`, Action is `RESTART`.

## 🛠️ Task 1: Generate History
Write a script `triage_trainer.py` that generates 1,000 samples based on the "Hidden Rules" above (with some noise). save as `triage_history.csv`.

```python
import pandas as pd
import numpy as np
# ... logic ...
```

## 🛠️ Task 2: Train the Model
Use `DecisionTreeClassifier`.
1.  Load `triage_history.csv`.
2.  Split into `X` (Features) and `y` (Action).
3.  `clf.fit(X, y)`.

## 🛠️ Task 3: Visualize the Logic
Use `export_text` (see Cheat Sheet).
Does the tree reflect the "Hidden Rules"?
- Does the root node check `is_backup_hour`? (It should, because backup overrides everything).

## 📝 Deliverable
A Python script `triage_trainer.py` that outputs the tree visualization.
