# Exercise 2: Metric Aggregation & Recording Rules

> **Duration:** 2 hours | **Difficulty:** Intermediate
> **Objective:** Design and implement recording rules to optimize query performance and reduce cardinality.

---

## 🎯 Learning Goals

By completing this exercise, you will:
1. Understand when and why to use recording rules.
2. Design aggregation strategies to reduce cardinality.
3. Optimize Prometheus queries for dashboard performance.
4. Implement federation for multi-region setups.

---

## 📋 Scenario

You're managing metrics for a **multi-region microservices architecture**:
- **3 regions:** `us-east`, `eu-west`, `ap-south`
- **5 services:** `api-gateway`, `user-service`, `order-service`, `payment-service`, `notification-service`
- **High cardinality problem:** Each service instance has unique labels, creating thousands of time-series

**Challenge:** Your Grafana dashboards are slow because queries compute `rate()` and `histogram_quantile()` on-the-fly.

---

## 🛠️ Requirements

### Part 1: Analyze Cardinality (30 minutes)

1. **Set up a test Prometheus instance** with sample metrics:
   ```yaml
   # prometheus.yml
   global:
     scrape_interval: 15s
   
   scrape_configs:
     - job_name: 'microservices'
       static_configs:
         - targets: 
           - 'localhost:8001'  # api-gateway
           - 'localhost:8002'  # user-service
           - 'localhost:8003'  # order-service
   ```

2. **Create a script** `cardinality_analyzer.py` that:
   - Queries Prometheus API: `http://localhost:9090/api/v1/label/__name__/values`
   - Counts unique time-series for each metric
   - Identifies high-cardinality metrics
   - Outputs a report:
     ```
     Metric: http_requests_total
     Cardinality: 15,000
     Labels: [region, service, instance, endpoint, status]
     Recommendation: Aggregate by region and service
     ```

3. **Query cardinality using PromQL:**
   ```promql
   # Count unique time-series
   count({__name__=~".+"})
   
   # Count by metric name
   count by (__name__) ({__name__=~".+"})
   ```

### Part 2: Design Recording Rules (45 minutes)

Create `recording_rules.yml` with the following aggregation strategies:

#### Strategy 1: Pre-compute Rates
```yaml
groups:
  - name: service_rates
    interval: 30s
    rules:
      # Aggregate request rate by service and region
      - record: service:requests:rate5m
        expr: |
          sum(rate(http_requests_total[5m])) 
          by (service, region, status)
      
      # Error rate per service
      - record: service:errors:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) 
          by (service, region)
```

#### Strategy 2: Reduce Cardinality
```yaml
  - name: service_aggregates
    interval: 1m
    rules:
      # Drop instance label, aggregate by service only
      - record: service:requests:total
        expr: |
          sum(http_requests_total) 
          by (service, region, status)
      
      # Compute error percentage
      - record: service:error:percentage
        expr: |
          (service:errors:rate5m / service:requests:rate5m) * 100
```

#### Strategy 3: Pre-compute Percentiles
```yaml
  - name: service_latency
    interval: 1m
    rules:
      # P50, P95, P99 latencies
      - record: service:latency:p50
        expr: |
          histogram_quantile(0.50,
            sum(rate(http_request_duration_seconds_bucket[5m])) 
            by (service, region, le))
      
      - record: service:latency:p95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) 
            by (service, region, le))
      
      - record: service:latency:p99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) 
            by (service, region, le))
```

### Part 3: Configure Prometheus (15 minutes)

1. **Update `prometheus.yml`:**
   ```yaml
   global:
     scrape_interval: 15s
     evaluation_interval: 15s
   
   # Load recording rules
   rule_files:
     - "recording_rules.yml"
   
   scrape_configs:
     - job_name: 'microservices'
       static_configs:
         - targets: ['localhost:8001', 'localhost:8002', 'localhost:8003']
   ```

2. **Verify rules are loaded:**
   ```bash
   curl http://localhost:9090/api/v1/rules
   ```

3. **Check rule evaluation:**
   - Go to Prometheus UI → Status → Rules
   - Verify all rules show "SUCCESS"

### Part 4: Query Optimization (30 minutes)

1. **Before (Slow Query):**
   ```promql
   # Computes rate on-the-fly for thousands of series
   histogram_quantile(0.95,
     rate(http_request_duration_seconds_bucket[5m]))
   ```

2. **After (Fast Query):**
   ```promql
   # Uses pre-computed recording rule
   service:latency:p95
   ```

3. **Create a comparison script** `query_benchmark.py`:
   ```python
   import requests
   import time
   
   prometheus_url = "http://localhost:9090/api/v1/query"
   
   # Slow query
   slow_query = """
   histogram_quantile(0.95,
     rate(http_request_duration_seconds_bucket[5m]))
   """
   
   # Fast query (using recording rule)
   fast_query = "service:latency:p95"
   
   def benchmark_query(query, name):
       start = time.time()
       response = requests.get(prometheus_url, 
                              params={'query': query})
       duration = time.time() - start
       print(f"{name}: {duration:.3f}s")
       return duration
   
   slow_time = benchmark_query(slow_query, "Slow Query")
   fast_time = benchmark_query(fast_query, "Fast Query")
   print(f"Speedup: {slow_time / fast_time:.2f}x")
   ```

---

## ✅ Success Criteria

- [ ] Recording rules are defined and loaded in Prometheus
- [ ] Rules successfully reduce cardinality (verify with queries)
- [ ] Pre-computed metrics appear in Prometheus
- [ ] Dashboard queries using recording rules are faster
- [ ] Cardinality analyzer identifies high-cardinality metrics

---

## 🎓 Bonus Challenges

1. **Implement Federation:**
   - Set up a federated Prometheus that aggregates metrics from multiple regions
   - Use `federation` endpoint to pull aggregated metrics

2. **Dynamic Recording Rules:**
   - Use `prometheus-operator` to manage rules via Kubernetes CRDs
   - Automatically generate rules based on service discovery

3. **Cardinality Budget:**
   - Create an alert that fires when cardinality exceeds a threshold
   - Use `prometheus_tsdb_head_series` metric

---

## 📚 Resources

- [Recording Rules Best Practices](https://prometheus.io/docs/practices/rules/)
- [Prometheus Federation](https://prometheus.io/docs/prometheus/latest/federation/)
- [Cardinality Management](https://prometheus.io/docs/practices/naming/)

---

## 💡 Hints

- Recording rules should be evaluated less frequently than scrape interval
- Use `sum()` to aggregate and drop high-cardinality labels
- Test rules with `promtool check rules recording_rules.yml`
- Monitor rule evaluation time in Prometheus UI

---

<p align="center">
  <a href="exercise-01-exporter.md">← Previous Exercise</a> | 
  <a href="exercise-03-pipeline.md">Next Exercise →</a>
</p>
