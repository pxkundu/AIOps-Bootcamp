# Week 3 Day 4 Project: The Silent Anomaly Hunter

> **Challenge:** Detecting "loud" failures (like a crash) is easy. Your mission is to detect "silent" failures—subtle deviations in system behavior that signal an impending doom, using Unsupervised Learning that requires NO labeled data.

---

## 🎯 Objective
Build an **Unsupervised Anomaly Detection System** that analyzes a multi-dimensional stream of server metrics to flag unusual behavior.

**Key Requirements:**
1. **Ingest** simulated metric data (CPU, Memory, Disk IO, Network).
2. **Train** an Isolation Forest or One-Class SVM on "healthy" baseline data.
3. **Detect** anomalies in a separate "live" stream containing hidden issues.
4. **Visualize** the anomalies using dimensionality reduction (PCA/t-SNE).

---

## 📂 Project Structure

```
silent-anomaly-hunter/
├── data/
│   ├── generate_data.py      # Script to create synthetic healthy/unhealthy data
│   ├── baseline_metrics.csv  # Generated healthy data
│   └── live_metrics.csv      # Generated data with hidden anomalies
├── src/
│   ├── train_model.py        # Script to train and save the detector
│   ├── detect.py             # Script to run detection on live data
│   └── visualize.py          # Script to plot PCA results
├── notebook/
│   └── exploration.ipynb     # Prototyping and analysis
├── requirements.txt
└── README.md
```

---

## 🛠️ Step 1: Data Generation (`data/generate_data.py`)

We need a sophisticated generator. "Healthy" data usually follows daily patterns. "Anomalous" data might drift slowly.

```python
import pandas as pd
import numpy as np

def generate_metrics(n_samples=1000, state='healthy'):
    np.random.seed(42 if state=='healthy' else 99)
    
    # Baseline healthy behavior
    cpu = np.random.normal(30, 10, n_samples)
    mem = np.random.normal(40, 5, n_samples)
    disk = np.random.gamma(2, 2, n_samples)
    
    if state == 'anomalous':
        # Introduce a "Memory Leak" pattern: Correlation breakage
        # Normal: CPU goes up, Mem goes up. 
        # Anomaly: CPU stays low, Mem creeps up.
        mem = np.linspace(40, 90, n_samples) + np.random.normal(0, 2, n_samples)
        cpu = np.random.normal(30, 5, n_samples) # CPU stays flat
        
    df = pd.DataFrame({
        'cpu': cpu, 'memory': mem, 'disk_io': disk
    })
    return df

# Generate
baseline = generate_metrics(2000, 'healthy')
baseline.to_csv('baseline_metrics.csv', index=False)

live = pd.concat([
    generate_metrics(500, 'healthy'),
    generate_metrics(200, 'anomalous'), # The silent leak
    generate_metrics(300, 'healthy')
])
live.to_csv('live_metrics.csv', index=False)
```

**Run this first** to create your dataset.

---

## 🛠️ Step 2: Model Training (`src/train_model.py`)

Train your model ONLY on the `baseline` data. This simulates learning "normalcy".

1. Load `baseline_metrics.csv`.
2. Preprocess (Scale data! Important for distance-based ML).
3. Train `IsolationForest` (or `LocalOutlierFactor` for novelty detection).
4. Save the model and the scaler using `joblib`.

---

## 🛠️ Step 3: Detection (`src/detect.py`)

Load your trained model and run it against `live_metrics.csv`.

1. Load model & scaler.
2. Load `live_metrics.csv`.
3. Predict anomalies (-1).
4. Output the results.
5. **Bonus:** Calculate a "Severity Score" using `model.decision_function()`. The more negative, the worse the anomaly.

---

## 🛠️ Step 4: Visualization (`src/visualize.py`)

Since we have 3 dimensions (CPU, Mem, Disk), we can plot 3D, or use PCA to project to 2D.

1. Use `PCA(n_components=2)` to reduce dimensionality.
2. Scatter plot the points.
3. Color code them: **Blue** for Normal, **Red** for Detected Anomaly.

Does the "Anomalous" cluster separate clearly?

---

## 🚀 Deliverables

1. **Python Scripts**: The complete working pipeline (`generate`, `train`, `detect`, `visualize`).
2. **Report (Markdown)**: 
   - How many anomalies did you catch?
   - Did you catch the "Memory Leak" (samples 500-700)?
   - Which feature contributed most to the anomaly? (Hint: Interpreting Isolation Forest is tricky, but check the raw values of the flagged rows).

## 🌟 Advanced Extensions
- **Real-time Simulation**: Instead of reading a CSV, make `detect.py` accept a single JSON object via an argument or API, and pipe data into it.
- **Auto-Encoder**: Replace Isolation Forest with a Neural Network Auto-Encoder (Train to reconstruct input; high reconstruction error = anomaly).

Good hunting, Predictor! 🕵️‍♂️
