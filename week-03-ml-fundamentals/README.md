# Week 3: Machine Learning Fundamentals for Operations

> **Theme:** Building ML intuition with operations data

---

## 🎯 Learning Objectives

By the end of this week, you will:

1. Apply supervised and unsupervised learning to operational data
2. Perform time-series analysis and decomposition
3. Build log classification models
4. Evaluate models and set up MLOps practices

---

## 📅 Daily Schedule

| Day | Topic | Duration |
|-----|-------|----------|
| 1 | [Statistical Foundations for AIOps](day-01-stats/) | 8 hours |
| 2 | [Ops EDA & Preprocessing](day-02-eda/) | 8 hours |
| 3 | [Supervised Learning: Predicting Impact](day-03-supervised/) | 8 hours |
| 4 | [Unsupervised Learning: Pattern Discovery](day-04-unsupervised/) | 8 hours |
| 5 | [NLP for Log Intelligence](day-05-nlp-logs/) | 8 hours |
| 6 | [Time-Series Basics for Forecasting](day-06-timeseries-intro/) | 8 hours |
| 7 | [MLOps & Model Evaluation in Ops](day-07-mlops-eval/) | 8 hours |

---

## 🛠️ Technologies Covered

- **scikit-learn** - Core ML algorithms
- **statsmodels** - Statistical modeling
- **MLflow** - Experiment tracking
- **Jupyter** - Interactive development
- **pandas/numpy** - Data manipulation

---

## ✅ Deliverables

- [ ] Time-series analysis of application metrics
- [ ] Log classification model with evaluation report
- [ ] MLflow experiment tracking setup
- [ ] Week 3 quiz completed

---

## 🔑 Key Concepts

### ML Pipeline for AIOps
```
Data Collection → Preprocessing → Feature Engineering → Model Training → Evaluation → Deployment
```

### Model Selection Guide
| Problem | Algorithm | Use Case |
|---------|-----------|----------|
| Severity classification | Random Forest | Log classification |
| Anomaly detection | Isolation Forest | Metric anomalies |
| Forecasting | ARIMA, Prophet | Capacity planning |
| Clustering | DBSCAN, K-Means | Log pattern mining |

---

## 📁 Folder Structure

```
week-03-ml-fundamentals/
├── README.md
├── THE-ORACLE-QUEST.md
├── LAUNCH-QUEST.py
├── day-01-stats/
│   ├── lecture-notes.md
│   ├── cheatsheet.md
│   ├── exercises/
│   ├── resources/
│   └── project/
├── day-02-eda/
├── day-03-supervised/
├── day-04-unsupervised/
├── day-05-nlp-logs/
├── day-06-timeseries-intro/
└── day-07-mlops-eval/
```

---

<p align="center">
  <a href="../week-02-data-engineering/day-05-06-tsdb/lecture-notes.md">⬅️ Back: Week 2</a> | <strong>Week 3 Overview</strong> | <a href="day-01-stats/lecture-notes.md">Start Week 3 ➡️</a>
</p>
