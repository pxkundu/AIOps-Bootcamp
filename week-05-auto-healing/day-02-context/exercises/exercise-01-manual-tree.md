# Exercise 01: The Manual Triage (Python Logic)

## 🎯 Objective
Write a Python function that uses **Context** (Time, Backup Status, Recent Deploys) to choose the correct remediation action. This is creating a "Decision Tree" manually.

---

## 📊 The Simulation
Imagine you are the On-Call Engineer for a critical payment system.
Incidents arrive as a dictionary:
```python
incident = {
    'cpu_usage': 95,      # %
    'memory_usage': 40,   # %
    'disk_io': 100,       # MB/s
    'hour': 3,            # 0-23
    'backup_running': True, 
    'deploy_running': False
}
```

## 🛠️ Task 1: Define the Rules

Write a function `diagnose(incident)` that applies these rules:
1.  **If CPU > 90% AND Backup is Running:** -> Returns `"IGNORE"` (It's normal).
2.  **If CPU > 90% AND Backup NOT Running:** -> Returns `"SCALE_UP"`.
3.  **If Memory > 90% AND Deploy is Running:** -> Returns `"ROLLBACK"`.
4.  **If Memory > 90% AND Deploy NOT Running:** -> Returns `"RESTART_SERVICE"`.
5.  **Else:** -> Returns `"Escalate to Human"`.

## 🛠️ Task 2: Test It

Create a test script that passes these cases:
- `{cpu: 95, hour: 3, backup: True}` -> IGNORE
- `{cpu: 95, hour: 10, backup: False}` -> SCALE_UP
- `{mem: 95, deploy: True}` -> ROLLBACK

## 📝 Deliverable
A Python script `manual_triage.py` that passes all test cases.
