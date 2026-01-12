# PromQL Challenge Game 🎮

> **Level up your PromQL skills through progressive challenges!**

---

## 🎯 How It Works

Each challenge presents a monitoring problem. You must write a PromQL query to solve it. Solutions are provided, but try solving them yourself first!

---

## 🌟 Level 1: Newbie (Basic Queries)

### Challenge 1.1: Service Health Check
**Problem:** Find all services that are currently down.

**Hint:** Use the `up` metric.

<details>
<summary>💡 Solution</summary>

```promql
up == 0
```

**Explanation:** The `up` metric is automatically created by Prometheus for all targets. Value 1 = healthy, 0 = down.
</details>

---

### Challenge 1.2: Count Running Instances
**Problem:** How many instances of each job are currently running?

<details>
<summary>💡 Solution</summary>

```promql
count by (job) (up == 1)
```

**Explanation:** `count by (job)` groups results by the job label and counts instances where `up == 1`.
</details>

---

## 🔥 Level 2: Intermediate (Rates & Aggregations)

### Challenge 2.1: Request Rate
**Problem:** Calculate the per-second request rate over the last 5 minutes for your API.

**Hint:** Use `rate()` on a counter metric.

<details>
<summary>💡 Solution</summary>

```promql
rate(http_requests_total[5m])
```

**Explanation:** `rate()` calculates the per-second average rate of increase over the specified time window.
</details>

---

### Challenge 2.2: Total Throughput
**Problem:** What's the TOTAL requests per second across ALL services?

<details>
<summary>💡 Solution</summary>

```promql
sum(rate(http_requests_total[5m]))
```

**Explanation:** `sum()` aggregates across all time series, giving you the total.
</details>

---

### Challenge 2.3: Error Rate Percentage
**Problem:** Calculate the percentage of requests that are errors (5xx status codes).

**Hint:** Divide error requests by total requests.

<details>
<summary>💡 Solution</summary>

```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) 
/ 
sum(rate(http_requests_total[5m])) 
* 100
```

**Explanation:** Regex `5..` matches any 5xx status. We divide error rate by total rate and multiply by 100 for percentage.
</details>

---

## 💪 Level 3: Advanced (Percentiles & Complex Queries)

### Challenge 3.1: P95 Latency
**Problem:** Calculate the 95th percentile request latency.

**Data:** You have `http_request_duration_seconds_bucket` histogram.

<details>
<summary>💡 Solution</summary>

```promql
histogram_quantile(0.95, 
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

**Explanation:** `histogram_quantile()` calculates quantiles from histogram buckets. The `le` label must be preserved with `sum by (le)`.
</details>

---

### Challenge 3.2: Slowest Endpoints
**Problem:** Find the top 5 endpoints with the highest P99 latency.

<details>
<summary>💡 Solution</summary>

```promql
topk(5,
  histogram_quantile(0.99,
    sum by (path, le) (rate(http_request_duration_seconds_bucket[5m]))
  )
)
```

**Explanation:** `topk(5, ...)` returns the 5 highest values. We group by `path` to get per-endpoint metrics.
</details>

---

### Challenge 3.3: Predict Future Value
**Problem:** Predict when disk space will run out (< 5% remaining) based on current trend.

**Hint:** Use `predict_linear()`.

<details>
<summary>💡 Solution</summary>

```promql
predict_linear(
  node_filesystem_avail_bytes{mountpoint="/"}[1h],
  4 * 3600
) < (node_filesystem_size_bytes * 0.05)
```

**Explanation:** `predict_linear()` forecasts the value 4 hours (4 * 3600 seconds) into the future based on the last hour of data.
</details>

---

## 🏆 Level 4: Expert (Production Scenarios)

### Challenge 4.1: Dynamic Threshold Alert
**Problem:** Create an alert that fires when request rate is 50% below the average of the last week.

<details>
<summary>💡 Solution</summary>

```promql
rate(http_requests_total[5m])
<
avg_over_time(rate(http_requests_total[5m])[7d:5m]) * 0.5
```

**Explanation:** `avg_over_time()` with `[7d:5m]` calculates average over the last 7 days, sampled every 5 minutes. We compare current rate to 50% of that baseline.
</details>

---

### Challenge 4.2: Memory Leak Detection
**Problem:** Detect if memory usage is consistently increasing (potential memory leak).

**Hint:** Use `deriv()` to calculate the rate of change.

<details>
<summary>💡 Solution</summary>

```promql
deriv(node_memory_MemAvailable_bytes[30m]) < -1000000
```

**Explanation:** `deriv()` calculates the per-second derivative (rate of change). Negative values indicate memory is decreasing (leak). The threshold -1000000 means memory is dropping by 1MB/sec.
</details>

---

### Challenge 4.3: Correlated Service Failures
**Problem:** Find services that tend to go down together (correlation).

**Advanced Concept:** This requires recording rules and alerting logic, but here's a detection query:

<details>
<summary>💡 Solution</summary>

```promql
# Count how many services are down in the same minute
count by (time) (
  up == 0
) > 2
```

**Explanation:** If more than 2 services go down simultaneously, it suggests a correlated failure (network issue, shared dependency, etc.).
</details>

---

## 🎖️ Bonus Challenges

### Ninja Challenge: Custom Apdex Score
**Problem:** Calculate an Apdex (Application Performance Index) score.

**Definition:**
- Satisfied: requests < 100ms
- Tolerating: requests 100-500ms
- Frustrated: requests > 500ms

**Formula:** `(Satisfied + (Tolerating / 2)) / Total`

<details>
<summary>💡 Solution</summary>

```promql
(
  sum(rate(http_request_duration_seconds_bucket{le="0.1"}[5m]))
  +
  (sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m])) - sum(rate(http_request_duration_seconds_bucket{le="0.1"}[5m]))) / 2
)
/
sum(rate(http_request_duration_seconds_count[5m]))
```

**Explanation:** This uses histogram buckets to count requests in each category, then applies the Apdex formula.
</details>

---

## 📊 Scoring System

- **Level 1:** 10 points per challenge (30 total)
- **Level 2:** 20 points per challenge (60 total)
- **Level 3:** 30 points per challenge (90 total)
- **Level 4:** 40 points per challenge (120 total)
- **Bonus:** 50 points

**Total Possible:** 350 points

### Achievement Badges

| Score | Badge | Title |
|-------|-------|-------|
| 100+ | 🥉 | PromQL Apprentice |
| 200+ | 🥈 | Query Craftsman |
| 300+ | 🥇 | Metrics Master |
| 350 | 💎 | PromQL Ninja |

---

## 🎓 Learning Tips

1. **Test in Prometheus UI first** - Use the Graph tab to validate queries
2. **Use query inspector** - Check query performance and sample count
3. **Start simple, then optimize** - Get it working, then make it efficient
4. **Read error messages carefully** - Prometheus errors are usually helpful
5. **Check cardinality** - Avoid queries that return millions of series

---

## 🚀 Next Steps

Once you've mastered these challenges:
1. Create your own challenges for your team
2. Time yourself - can you solve all in under 30 minutes?
3. Optimize query performance (fewer samples = faster)
4. Convert these into recording rules or alerts

---

**Share your score in GitHub Discussions!** 🎉
