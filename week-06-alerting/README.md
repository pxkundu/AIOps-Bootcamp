# Week 6: Intelligent Alerting & Noise Reduction

> **Theme:** From alert fatigue to actionable insights

---

## 🎯 Learning Objectives

By the end of this week, you will:

1. Build alert correlation and deduplication systems
2. Implement topology-aware root cause analysis
3. Replace static thresholds with dynamic ML-based thresholds
4. Create alert severity prediction models

---

## 📅 Daily Schedule

| Day | Topic | Duration |
|-----|-------|----------|
| 1-2 | [Alert Correlation & Deduplication](day-01-correlation/) | 8 hours |
| 3-4 | [Root Cause Analysis](day-02-rca/) | 8 hours |
| 5-6 | [Dynamic Thresholding](day-03-thresholds/) | 8 hours |
| 7 | [Alert Prioritization](day-04-prioritization/) | 4 hours |

---

## 🛠️ Technologies Covered

- **NetworkX** - Graph-based topology
- **causalnex** - Causal inference
- **Custom ML models** - Threshold learning
- **PagerDuty/Opsgenie APIs** - Alert integration

---

## ✅ Deliverables

- [ ] Alert correlation engine
- [ ] Dynamic threshold system for key metrics
- [ ] Alert severity classifier
- [ ] Week 6 quiz completed

---

## 🔑 Key Concepts

### Alert Correlation Strategies
```
Temporal Correlation    Topological Correlation    Semantic Correlation
───────────────────    ───────────────────────    ────────────────────
Same time window?      Same service/dependency?   Similar message content?
```

### Dynamic Thresholds
```
Static: if cpu > 80% → alert
Dynamic: if cpu > (baseline + 2*std) → alert

Benefits:
- Adapts to traffic patterns
- Reduces false positives  
- Handles seasonality
```

---

<p align="center">
  <a href="../week-05-predictive/">← Week 5</a> | <a href="day-01-correlation/">Start Week 6 →</a> | <a href="../week-07-remediation/">Week 7 →</a>
</p>
