# Week 1: AIOps Fundamentals & Observability Stack

> **Theme:** Understanding the AIOps landscape and building your observability foundation

---

## 🎯 Learning Objectives

By the end of this week, you will:

1. Understand what AIOps is and its role in modern IT operations
2. Explain the three pillars of observability (metrics, logs, traces)
3. Deploy a complete observability stack (Prometheus + Grafana + Jaeger)
4. Instrument an application using OpenTelemetry
5. Compare major industry observability tools

---

## 📅 Daily Schedule

| Day | Topic | Duration |
|-----|-------|----------|
| 1-2 | [Introduction to AIOps](day-01-intro/) | 8 hours |
| 3-4 | [Observability Stack Setup](day-02-observability/) | 8 hours |
| 5-6 | [OpenTelemetry & Instrumentation](day-03-instrumentation/) | 8 hours |
| 7 | [Industry Tools Landscape](day-04-tools/) | 4 hours |

---

## 🛠️ Technologies Covered

- **Prometheus** - Metrics collection and alerting
- **Grafana** - Visualization and dashboards
- **Jaeger** - Distributed tracing
- **OpenTelemetry** - Observability instrumentation
- **Docker** - Containerization
- **Python** - Application development

---

## ✅ Deliverables

By the end of Week 1, you should have:

- [ ] Personal AIOps learning repo set up
- [ ] Running observability stack locally
- [ ] Instrumented sample application with metrics/traces
- [ ] First Grafana dashboard created
- [ ] Completed Week 1 quiz

---

## 📁 Folder Structure

```
week-01-fundamentals/
├── README.md                  # This file
├── day-01-intro/              # Introduction to AIOps
│   ├── lecture-notes.md
├── day-01-intro/             # AIOps intro & Environment setup
├── day-02-pillars/           # Three Pillars Deep Dive (Metrics/Logs/Traces)
├── day-03-stack/             # Hands-on: Prometheus, Grafana, Jaeger
├── day-04-instrumentation/   # OpenTelemetry & App instrumentation
├── day-05-tools/             # Industry tools (Datadog, etc.)
└── project/                  # Week 1 mini-project
    ├── requirements.md
    └── starter-code/
```

---

## 🚀 Getting Started

1. Ensure you've completed [Prerequisites](../PREREQUISITES.md)
2. Set up your development environment:
   ```bash
   cd week-01-fundamentals
   docker --version  # Ensure Docker is running
   python --version  # Should be 3.10+
   ```
3. Start with [Day 1: Introduction](day-01-intro/lecture-notes.md)

---

## 📚 Additional Resources

- [PromQL Cheatsheet](../resources/cheatsheets/promql-cheatsheet.md)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)

---

<p align="center">
  <a href="../PREREQUISITES.md">⬅️ Back: Prerequisites</a> | <strong>Week 1 Overview</strong> | <a href="day-01-intro/lecture-notes.md">Start Day 1 ➡️</a>
</p>
