# Week 2 Day 4 Resources: Custom Exporters & Metrics Lab

> Advanced materials for mastering metrics engineering.

---

## 📚 Essential Documentation

- **[Prometheus: Best Practices for Instrumentation](https://prometheus.io/docs/practices/instrumentation/)** - The "Bible" of how to name and structure your metrics.
- **[Writing Exporters (Prometheus Official)](https://prometheus.io/docs/instrumenting/writing_exporters/)** - Technical guide on how an exporter should behave.
- **[Prometheus Client Python (GitHub)](https://github.com/prometheus/client_python)** - Examples and deep-dive into the library features.

---

## 🏎️ Engineering High-Performance Exporters

- **[Exporter Cardinality Management (Grafana)](https://grafana.com/blog/2022/02/15/how-to-manage-high-cardinality-metrics-with-prometheus/)** - Strategies to keep your TSDB alive.
- **[Caching in Python Exporters](https://github.com/prometheus/client_python#caching)** - How to use `CachingCollector` for slow backend APIs.
- **[The Prometheus Pushgateway](https://prometheus.io/docs/instrumenting/pushing/)** - When to use push (batch jobs) vs pull.

---

## 🛠️ Community & Tools

- **[SQL Exporter](https://github.com/free/sql_exporter)** - A generic exporter for SQL databases (use this if you don't want to write custom Python).
- **[Prometheus Relabeler (Tool)](https://relabeler.promtools.dev/)** - An interactive web tool to test your relabeling rules.
- **[CNCF Exporters List](https://prometheus.io/docs/instrumenting/exporters/)** - Don't reinvent the wheel! Check if an exporter already exists for your tool.

---

## 🎓 Video Deep Dives

- **[Deep Dive into Prometheus Relabeling](https://www.youtube.com/watch?v=52YfV3u2R0Y)** - Excellent technical walkthrough of `metric_relabel_configs`.
- **[Instrumentation 101: Counter vs Gauge](https://www.youtube.com/watch?v=mP07A6reP3M)** - Why selecting the wrong type breaks your AIOps models.

---

## 💡 Pro-Tips for "Business Observability"

1. **The "Golden Signals" of Business:** Instead of Latency/Errors/Traffic, track **Conversion/Churn/Revenue**.
2. **Aggregating at the Edge:** If you have 10,000 checkout occurrences per second, don't export each one. Use a `Counter` locally and let Prometheus scrape the aggregate.
3. **Use Annotations:** Leverage Grafana Annotations to mark deployment times on your business metrics charts. This instantly shows if a new release hurt sales.
