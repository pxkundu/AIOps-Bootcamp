# Exercise Solutions: Metrics Pipeline Design

> Solutions and explanations for Day 3 exercises

---

## Exercise 1: Building a Custom Prometheus Exporter

### Solution Overview

The solution demonstrates:
- Proper metric type selection (Counter, Gauge, Histogram)
- Multi-process support for Gunicorn
- Realistic metric simulation
- Integration with Prometheus

### Key Implementation Points

1. **Metric Definitions:**
   - Use appropriate suffixes (`_total` for counters)
   - Include relevant labels (category, status)
   - Set appropriate histogram buckets

2. **Multi-Process Mode:**
   - Use `multiprocess.MultiProcessCollector(registry)`
   - Set `PROMETHEUS_MULTIPROC_DIR` environment variable
   - Use shared registry for all metrics

3. **Testing:**
   - Verify metrics endpoint returns valid Prometheus format
   - Check metric types and labels
   - Validate histogram buckets

---

## Exercise 2: Metric Aggregation & Recording Rules

### Solution Overview

The solution focuses on:
- Reducing cardinality through aggregation
- Pre-computing expensive queries
- Optimizing dashboard performance

### Key Implementation Points

1. **Cardinality Analysis:**
   ```promql
   # Count unique time-series
   count({__name__=~".+"})
   
   # Identify high-cardinality metrics
   topk(10, count by (__name__) ({__name__=~".+"}))
   ```

2. **Recording Rules Design:**
   - Aggregate by service/region (drop instance label)
   - Pre-compute rates and percentiles
   - Use appropriate evaluation intervals

3. **Performance Optimization:**
   - Compare query times before/after recording rules
   - Monitor rule evaluation time
   - Use `promtool` to validate rules

---

## Exercise 3: Real-Time Metrics Pipeline

### Solution Overview

The solution implements:
- Prometheus Remote Write adapter
- Kafka-based streaming pipeline
- Statistical and ML-based anomaly detection
- Alert generation and routing

### Key Implementation Points

1. **Remote Write Adapter:**
   - Parse Prometheus remote write format
   - Convert to Kafka messages
   - Handle backpressure

2. **Anomaly Detection:**
   - Rolling window statistics (mean, std, z-score)
   - Isolation Forest for ML-based detection
   - Multiple detection methods for robustness

3. **Alert Pipeline:**
   - Format alerts in Prometheus Alertmanager format
   - Route to appropriate channels
   - Include context and severity

---

## Common Pitfalls & Solutions

### Pitfall 1: High Cardinality
**Problem:** Too many unique label combinations
**Solution:** Aggregate by dropping high-cardinality labels

### Pitfall 2: Slow Queries
**Problem:** Computing rates/percentiles on-the-fly
**Solution:** Use recording rules to pre-compute

### Pitfall 3: Missing Metrics
**Problem:** Exporter not exposing metrics correctly
**Solution:** Verify `/metrics` endpoint, check Prometheus targets

### Pitfall 4: Anomaly False Positives
**Problem:** Too sensitive detection thresholds
**Solution:** Tune z-score thresholds, use ensemble methods

---

## Best Practices Demonstrated

1. **Metric Naming:** Follow Prometheus conventions
2. **Label Design:** Keep cardinality low
3. **Recording Rules:** Pre-compute expensive queries
4. **Error Handling:** Graceful degradation
5. **Testing:** Validate at each stage

---

<p align="center">
  <a href="../exercises/exercise-01-exporter.md">← Back to Exercises</a>
</p>
