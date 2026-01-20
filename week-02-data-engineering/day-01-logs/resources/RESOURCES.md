# Week 2 Day 1 Resources: Advanced Logging & Aggregation

> Curated list of documentation, tools, and reading materials to master log pipelines.

---

## 📚 Essential Reading

### Log Infrastructure
- **[The Log: What every software engineer should know about real-time data's unifying abstraction](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)** - Jay Kreps (LinkedIn). The foundational blog post for understanding logs in distributed systems.
- **[Fluent Bit Documentation](https://docs.fluentbit.io/manual/)** - Official guide for Fluent Bit.
- **[Confluent Kafka Architecture](https://developer.confluent.io/learn-kafka/architecture/logs/)** - Visualizing how Kafka handles logs as a persistence layer.

### AIOps & Logs
- **[Logs vs Metrics vs Traces (Cortex)](https://getcortexapp.com/blog/logs-vs-metrics-vs-traces)** - Why logs are the most heavy but most valuable for AI.
- **[Automated Log Analysis (Elastic)](https://www.elastic.co/guide/en/observability/current/monitor-logs.html)** - How Elasticsearch uses ML for log categorization.

---

## 🛠️ Tools & Ecosystem

### Log Shippers
- **[Fluent Bit](https://fluentbit.io/)** - Core collector we use today.
- **[Vector](https://vector.dev/)** - A high-performance Rust-based alternative for log transformation. Great benchmarks.
- **[Promtail](https://grafana.com/docs/loki/latest/send-data/promtail/)** - The agent specifically for Grafana Loki.
- **[Benthos / Redpanda Connect](https://www.benthos.dev/)** - Powerful stream processor for logs.

### Buffering & Streaming
- **[Apache Kafka](https://kafka.apache.org/)** - The industry standard buffer.
- **[Redpanda](https://redpanda.com/)** - A Kafka-compatible streaming platform written in C++ (easier to run in Docker).
- **[Amazon Kinesis](https://aws.amazon.com/kinesis/)** - Managed alternative in AWS.

---

## 🏎️ Performance & Benchmarking

- **[Fluent Bit vs. Logstash vs. Fluentd](https://logz.io/blog/fluent-bit-vs-fluentd/)** - Comparative analysis of resource usage.
- **[Vector Benchmarks](https://vector.dev/docs/about/benchmarks/)** - Visualizing the throughput limits of modern log shippers.

---

## ⚖️ Standards & Compliance (AIOps Ready)

- **[ECS (Elastic Common Schema)](https://www.elastic.co/guide/en/ecs/current/index.html)** - A common set of fields for log data. This is **essential** for building reusable AI models.
- **[OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/general/logs/)** - The future standard for log attributes.
- **[GDPR & Logging Best Practices](https://www.scalyr.com/blog/gdpr-logging-best-practices/)** - How to log without violating privacy laws.

---

## 💻 Sandbox Environments

- **[Play with Docker (Fluent Bit)](https://labs.play-with-docker.com/)** - Spin up a multi-node swarm and test Fluent Bit routing.
- **[Regex101](https://regex101.com/)** - Essential for building Fluent Bit and Logstash parsers. Select `PCRE` flavor for most collectors.

---

## 🎓 Video Tutorials

- **[Fluent Bit Hands-on](https://www.youtube.com/watch?v=kYJjC6YfH4o)** - Getting started with inputs and outputs.
- **[Kafka in 100 Seconds](https://www.youtube.com/watch?v=kP_pL4N1n8M)** - High-level conceptual overview.

---

## 💡 Pro Tips for AIOps

1. **Always Use UTC:** Never log in local time. Use ISO 8601 with Zulu time (`Z`) to avoid timezone hell during ML training.
2. **Contextual Baggage:** Propagate a `correlation_id` from your traces into every log message. This allows you to reconstruct the "STORY" of a failure.
3. **Log Rotation is NOT enough:** In AIOps, rotation deletes the history you need for long-term trend analysis. Always archive to S3/GCS.
