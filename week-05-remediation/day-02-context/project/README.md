# Week 5 Day 2 Project: The Smart Doctor 🩺

> **Challenge:** You are the On-Call Engineer. Incidents are flooding in. Use Machine Learning to automatically triage them based on context (Time, Deploy, Backup).

---

## 🎯 Objective
Create an Intelligent Triage Bot (`doctor.py`) that:
1.  **Learns** the historical patterns of your system (Training Phase).
2.  **Diagnoses** new incidents in real-time.
3.  **Prescribes** the correct action (Ignore, Restart, Rollback).

---

## 📂 Project Structure

```
smart-doctor/
├── data/
│   └── triage_history.csv  # Historical logs (You generate this)
├── src/
│   ├── doctor.py           # The detection logic
│   └── trainer.py          # The training script
└── README.md
```

## 🛠️ Step 1: Generate History (`data/triage_history.csv`)

Create 1,000 synthetic incident logs with these **Ground Truth Rules**:
1.  **Backup Window (2AM-4AM):** Always action `IGNORE`.
2.  **Deploy Window (Is Deploying=True):** If CPU > 80, action `ROLLBACK`.
3.  **Normal Time:**
    - If Mem > 90, action `RESTART`.
    - If CPU > 90, action `SCALE_UP`.
    - Else `Escalate`.

## 🛠️ Step 2: Train the Brain (`src/trainer.py`)

A script that:
1.  Loads `triage_history.csv`.
2.  Trains a `DecisionTreeClassifier`.
3.  Saves it to `doctor_model.pkl` using `joblib`.
4.  Visualizes the tree (`export_text`) to confirm logic.

## 🛠️ Step 3: The Doctor (`src/doctor.py`)

A class `SmartDoctor` that:
1.  Loads `doctor_model.pkl` on init.
2.  Has a method `predict(incident)`:
    - Takes `{'cpu': 95, 'hour': 3, ...}`
    - Returns `"IGNORE"` (mapped from class ID).

## 🚀 Twist: Drift!
After running perfectly for 100 incidents, the "Backup Window" changes from 2AM to 3AM.
Watch your model fail.
**Task:** Retrain your model with new data to handle the change. (This is MLOps).

## 📝 Deliverable
Run `python run_simulation.py` (provided solution). It must achieve 100% accuracy on the test set.
