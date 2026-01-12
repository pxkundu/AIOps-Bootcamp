# Real-World Project: The "Pillar-Collector" CLI

> **Build a tool that simulates the core of an AIOps ingestion engine.**

## 🎯 Project Goal
Create a Python CLI tool that can ingest CSV/JSON data, validate their "Pillar" type, and detect "Bad Data Patterns" (like High Cardinality).

---

## 🏗️ Requirements

### 1. Ingestion
- Support reading a CSV file (Metrics) and a JSONL file (Logs).
- Validate that Metrics have a `timestamp` and a `numeric value`.
- Validate that Logs have a `level`.

### 2. The "Cardinality Guard" (AIOps Feature)
- Analyze the labels/keys in the data.
- If any key has > 50% unique values compared to the total row count, flag it as **"HIGH CARDINALITY WARNING"**.
- This is exactly how production systems prevent TSDB crashes!

### 3. Correlation Logic
- If a Log entry and a Metric entry share a `timestamp` (within 1 second window), output them as a **"Correlated Event Pair"**.

---

## 📂 Folder Structure
```
day-02-pillars/project/
├── pillar_collector.py     # Your main Python script
├── data/
│   ├── sample_metrics.csv  # Use the metrics_simulator to generate
│   └── sample_logs.json    # Use the log_generator to generate
└── README.md               # User guide for your tool
```

---

## 🚀 Getting Started

1.  Use the `pandas` library for easy CSV/JSON processing.
2.  Implement a `detect_cardinality(df)` function.
3.  Simulate some "bad data" by adding a `request_id` column to a CSV to see if your tool catches it.

---

## 📊 Evaluation Rubric
- **Functionality**: Does it detect high cardinality? (50%)
- **Data Handling**: Does it correctly parse both JSON and CSV? (30%)
- **Correlation**: Does it find overlapping timestamps? (20%)

---

## 💡 Why this is important
In Week 4, we will build an automated anomaly detector. That detector *cannot work* if the data ingestion is broken or if high cardinality is slowing down the system. You are building the foundation of your AIOps platform today!
