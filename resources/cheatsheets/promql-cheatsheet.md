# PromQL Cheatsheet

Quick reference for Prometheus Query Language.

---

## Basic Selectors

```promql
# Select metric by name
http_requests_total

# With label filter
http_requests_total{job="api-server"}

# Multiple labels
http_requests_total{job="api-server", status="200"}

# Regex match
http_requests_total{job=~"api-.*"}

# Negative match
http_requests_total{job!="frontend"}
```

---

## Range Vectors

```promql
# Last 5 minutes
http_requests_total[5m]

# Last 1 hour
http_requests_total[1h]

# Time units: s, m, h, d, w, y
```

---

## Aggregation Operators

```promql
# Sum across all instances
sum(http_requests_total)

# Group by label
sum by (job) (http_requests_total)

# Average
avg(node_cpu_seconds_total)

# Count
count(up == 1)

# Min/Max
min(node_memory_MemFree_bytes)
max(node_memory_MemFree_bytes)

# Top/Bottom K
topk(5, http_requests_total)
bottomk(3, http_requests_total)
```

---

## Rate Functions

```promql
# Per-second rate over 5m
rate(http_requests_total[5m])

# Increase over time range
increase(http_requests_total[1h])

# Instant rate (last two samples)
irate(http_requests_total[5m])
```

---

## Math Operations

```promql
# Arithmetic
node_memory_MemTotal_bytes - node_memory_MemFree_bytes

# Percentage
(node_memory_MemTotal_bytes - node_memory_MemFree_bytes) / node_memory_MemTotal_bytes * 100

# Comparison (returns 1 or 0)
http_requests_total > 100
```

---

## Common Patterns

```promql
# Request rate per second
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# CPU usage percentage
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage percentage
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# Disk usage
(node_filesystem_size_bytes - node_filesystem_free_bytes) / node_filesystem_size_bytes * 100
```

---

## Alert Examples

```promql
# High error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05

# Instance down
up == 0

# High memory usage
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.9

# Disk filling up (predict 4h)
predict_linear(node_filesystem_free_bytes[1h], 4 * 3600) < 0
```

---

## Functions Reference

| Function | Description |
|----------|-------------|
| `rate()` | Per-second average rate over range |
| `irate()` | Instant rate (last two points) |
| `increase()` | Total increase over range |
| `sum()` | Sum values |
| `avg()` | Average values |
| `count()` | Count series |
| `min()` / `max()` | Min/Max values |
| `histogram_quantile()` | Calculate percentiles |
| `predict_linear()` | Linear prediction |
| `delta()` | Difference between first/last |
| `absent()` | Returns 1 if series is missing |

---

*For complete reference, see [Prometheus Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)*
