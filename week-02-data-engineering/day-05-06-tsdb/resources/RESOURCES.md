# Week 2 Day 5-6 Resources: Time-Series Databases

> Comprehensive guide for choosing, scaling, and optimizing your metrics storage.

---

## 📚 Official Documentation

- **[InfluxDB 2.x Documentation](https://docs.influxdata.com/influxdb/v2/)** - The definitive guide for TSM, TSI, and Flux.
- **[TimescaleDB Documentation](https://docs.timescale.com/latest/main/)** - Learning about Hypertables, Continuous Aggregates, and Compression.
- **[VictoriaMetrics Docs](https://docs.victoriametrics.com/)** - Excellent for high-performance single-node clusters.
- **[QuestDB Documentation](https://questdb.io/docs/)** - A high-performance SQL TSDB focused on low latency and high ingestion.

---

## 🏎️ Benchmarking & Performance Comparisons

- **[TSDB Benchmarking: InfluxDB vs TimescaleDB](https://www.timescale.com/blog/timescaledb-vs-influxdb-for-time-series-data-timescale-is-up-to-44x-faster/)** - A comparative study focusing on SQL vs NoSQL performance.
- **[VictoriaMetrics Benchmark (1.4 Billion Series)](https://victoriametrics.com/blog/victoriametrics-benchmark-1-4-billion-series/)** - Pushing the limits of vertical scalability.
- **[ClickHouse as a TSDB](https://clickhouse.com/docs/en/introduction/performance/)** - Understanding why some AIOps platforms use OLAP databases like ClickHouse for time-series.

---

## 🏢 Multi-Tenancy & Governance Patterns

- **[Grafana Mimir: Scalable, Multi-Tenant Prometheus](https://grafana.com/oss/mimir/)** - The industry standard for large-scale multi-tenant metrics.
- **[InfluxDB 2.x Multi-Tenancy Guide](https://docs.influxdata.com/influxdb/v2/administration/organizations/)** - Using Organizations and Buckets to isolate data.
- **[Tenancy in TimescaleDB](https://docs.timescale.com/latest/using-timescaledb/multi-tenancy/)** - Row-level security vs Schema-per-tenant patterns.

- **[Thanos: Open source, highly available Prometheus](https://thanos.io/)** - For long-term metric storage over S3.
- **[Cortex: Horizontally scalable Prometheus](https://cortexmetrics.io/)** - Distributed TSDB mostly used in large Kubernetes clusters.
- **[Benchmark: InfluxDB vs VictoriaMetrics](https://valyala.medium.com/measuring-vertical-scalability-of-influxdb-vs-victoriametrics-e1394dba8fd2)** - A classic (though biased) look at vertical scaling limits.

---

## 🛠️ Data Engineering Tools

- **[Telegraf](https://www.influxdata.com/time-series-platform/telegraf/)** - The "Swiss Army Knife" of data collection. Works with 300+ inputs.
- **[Prometheus Remote Write](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)** - The protocol that allows Prometheus to speak to InfluxDB and TimescaleDB.
- **[Grafana Infinity Data Source](https://grafana.com/docs/plugins/yesoreyeram-infinity-datasource/)** - Query any API as if it were a TSDB.

---

## 🎓 Video Deep Dives

- **[Under the Hood: How InfluxDB TSI Works](https://www.youtube.com/watch?v=FjS63iT7_M0)** - Understanding how they solved the high-cardinality problem on disk.
- **[TimescaleDB: Why SQL is better for Time-Series](https://www.youtube.com/watch?v=R96-9t3DsbE)** - A compelling argument for keeping relational features.

---

## 💡 Pro-Tips for Production

1. **The "Bucket Per Retention" Pattern:** In InfluxDB, create separate buckets for `raw`, `hourly`, and `daily` data. Each bucket should have its own retention policy.
2. **Indexing Metadata:** Never put a `random_id` in a tag. If you need it, put it in a field. This prevents your TSDB index from growing to the size of the data.
3. **Query Lookback:** Always bound your queries with a time range. `SELECT * FROM metrics` without a `WHERE time > ...` is the most common cause of database timeouts.
4. **Use Hyperfunctions:** In TimescaleDB, don't just use `AVG()`. Use `stats_agg()` or `percentile_cont()` for more robust AIOps features.
