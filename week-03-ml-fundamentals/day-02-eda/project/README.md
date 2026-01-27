# Day 2 Project: The Data Refinery 🧪

> **Challenge:** Build a reusable Python class that automates the "Refining" (cleaning and feature engineering) of messy Prometheus/Loki data for downstream ML model training.

---

## 🎯 Project Scenario
Your AIOps team is frequently building new models. Every time, they spend 90% of their time writing the same cleaning code. You have been tasked with building the **Data Refinery Engine**—a modular pipeline that takes raw, dirty operational CSVs and outputs "ML-Ready" feature matrices.

---

## 🏗️ Project Requirements

### 1. The Refinery Class (`refinery.py`)
Build a class named `OpsDataRefinery` that implements the following methods:

-   `load_data(file_path)`: Loads metrics, sets index to datetime, and sorts.
-   `handle_missing(strategy='interpolate')`: Automatically fills gaps based on the chosen strategy.
-   `remove_noise(window=3)`: Applies a rolling mean to smooth jitter.
-   `engineer_features()`: 
    -   Adds cyclic time features (sin/cos).
    -   Adds an `is_working_hours` binary flag.
    -   Adds `lag_features` (e.g., `cpu_5m_ago`).
-   `scale_features()`: Standardizes all numeric columns.
-   `export(file_path)`: Saves the cleaned, refined dataframe.

### 2. The Stress Test Dataset
Create a script `generate_dirty_data.py` that generates a CSV with:
-   Column `latency`: Highly skewed with 5% missing values and 2% extreme spikes (outliers).
-   Column `cpu`: 0-100% with random jitter.
-   Timestamp index with frequent "gaps" (missing rows).

### 3. Validation Runner
Create a script `test_refinery.py` that:
1.  Loads the dirty data.
2.  Runs the full refinery pipeline.
3.  Checks that the output has **0 missing values**.
4.  Logs the **Mean and Variance** of the final feature set (should be ~0 and ~1).

---

## 📋 Evaluation Rubric

| Criteria | Points |
|----------|--------|
| **Robustness:** Handles missing files, empty columns, and non-numeric data gracefully. | 30 |
| **Logic:** Correct implementation of Cyclic Encoding and Lag Features. | 30 |
| **Clean Code:** Code is readable, well-commented, and follows PEP8. | 20 |
| **Innovation:** Implement an `automated_outlier_cap` that uses IQR to clip values. | 20 |

---

## 📤 Submission
Submit your `refinery.py`, `generate_dirty_data.py`, and the resulting `refined_metrics.csv`.
