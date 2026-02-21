# Week 6 Day 3 Resources: Prometheus, Grafana, & AIOps

Advance your PromQL skills with these industry resources.

---

## 📚 Essential Reading
- **[Prometheus: Querying Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)** - Official guide to vectors and ranges.
- **[Statistical Monitoring (Blog)](https://www.robustperception.io/using-standard-deviation-to-detect-outliers/)** - How to use `stddev_over_time` effectively.
- **[Google SRE Book: Alerting](https://sre.google/sre-book/monitoring-distributed-systems/)** - Why you should alert on symptoms, not causes.

---

## 🛠️ Tools & Dashboards
- **[Grafana Play](https://play.grafana.org/)** - Explore advanced dashboard techniques without an installation.
- **[PromLens](https://promlens.com/)** - An advanced PromQL query builder and analyzer (now part of Prometheus).
- **[Awesome Prometheus](https://github.com/roaldnefs/awesome-prometheus)** - A curated list of exporters, dashboards, and tools.

---

## 🎓 Advanced PromQL Cheat Sheet

| Task | PromQL Fragment |
|---|---|
| **Moving Average** | `avg_over_time(metric[1h])` |
| **Outlier (Z-Score)** | `(metric - avg_over_time(metric[1h])) / stddev_over_time(metric[1h])` |
| **Prediction (4h)** | `predict_linear(metric[1h], 4 * 3600)` |
| **Change Rate** | `delta(metric[1h])` |

---

## 💡 Pro Tips for The Self-Adjusting Sentinel
1.  **Warm-up History:** Statistical alerts need at least 1-2 hours of data before they become accurate. Don't enable them on a brand new cluster immediately.
2.  **Filter Noise:** Always use `rate()` or `irate()` for counter metrics before applying averages.
3.  **Combine Rules:** Use a static "Sanity Check" (e.g., Latency < 10s) alongside dynamic rules to catch extreme failures that might break the statistics.
