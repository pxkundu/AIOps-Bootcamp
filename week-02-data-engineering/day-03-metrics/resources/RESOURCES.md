# Week 2 Day 3 Resources: Metrics Pipeline Design

> Curated list of documentation, tools, and reading materials to master metrics pipelines for AIOps.

---

## 📚 Essential Reading

### Metrics Fundamentals
- **[Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)** - Official Prometheus guide covering all concepts.
- **[The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/)** - Google's SRE book chapter on what to monitor.
- **[USE Method: Utilization, Saturation, Errors](https://www.brendangregg.com/usemethod.html)** - Brendan Gregg's methodology for performance monitoring.

### Metrics vs Logs vs Traces
- **[Observability: Logs, Metrics, and Traces](https://www.datadoghq.com/knowledge-center/observability-pipelines/)** - Understanding when to use each signal.
- **[The Three Pillars of Observability](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/)** - O'Reilly book on observability patterns.

---

## 🛠️ Tools & Ecosystem

### Metrics Collection
- **[Prometheus](https://prometheus.io/)** - Industry-standard metrics collection and storage.
- **[VictoriaMetrics](https://victoriametrics.com/)** - High-performance Prometheus-compatible TSDB.
- **[Grafana](https://grafana.com/)** - Visualization and alerting platform.
- **[Node Exporter](https://github.com/prometheus/node_exporter)** - System metrics exporter.

### Exporters & Instrumentation
- **[Prometheus Client Libraries](https://prometheus.io/docs/instrumenting/clientlibs/)** - Official client libraries for various languages.
- **[Prometheus Exporter Hub](https://github.com/prometheus/docs/blob/main/content/docs/instrumenting/exporters.md)** - List of community exporters.
- **[OpenTelemetry](https://opentelemetry.io/)** - Vendor-neutral observability framework.

### Streaming & Processing
- **[Apache Kafka](https://kafka.apache.org/)** - Distributed event streaming platform.
- **[Apache Flink](https://flink.apache.org/)** - Stream processing framework.
- **[Apache Spark Streaming](https://spark.apache.org/streaming/)** - Real-time data processing.

---

## 📊 Best Practices & Patterns

### Metric Design
- **[Prometheus Naming Conventions](https://prometheus.io/docs/practices/naming/)** - How to name metrics correctly.
- **[Metric and Label Naming](https://prometheus.io/docs/practices/naming/)** - Best practices for labels.
- **[Cardinality Management](https://prometheus.io/docs/practices/naming/#cardinality)** - Avoiding high-cardinality pitfalls.

### Architecture Patterns
- **[Prometheus Federation](https://prometheus.io/docs/prometheus/latest/federation/)** - Aggregating metrics from multiple Prometheus instances.
- **[Recording Rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)** - Pre-computing expensive queries.
- **[Remote Write](https://prometheus.io/docs/prometheus/latest/storage/#remote-storage-integrations)** - Long-term storage strategies.

---

## 🎓 Video Tutorials & Courses

### Getting Started
- **[Prometheus Tutorial for Beginners](https://www.youtube.com/watch?v=7gW5pSM6dlU)** - Comprehensive introduction.
- **[Grafana Dashboard Tutorial](https://www.youtube.com/watch?v=mgcJPREl3CU)** - Building effective dashboards.

### Advanced Topics
- **[Prometheus Deep Dive](https://www.youtube.com/watch?v=nDalewt4BOw)** - Internal architecture and optimization.
- **[Cardinality Explained](https://www.youtube.com/watch?v=H7zJN5q5Y8k)** - Understanding and managing cardinality.

---

## 📖 Books & Papers

### Books
- **[Prometheus: Up & Running](https://www.oreilly.com/library/view/prometheus-up-running/9781492034131/)** - O'Reilly book on Prometheus.
- **[Site Reliability Engineering](https://sre.google/books/)** - Google's SRE book (free online).

### Research Papers
- **[The Log-Structured Merge-Tree](https://www.cs.umb.edu/~poneil/lsmtree.pdf)** - Foundation of time-series databases.
- **[Time Series Databases](https://www.cs.cornell.edu/courses/cs6452/2010sp/papers/tsdb-survey.pdf)** - Survey of TSDB architectures.

---

## 🔬 Performance & Benchmarking

### Benchmarks
- **[VictoriaMetrics Benchmarks](https://victoriametrics.com/blog/2020/03/16/prometheus-benchmark-on-raspberry-pi/)** - Performance comparisons.
- **[Prometheus Scalability](https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects)** - Scaling considerations.

### Optimization
- **[Prometheus Storage Optimization](https://prometheus.io/docs/prometheus/latest/storage/)** - Storage and retention strategies.
- **[Query Optimization](https://prometheus.io/docs/prometheus/latest/querying/basics/)** - Writing efficient PromQL queries.

---

## 🤖 AIOps & Machine Learning

### Anomaly Detection
- **[Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)** - Scikit-learn documentation.
- **[Time Series Anomaly Detection](https://github.com/twitter/AnomalyDetection)** - Twitter's anomaly detection library.
- **[Prophet](https://facebook.github.io/prophet/)** - Facebook's forecasting tool.

### Feature Engineering
- **[Time Series Feature Engineering](https://www.kaggle.com/learn/time-series)** - Kaggle course on time-series features.
- **[Rolling Window Statistics](https://pandas.pydata.org/docs/user_guide/window.html)** - Pandas window functions.

---

## 🏗️ Architecture Examples

### Real-World Implementations
- **[Prometheus at SoundCloud](https://developers.soundcloud.com/blog/prometheus-at-soundcloud)** - Large-scale deployment.
- **[Prometheus at DigitalOcean](https://www.digitalocean.com/community/tutorials/an-introduction-to-metrics-monitoring-and-alerting-with-prometheus)** - Production setup guide.

### Design Patterns
- **[Microservices Monitoring](https://microservices.io/patterns/observability/application-metrics.html)** - Monitoring patterns for microservices.
- **[SLO-Based Monitoring](https://sre.google/workbook/slo-document/)** - Service Level Objectives.

---

## 💻 Code Examples & Templates

### GitHub Repositories
- **[Awesome Prometheus](https://github.com/roaldnefs/awesome-prometheus)** - Curated list of Prometheus resources.
- **[Prometheus Examples](https://github.com/prometheus/client_python/tree/master/examples)** - Python client examples.
- **[Grafana Dashboards](https://grafana.com/grafana/dashboards/)** - Community dashboard library.

### Tutorials
- **[Building a Custom Exporter](https://prometheus.io/docs/instrumenting/writing_exporters/)** - Step-by-step guide.
- **[PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/examples/)** - Query examples.

---

## 🔧 Configuration & Deployment

### Docker & Kubernetes
- **[Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)** - Kubernetes operator for Prometheus.
- **[Docker Compose Examples](https://github.com/prometheus/prometheus/tree/main/documentation/examples)** - Local development setups.

### CI/CD Integration
- **[Prometheus in CI/CD](https://prometheus.io/docs/guides/multi-target-exporter/)** - Monitoring CI/CD pipelines.
- **[GitOps for Monitoring](https://www.weave.works/blog/gitops-monitoring-prometheus-grafana)** - Managing monitoring with GitOps.

---

## 🐛 Troubleshooting & Debugging

### Common Issues
- **[Prometheus Troubleshooting](https://prometheus.io/docs/prometheus/latest/troubleshooting/)** - Official troubleshooting guide.
- **[Cardinality Explosion](https://www.robustperception.io/cardinality-is-key)** - Identifying and fixing cardinality issues.

### Tools
- **[Promtool](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/)** - Prometheus CLI tool for testing.
- **[PromLens](https://promlens.com/)** - PromQL query builder and analyzer.

---

## 📈 Monitoring Best Practices

### SRE Principles
- **[Error Budgets](https://sre.google/workbook/error-budget-policy/)** - Balancing reliability and innovation.
- **[SLI, SLO, SLA](https://sre.google/workbook/slo-document/)** - Service level definitions.

### Alerting
- **[Alerting Best Practices](https://prometheus.io/docs/practices/alerting/)** - When and how to alert.
- **[Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)** - Alert routing and grouping.

---

## 💡 Pro Tips for AIOps

1. **Start with High-Value Metrics:** Focus on business-critical metrics first (revenue, user experience).
2. **Use Recording Rules Early:** Pre-compute expensive queries to speed up dashboards.
3. **Monitor Cardinality:** Track `prometheus_tsdb_head_series` to catch cardinality explosions early.
4. **Combine Signals:** Use metrics for trends, logs for context, traces for debugging.
5. **Set Retention Policies:** Balance storage costs with query needs (hot/warm/cold storage).
6. **Test Your Alerts:** Use chaos engineering to verify alerting works correctly.

---

<p align="center">
  <a href="../lecture-notes.md">← Back to Lecture Notes</a>
</p>
