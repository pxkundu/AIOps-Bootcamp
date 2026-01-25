# Exercise 03: High-Performance Metrics with VictoriaMetrics

## 🎯 Objective
Explore VictoriaMetrics as a drop-in replacement for Prometheus storage and learn how to use the "Remote Write" protocol to centralize metrics.

---

## 🛠️ Step 1: Deploying VictoriaMetrics

Update your `docker-compose.yml` to add VictoriaMetrics (Single-node):

```yaml
  victoriametrics:
    image: victoriametrics/victoria-metrics:latest
    ports:
      - "8428:8428"
    command:
      - "--storageDataPath=/storage"
      - "--httpListenAddr=:8428"
```

Restart the stack:
```bash
docker-compose up -d victoriametrics
```

---

## 📝 Step 2: Configuring Prometheus Remote Write

In your existing Prometheus configuration (`prometheus.yml`), add the following section to stream metrics to VictoriaMetrics:

```yaml
remote_write:
  - url: "http://victoriametrics:8428/api/v1/write"
```

*Note: Restart Prometheus after updating the configuration.*

---

## 🔍 Step 3: Querying Metrics (MetricsQL)

VictoriaMetrics supports **MetricsQL**, which is backward compatible with PromQL but adds powerful features.

1. Open http://localhost:8428/vmui/
2. Run these queries to see the difference:

### Task 1: Rate Calculation (The VictoriaMetrics Way)
Standard PromQL: `rate(node_cpu_seconds_total[5m])`
MetricsQL simplified: `rate(node_cpu_seconds_total)` (It automatically detects intervals!)

### Task 2: Topk with Aggregation
Find the top 3 measurements by count, but combined across all instances.
```js
topk(3, count({__name__=~".+"}) by (__name__))
```

---

## 🧪 Challenge: Benchmarking Storage
Run a load generator (like the one from Day 4) for 10 minutes. 
1. Check the disk usage of VictoriaMetrics: `du -sh /var/lib/docker/volumes/...`
2. Compare it to Prometheus's `/data` folder.
*Hint: VictoriaMetrics often has 10x better compression than standard Prometheus.*

---

## ✅ Delivery
Submit a screenshot of the VictoriaMetrics **VMUI** showing a graph of `prometheus_remote_storage_succeeded_samples_total`.
