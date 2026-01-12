# Day 3 Resources: Observability Stack Deep Dive

> **Advanced materials for mastering Prometheus, Grafana, and Jaeger.**

---

## 🌐 Official Documentation

### Prometheus
*   **[Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)** - Official comprehensive guide
*   **[PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)** - Query language fundamentals
*   **[Best Practices](https://prometheus.io/docs/practices/naming/)** - Metric naming and instrumentation patterns
*   **[Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)** - Complete alerting guide

### Grafana
*   **[Grafana Documentation](https://grafana.com/docs/grafana/latest/)** - Official docs
*   **[Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)** - Design guidelines
*   **[Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)** - Automate dashboard deployment
*   **[Variables](https://grafana.com/docs/grafana/latest/dashboards/variables/)** - Dynamic dashboard creation

### Jaeger
*   **[Jaeger Documentation](https://www.jaegertracing.io/docs/)** - Official tracing guide
*   **[Architecture](https://www.jaegertracing.io/docs/latest/architecture/)** - Understanding Jaeger components
*   **[Sampling Strategies](https://www.jaegertracing.io/docs/latest/sampling/)** - Control trace volume

---

## 📖 Learning Resources

### Interactive Tutorials
*   **[PromLabs](https://promlabs.com/)** - Interactive PromQL training
*   **[Katacoda Prometheus](https://www.katacoda.com/courses/prometheus)** - Hands-on scenarios
*   **[Grafana Play](https://play.grafana.org/)** - Explore live dashboards

### Video Courses
*   **[Prometheus Monitoring on Udemy](https://www.udemy.com/course/prometheus-course/)** - Comprehensive video course
*   **[PromCon Talks](https://www.youtube.com/c/PrometheusIo)** - Conference presentations
*   **[Grafana Tutorials](https://www.youtube.com/c/Grafana)** - Official video tutorials

### Books
*   **"Prometheus: Up & Running"** by Brian Brazil - The definitive guide
*   **"Distributed Tracing in Practice"** - O'Reilly book on tracing patterns

---

## 🛠️ Tools & Utilities

### PromQL Tools
*   **[PromLens](https://promlens.com/)** - PromQL query builder and visualizer
*   **[Promtool](https://prometheus.io/docs/prometheus/latest/command-line/promtool/)** - Validate configs and rules

### Dashboard Libraries
*   **[Grafana Dashboard Repository](https://grafana.com/grafana/dashboards/)** - Pre-built dashboards
*   **[Node Exporter Full](https://grafana.com/grafana/dashboards/1860)** - Popular system dashboard
*   **[Kubernetes Cluster Monitoring](https://grafana.com/grafana/dashboards/7249)** - K8s dashboard

### Testing Tools
*   **[Avalanche](https://github.com/prometheus-community/avalanche)** - Prometheus load testing
*   **[Promgen](https://github.com/line/promgen)** - Prometheus configuration management

---

## 🐛 Troubleshooting Guide

### Common Issues

#### Prometheus Not Scraping Targets

**Symptoms:** Targets show as DOWN in Prometheus UI

**Solutions:**
```bash
# Check network connectivity
docker exec prometheus ping node-exporter

# Verify DNS resolution
docker exec prometheus nslookup node-exporter

# Check Prometheus logs
docker logs prometheus

# Validate prometheus.yml
promtool check config prometheus.yml
```

#### High Cardinality Issues

**Symptoms:** Prometheus using too much memory/disk

**Solutions:**
- Review metric labels for high-cardinality values (user IDs, request IDs)
- Use recording rules to pre-aggregate expensive queries
- Adjust retention period: `--storage.tsdb.retention.time=15d`
- Enable remote write for long-term storage

#### Grafana Dashboard Not Loading

**Symptoms:** Dashboard shows "No data" or errors

**Solutions:**
```promql
# Test query in Prometheus first
up

# Check time range matches data availability
# Verify data source configuration
# Check browser console for errors
```

#### Jaeger Traces Not Appearing

**Symptoms:** No traces in Jaeger UI

**Solutions:**
```bash
# Verify collector is receiving spans
docker logs jaeger | grep "span"

# Check application is sending to correct endpoint
# Verify OTLP port is accessible (4317 for gRPC)
# Check sampling rate (might be set to 0)
```

---

## 📊 Performance Tuning

### Prometheus Optimization
```yaml
# prometheus.yml
global:
  scrape_interval: 30s      # Increase for less critical metrics
  evaluation_interval: 30s   # Match scrape interval

# Use relabeling to drop unnecessary metrics
scrape_configs:
  - job_name: 'node'
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'node_.*_seconds_total'
        action: drop
```

### Grafana Performance
- Limit time range for queries
- Use `$__interval` variable for dynamic step size
- Enable query caching
- Use recording rules for expensive queries

---

## 🎓 Next Steps: Preparation for Day 4

Tomorrow we'll dive into OpenTelemetry instrumentation. To prepare:
1. Read [OpenTelemetry Concepts](https://opentelemetry.io/docs/concepts/)
2. Review [Python Auto-Instrumentation](https://opentelemetry.io/docs/instrumentation/python/automatic/)
3. Understand [Context Propagation](https://opentelemetry.io/docs/concepts/context-propagation/)

---

## 💡 Pro Tips

1. **Use Labels Wisely:** Keep cardinality low, use labels for dimensions you'll aggregate on
2. **Recording Rules:** Pre-compute expensive queries that run frequently
3. **Alert Fatigue:** Start with fewer, high-quality alerts
4. **Dashboard Organization:** Group related panels, use rows and variables
5. **Backup Dashboards:** Export as JSON and version control them

---

<p align="center">
  <a href="../lecture-notes.md">Back to Lecture Notes</a>
</p>
