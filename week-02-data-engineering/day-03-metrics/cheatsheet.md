# Metrics Pipeline Design Cheat Sheet

> Quick reference for building metrics pipelines in AIOps

---

## 📊 Metric Types Quick Reference

| Type | Use Case | Example | PromQL Function |
|------|----------|---------|-----------------|
| **Counter** | Always increasing | `http_requests_total` | `rate()`, `increase()` |
| **Gauge** | Can go up/down | `memory_usage_bytes` | Direct query |
| **Histogram** | Distribution | `request_duration_seconds` | `histogram_quantile()` |
| **Summary** | Pre-computed quantiles | `request_duration_seconds` | Direct query |

---

## 🔧 Prometheus Exporter (Python)

```python
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Counter
requests = Counter('http_requests_total', 'Total requests', ['method', 'status'])
requests.labels(method='GET', status='200').inc()

# Gauge
memory = Gauge('memory_usage_bytes', 'Memory usage')
memory.set(1024 * 1024 * 512)  # 512 MB

# Histogram
duration = Histogram('request_duration_seconds', 'Request duration')
with duration.time():
    # Your code here
    pass

# Start HTTP server
start_http_server(8000)
```

---

## 📝 PromQL Essentials

```promql
# Rate of change (per second)
rate(http_requests_total[5m])

# Increase over time window
increase(http_requests_total[1h])

# Percentile from histogram
histogram_quantile(0.95, 
  rate(http_request_duration_seconds_bucket[5m]))

# Aggregation
sum(rate(http_requests_total[5m])) by (status)

# Filtering
http_requests_total{status="500"}

# Mathematical operations
rate(http_requests_total[5m]) * 100
```

---

## ⚙️ Prometheus Configuration

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['localhost:8000']
    scrape_interval: 10s
    metrics_path: '/metrics'
```

---

## 🎯 Recording Rules

```yaml
groups:
  - name: api_aggregates
    interval: 30s
    rules:
      - record: api:requests:rate5m
        expr: rate(http_requests_total[5m])
      
      - record: api:latency:p95
        expr: histogram_quantile(0.95,
              rate(http_request_duration_seconds_bucket[5m]))
```

---

## 🏷️ Label Best Practices

✅ **Good Labels (Low Cardinality):**
- `method`, `status`, `endpoint`, `environment`

❌ **Bad Labels (High Cardinality):**
- `user_id`, `session_id`, `request_id`, `ip_address`

---

## 📈 Cardinality Calculation

```
Cardinality = product of all label value combinations

Example:
  method: [GET, POST] = 2
  status: [200, 404, 500] = 3
  endpoint: [/api/users, /api/orders] = 2
  
  Total = 2 × 3 × 2 = 12 time-series
```

---

## 🔄 Push vs Pull

| Model | Tool | Use Case |
|-------|------|----------|
| **Pull** | Prometheus | Long-running services |
| **Push** | Pushgateway | Batch jobs, short-lived tasks |

---

## 🚀 Quick Start: Custom Exporter

```python
#!/usr/bin/env python3
from prometheus_client import Counter, Gauge, start_http_server
import time

# Define metrics
counter = Counter('my_counter_total', 'Description')
gauge = Gauge('my_gauge', 'Description')

# Start server
start_http_server(8000)

# Update metrics
while True:
    counter.inc()
    gauge.set(time.time() % 100)
    time.sleep(1)
```

---

## 📦 Docker Compose: Prometheus Stack

```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🎨 Metric Naming Convention

```
<namespace>_<metric_name>_<unit>_<suffix>

Examples:
  http_requests_total
  http_request_duration_seconds
  node_memory_usage_bytes
  api_errors_total
```

---

## 🔍 Debugging Tips

```bash
# Check exporter endpoint
curl http://localhost:8000/metrics

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Query Prometheus
curl 'http://localhost:9090/api/v1/query?query=up'

# Check cardinality
prometheus_tsdb_head_series
```

---

## 📚 Common Patterns

### Rate Calculation
```promql
rate(metric_name[5m])  # Per second
increase(metric_name[1h])  # Total increase
```

### Error Rate
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) 
/ 
sum(rate(http_requests_total[5m]))
```

### SLO Calculation (99.9% availability)
```promql
sum(rate(http_requests_total{status!~"5.."}[5m])) 
/ 
sum(rate(http_requests_total[5m])) >= 0.999
```

---

## ⚠️ Common Pitfalls

1. **High Cardinality:** Don't use unique IDs as labels
2. **Missing `_total` suffix:** Counters should end with `_total`
3. **Wrong metric type:** Use Histogram for distributions, not Gauge
4. **No recording rules:** Expensive queries slow down dashboards
5. **Too frequent scraping:** 5s is usually enough, 1s is overkill

---

<p align="center">
  <a href="lecture-notes.md">← Back to Lecture Notes</a>
</p>
