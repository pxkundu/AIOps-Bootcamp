# Day 2 Resources: Deep Dive into the Three Pillars

> **Advanced materials for mastering Metrics, Logs, and Traces.**

---

## 🌐 Websites & Interactive Materials

### Metrics & Cardinality
*   **[Prometheus Documentation: Metric Types](https://prometheus.io/docs/concepts/metric_types/)** - The official guide to Counter, Gauge, Histogram, and Summary.
*   **[Robust Perception: Subleties in Metrics](https://www.robustperception.io/blog/)** - Excellent blog post series on technical nuances of Prometheus.
*   **[Cardinality Explorer](https://demo.promlens.com/)** - Use PromLens to visualize how labels increase series count.

### Logging Best Practices
*   **[The 12-Factor App: Logs](https://12factor.net/logs)** - Why logs should be treated as event streams.
*   **[JSON Logging Guide](https://sematext.com/blog/structured-logging/)** - Practical tips for moving from plain text to JSON.

### Distributed Tracing
*   **[OpenTelemetry: Context Propagation](https://opentelemetry.io/docs/concepts/context-propagation/)** - How Trace IDs travel through your stack.
*   **[Lightstep: Learning Center](https://lightstep.com/observability/)** - High-quality videos and articles on tracing.

---

## 📖 Deep Dive Reading

*   **[Logs vs. Metrics](https://peter.bourgon.org/blog/2017/02/21/metrics-logs-and-traces.html)** by Peter Bourgon - The seminal post that popularized the "Three Pillars" concept.
*   **[Distributed Tracing in Practice](https://www.oreilly.com/library/view/distributed-tracing-in/9781492056621/)** (O'Reilly) - Chapter 1 & 2 cover the fundamental architecture.

---

## 💻 Learning Tools

*   **[Online Regex Tester](https://regex101.com/)** - Essential for when you *must* parse unstructured logs.
*   **[JSONLint](https://jsonlint.com/)** - Validate your structured log formats.
*   **[Mermaid Live Editor](https://mermaid.live/)** - Practice drawing your own sequence diagrams for traces.

---

## 🎓 Next Steps: Preparation for Day 3
Tomorrow, we will deploy a full stack. To prepare:
1.  Read about **[Docker Compose Networking](https://docs.docker.com/compose/networking/)**.
2.  Refresh your knowledge of **[Prometheus Scraping](https://prometheus.io/docs/introduction/first_steps/#configuring-prometheus-to-monitor-itself)**.

---

<p align="center">
  <a href="../lecture-notes.md">Back to Lecture Notes</a>
</p>
