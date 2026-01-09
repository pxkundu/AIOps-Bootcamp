# Week 2: Data Engineering for AIOps

> **Theme:** Collecting, processing, and storing operational data at scale

---

## 🎯 Learning Objectives

By the end of this week, you will:

1. Design and deploy log collection pipelines (ELK/EFK stack)
2. Build custom Prometheus exporters for application metrics
3. Work with time-series databases (InfluxDB, TimescaleDB)
4. Create feature engineering pipelines for ML preparation

---

## 📅 Daily Schedule

| Day | Topic | Duration |
|-----|-------|----------|
| 1-2 | [Log Collection & Aggregation](day-01-logs/) | 8 hours |
| 3-4 | [Metrics Pipeline Design](day-02-metrics/) | 8 hours |
| 5-6 | [Time-Series Databases](day-03-tsdb/) | 8 hours |
| 7 | [Feature Engineering](day-04-features/) | 4 hours |

---

## 🛠️ Technologies Covered

- **Elasticsearch** - Log storage and search
- **Fluentd/Fluent Bit** - Log collection
- **Kafka** - Event streaming
- **InfluxDB** - Time-series database
- **Pandas** - Data processing
- **Python** - Custom exporters

---

## ✅ Deliverables

- [ ] Complete logging pipeline with structured logs
- [ ] Custom Prometheus exporter for application metrics
- [ ] Feature engineering notebook for ML preparation
- [ ] Week 2 quiz completed

---

## 🔑 Key Concepts

### Log Pipeline Architecture
```
Applications → Fluent Bit → Kafka → Logstash → Elasticsearch → Kibana
                (collect)   (buffer)  (transform)   (store)     (visualize)
```

### Feature Store Pattern
```
Raw Metrics → Feature Engineering → Feature Store → ML Models
                (aggregation,        (Redis,        (training,
                 normalization,       database)      inference)
                 lag features)
```

---

## 📁 Folder Structure

```
week-02-data-engineering/
├── README.md
├── day-01-logs/
│   ├── lecture-notes.md
│   ├── exercises/
│   └── solutions/
├── day-02-metrics/
│   ├── lecture-notes.md
│   ├── exercises/
│   └── solutions/
├── day-03-tsdb/
│   ├── lecture-notes.md
│   ├── exercises/
│   └── solutions/
├── day-04-features/
│   ├── lecture-notes.md
│   └── exercises/
└── project/
    ├── requirements.md
    └── starter-code/
```

---

## 🚀 Getting Started

```bash
cd week-02-data-engineering
# Follow Day 1 instructions
```

---

<p align="center">
  <a href="../week-01-fundamentals/">← Week 1</a> | <a href="day-01-logs/">Start Week 2 →</a> | <a href="../week-03-ml-fundamentals/">Week 3 →</a>
</p>
