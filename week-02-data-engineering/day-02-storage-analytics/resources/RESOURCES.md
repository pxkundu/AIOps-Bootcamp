# Week 2 Day 2 Resources: Log Analytics & Insights

> Deep dive into the technologies that power modern log analytics.

---

## 📚 Technical Documentation

### Elasticsearch & Kibana
- **[Elasticsearch Guide: Scaling and Capacity Planning](https://www.elastic.co/guide/en/elasticsearch/reference/current/scalability.html)** - Understanding shards, replicas, and nodes.
- **[Kibana Query Language (KQL) Syntax](https://www.elastic.co/guide/en/kibana/current/kuery-query.html)** - The official guide to searching in Kibana.
- **[ILM: Manage the Index Lifecycle](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)** - How to set up rollover and deletion policies.

### Grafana Loki
- **[LogQL: The Query Language of Loki](https://grafana.com/docs/loki/latest/query/)** - Comprehensive guide to stream selectors and filters.
- **[Loki Storage Backends](https://grafana.com/docs/loki/latest/operations/storage/)** - Why S3/GCS is the recommendation for Loki.

---

## 🛠️ Community Tools & Playgrounds

- **[Grok Debugger](https://grokdebug.herokuapp.com/)** - Test your Grok patterns against sample logs.
- **[Play with Kibana (Elastic Demo)](https://demo.elastic.co/)** - A live, pre-populated Kibana instance to practice your KQL skills.
- **[Grafana Play (Loki Demo)](https://play.grafana.org/d/loki-explore/loki-explore-logs)** - Live Loki explore environment.

---

## 📈 AIOps & Advanced Analytics

- **[Log Pattern Analysis (Elastic)](https://www.elastic.co/blog/how-to-group-logs-by-pattern-in-kibana)** - Using ML to cluster millions of logs into a few hundred patterns.
- **[Anomaly Detection on Logs](https://www.elastic.co/guide/en/machine-learning/current/ml-gs-logs.html)** - Configuring unsupervised ML for log message frequency.
- **[AIOps: The Future of Log Management (Gartner)](https://www.gartner.com/en/documents/3981156)** - Understanding why standard logging isn't enough for the GenAI era.

---

## 🏗️ Real-World Case Studies

- **[Uber: Scaling Logging with ELK and Kafka](https://www.uber.com/en-IN/blog/logging/)** - How Uber handles petabytes of logs per day.
- **[Cloudflare: Log Management at the Edge](https://blog.cloudflare.com/log-management-at-the-edge/)** - Using Schema-on-Read at massive scale.
- **[Pinterest: Moving from ELK to Loki](https://medium.com/pinterest-engineering/how-we-scaled-our-logging-infrastructure-7c8a6f67a21b)** - A classic example of the cost-vs-search trade-off.

---

## 🎥 Video Deep Dives

- **[Elasticsearch Internal: How Indexing Works](https://www.youtube.com/watch?v=52G5ZzcEAD8)** - Great for understanding the performance cost of Schema-on-Write.
- **[Grafana Loki: Architecture & Usage](https://www.youtube.com/watch?v=N_8q689BNoI)** - A 45-minute masterclass by the creators.
- **[AIOps: From Logs to Insights](https://www.youtube.com/watch?v=S0T0RIs0q1k)** - Practical demonstration of ML on observability data.

---

## 💡 Pro Tips for Log Storage

1. **Keywords vs Text:** In Elasticsearch, always use `keyword` for identifiers (IPs, IDs, Levels) and `text` for messages. Searching a keyword is 10x faster.
2. **Chunk Target Size:** In Loki, aim for 15-30MB chunks for optimal performance.
3. **Labels are not Fields:** In Loki, don't use labels for values that change every line (like `trace_id`). Use the `| json` parser at query time instead.
4. **Hydrate your logs:** Add `service_version` and `deployment_env` at the source. It's much harder to guess this data later.
