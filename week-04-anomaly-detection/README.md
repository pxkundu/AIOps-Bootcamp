# Week 4: Anomaly Detection & Log Analytics

> **Theme:** Detecting the unknown unknowns in your systems

---

## 🎯 Learning Objectives

By the end of this week, you will:

1. Implement statistical anomaly detection (Z-score, IQR, EWMA)
2. Build ML-based anomaly detectors (Isolation Forest, Autoencoders)
3. Perform log pattern mining with Drain3
4. Create real-time anomaly detection pipelines

---

## 📅 Daily Schedule

| Day | Topic | Duration |
|-----|-------|----------|
| 1-2 | [Statistical Anomaly Detection](day-01-statistical/) | 8 hours |
| 3-4 | [ML-based Anomaly Detection](day-02-ml-anomaly/) | 8 hours |
| 5-6 | [Log Pattern Mining & NLP](day-03-log-analytics/) | 8 hours |
| 7 | [Real-time Anomaly Detection](day-04-streaming/) | 4 hours |

---

## 🛠️ Technologies Covered

- **PyOD** - Outlier detection library
- **Drain3** - Log parsing
- **Kafka + Faust** - Stream processing
- **TensorFlow/PyTorch** - Autoencoders
- **spaCy** - NLP for logs

---

## ✅ Deliverables

- [ ] Anomaly detection pipeline for system metrics
- [ ] Log clustering and pattern extraction system
- [ ] Real-time anomaly alerting prototype
- [ ] Week 4 quiz completed

---

## 🔑 Key Concepts

### Anomaly Detection Methods
```
Statistical           ML-Based              Deep Learning
──────────           ────────              ─────────────
• Z-score            • Isolation Forest    • Autoencoders
• IQR                • One-Class SVM       • LSTM
• EWMA               • LOF                 • Transformers
• Seasonal decomp    • DBSCAN              • VAE
```

### Log Analytics Pipeline
```
Raw Logs → Parsing (Drain3) → Clustering → Pattern Mining → Anomaly Detection
```

---

<p align="center">
  <a href="../week-03-ml-fundamentals/day-05-evaluation-automl/lecture-notes.md">⬅️ Back: Week 3</a> | <strong>Week 4 Overview</strong> | <a href="day-01-statistical/lecture-notes.md">Start Day 1 ➡️</a>
</p>
