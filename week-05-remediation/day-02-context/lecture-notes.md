# Week 5 Day 2: Context-Aware Decision Trees (Smart Triage)

> **Duration:** 8 hours | **Difficulty:** Intermediate  
> **Focus:** Replacing brittle "if-else" scripts with learned logic.

---

## 🏥 Part 1: The Problem with Rules

Yesterday (Day 1), you wrote a script:
```python
if cpu > 90:
    restart_service()
```

**What broke?**
- The Database Backup runs every night at 2 AM. It uses 95% CPU.
- Your script restarted the DB in the middle of a backup. Data Corruption.

**Context is King:**
- Is this normal behavior for this time?
- Did we just deploy code? (If so, maybe Rollback instead of Restart).
- Is the disk full? (If so, restart won't help).

---

## 🌳 Part 2: Decision Trees for SREs

A Decision Tree is a flowchart that asks sequential questions to reach a conclusion.
It mimics how a Senior Engineer debugs.

### Example Triage Tree

1.  **Is CPU > 90%?**
    - **No:** Ignore.
    - **Yes:**
        2.  **Is Time between 02:00 - 04:00?**
            - **Yes:** (Backup Window) -> **Ignore**.
            - **No:**
                3.  **Is Disk I/O High?**
                    - **Yes:** (Database Query Issue) -> **Kill Long Query**.
                    - **No:** (Runaway App) -> **Restart App**.

---

## 🤖 Part 3: From Manual Logic to Machine Learning

You *could* write 50 nested `if` statements. Or, you can **train** a Decision Tree on your incident history.

**Inputs (Features):**
- `cpu_usage` (float)
- `hour_of_day` (int)
- `is_backup_window` (bool)
- `disk_io` (float)

**Outputs (Labels/Actions):**
- `IGNORE`
- `RESTART`
- `SCALE_UP`
- `KILL_QUERY`

**Training Data:**
You take last year's incident logs.
- "On Jan 5th at 3 AM, CPU was 95%. Engineer marked as 'False Positive'."
- "On Jan 6th at 10 AM, CPU was 95%. Engineer restarted App."

The model learns: *Time matters*.

---

## 🛠️ Part 4: Building the Triage Bot

We use `scikit-learn`:

```python
from sklearn.tree import DecisionTreeClassifier

# Features: [CPU, Hour, DiskIO]
X = [[95, 3, 100],  # Backup (High CPU, 3AM, High IO)
     [95, 10, 10]]  # App Freeze (High CPU, 10AM, Low IO)

# Actions: 0=Ignore, 1=Restart
y = [0, 1]

clf = DecisionTreeClassifier()
clf.fit(X, y)

# Predict new incident
action = clf.predict([[96, 3, 110]]) 
# Output: 0 (Ignore)
```

**Pros:**
1.  **Interpretability:** You can visualize the tree. You know *why* it made the decision.
2.  **Automation:** Handles complex logic without spaghetti code.

---

## 🔗 Next Steps

1.  Open the [Cheat Sheet](cheatsheet.md) for Decision Tree code.
2.  Build a manual tree in [Exercise 01](exercises/exercise-01-manual-tree.md).
3.  Train an ML tree in [Exercise 02](exercises/exercise-02-sklearn-tree.md).
4.  Build "The Smart Doctor" in the [Project](project/README.md).
