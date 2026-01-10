# Day 1 Resources: AIOps Fundamentals

> **Curated list of materials and code to support your first steps in AIOps.**

---

## 🌐 Must-Read Articles & Websites

### For Absolute Beginners
*   **[AIOps for Dummies](https://www.splunk.com/en_us/form/aiops-for-dummies-v2.html)** (E-book) - Great entry point for non-technical background.
*   **[Gartner’s AIOps Market Guide](https://www.gartner.com/en/documents/4000399)** - The industry standard definition of the market.
*   **[BigPanda’s AIOps Handbook](https://www.bigpanda.io/aiops-handbook/)** - Practical insights into incident management.

### Technical Deep Dives
*   **[The SRE Book by Google](https://sre.google/sre-book/monitoring-distributed-systems/)** - Essential reading for any operations engineer.
*   **[Observability Engineering Whitepaper](https://www.honeycomb.io/whitepaper/observability-engineering)** - Why observability is the engine of AIOps.
*   **[OpenTelemetry Concepts](https://opentelemetry.io/docs/concepts/)** - Official docs on the future of data collection.

---

## 📺 Recommended Videos

*   **[AIOps Explained in 5 Minutes](https://www.youtube.com/watch?v=0kUpR-G4q54)** - Quick conceptual overview.
*   **[Observability vs. Monitoring](https://www.youtube.com/watch?v=2eGoA06zEAc)** - A critical distinction for AIOps.
*   **[SREcon Talks on AIOps](https://www.usenix.org/conferences/byname/1033)** - Technical case studies from companies like LinkedIn and Uber.

---

## 💻 Supporting Code & Scripts

These files help you understand the data patterns discussed in Day 1:

| File | Purpose |
| :--- | :--- |
| `metrics_simulator.py` | Generates seasonal CPU data for analysis. |
| `log_generator.py` | Creates mock structured JSON logs. |
| `trace_visualizer.py` | Simple CLI tool to visualize request spans. |

---

## 🎓 Daily Prerequisites: Getting Ready

To make the most of each day in Week 1, ensure you have reviewed these topics *before* starting the lecture:

### Day 1: Introduction to AIOps
*   **Understand**: What is a "server" vs "microservice"?
*   **Refresh**: Basic YAML syntax.
*   **Read**: Difference between "Metric" and "Log".

### Day 2: The Three Pillars
*   **Understand**: Distributed systems basics (HTTP requests, APIs).
*   **Refresh**: Linux `grep` and `cat` commands.
*   **Watch**: [What is a Trace ID?](https://www.youtube.com/watch?v=6PHeG89H2gM)

### Day 3: Prometheus & Grafana
*   **Understand**: What is a Time-Series Database (TSDB)?
*   **Refresh**: Basic Docker commands (`ps`, `run`, `stop`).
*   **Read**: [Prometheus Query Language (PromQL) basics](https://prometheus.io/docs/prometheus/latest/querying/basics/).

### Day 4: Instrumentation with OTel
*   **Understand**: What is an "Agent" vs "SDK"?
*   **Technical**: Basic Python function decorators/context managers.
*   **Read**: [OTel Python Getting Started](https://opentelemetry.io/docs/instrumentation/python/getting-started/).

---

## 📍 Interactive Learning Sites
*   **[PromLabs](https://promlabs.com/promql-cheat-sheet/)** - Hands-on PromQL training.
*   **[Grafana Play](https://play.grafana.org/)** - Explore production-grade dashboards.
*   **[Jaeger Demo](https://www.jaegertracing.io/docs/next-release/getting-started/#sample-app-hotrod)** - Play with distributed tracing without installing anything.
