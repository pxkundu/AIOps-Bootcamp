# Metrics Engineering & Exporter Cheat Sheet

> Master the implementation of custom metrics and Prometheus relabeling.

---

## 🐍 Python `prometheus_client` SDK

### 1. The Four Metric Types
```python
from prometheus_client import Counter, Gauge, Histogram, Summary

# Counter: Only goes UP (e.g. Total Requests)
c = Counter('app_requests_total', 'Total app requests', ['method', 'endpoint'])
c.labels(method='get', endpoint='/api').inc()

# Gauge: Goes up and down (e.g. Memory, Active Threads)
g = Gauge('app_active_users', 'Current active users')
g.set(42)  # Set to specific value
g.inc()    # Increment by 1
g.dec(10)  # Decrement by 10

# Histogram: Sample observations (e.g. Latency)
h = Histogram('app_latency_seconds', 'Request latency', buckets=[0.1, 0.5, 1.0, 5.0])
h.observe(0.42)

# Summary: Similar to Histogram, but calculates quantiles on-the-fly
s = Summary('app_obj_size_bytes', 'Object size')
s.observe(1024)
```

### 2. Running the HTTP Server
```python
from prometheus_client import start_http_server

if __name__ == '__main__':
    # Start exporter on port 8000
    start_http_server(8000)
    while True:
        process_data()
```

---

## ⚙️ Prometheus Relabeling (`relabel_configs`)
Happens *before* the scrape. Usually used for metadata.

### Drop a Target
```yaml
scrape_configs:
  - job_name: 'no-dev'
    static_configs:
      - targets: ['localhost:9090', 'dev-server:9090']
    relabel_configs:
      - source_labels: [__address__]
        regex: 'dev-.*'
        action: drop
```

## 🏷️ Metric Relabeling (`metric_relabel_configs`)
Happens *after* the scrape. Used for pruning labels/metrics.

### Drop a Label (High Cardinality)
```yaml
    metric_relabel_configs:
      - regex: 'user_agent|session_id'
        action: labeldrop
```

### Standardizing Labels
```yaml
    metric_relabel_configs:
      - source_labels: [service_name]
        target_label: service
        action: replace
```

---

## 📊 Naming Conventions (AIOps Ready)
- **Use base units:** `seconds`, `bytes`, `meters`.
- **Suffix with type:** `_total` (for counters), `_created` (auto-added).
- **Scale:** Prefer `seconds` over `milliseconds` to avoid confusion.
- **Naming example:** `http_request_duration_seconds`

---

## 🚨 Cardinality Warning Signs
- If `count(count by(__name__) ({__name__=~".+"}))` exceeds 10,000 for a single job.
- If Grafana queries feel "heavy" or slow to load.
- If your TSDB WAL (Write Ahead Log) is filling up disk rapidly.
- **Diagnosis Query:** `topk(10, count by (__name__) ({__name__=~".+"}))`
