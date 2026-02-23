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
| 1 | [Datadog Alerting & Correlation](day-01-datadog/) | 8 hours |
| 2 | [Dynatrace Davis AI & RCA](day-02-dynatrace/) | 8 hours |
| 3 | [Grafana & Prometheus Thresholds](day-03-grafana-prom/) | 8 hours |
| 4 | [Topology-Aware RCA (NetworkX)](day-04-topology-rca/) | 8 hours |
| 5 | [Probabilistic RCA & Causality](day-05-causality/) | 8 hours |
| 6 | [Alert Prioritization & Scoring](day-06-prioritization/) | 8 hours |
| 7 | [Incident Management Integration](day-07-ops-integration/) | 4 hours |

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
  <a href="../week-05-remediation/day-05-capstone/lecture-notes.md">⬅️ Back: Week 5</a> | <strong>Week 6 Overview</strong> | <a href="day-01-datadog/lecture-notes.md">Start Week 6 ➡️</a>
</p>
