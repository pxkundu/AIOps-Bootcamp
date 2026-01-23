# Solutions: Week 2 Day 4 - Metrics Engineering

## [Exercise 1: GitHub Exporter](exercise-01-exporter/)
- `github_exporter.py`: Completed script with labels and error handling.
- `prometheus.yml`: Relabeling snippet.

## [Project: Business Logic Exporter](project-solution/)
- `biz_exporter.py`: Solution with SQLite integration and threshold logic.
- `SentinelDashboard.json`: Grafana dashboard template.

---

### Key Solution Snippets

**1. Database Query in Python Exporter:**
```python
def get_revenue():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM orders WHERE status='completed'")
    result = cursor.fetchone()[0]
    return result if result else 0.0
```

**2. Threshold Selection:**
```python
# Adding severity label based on logic
failed_count = get_failed_count()
sev = "critical" if failed_count > 10 else "normal"
FAILED_METRIC.labels(severity=sev).set(failed_count)
```

**3. Relabeling (Standardizing names):**
```yaml
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'github_(.*)'
        target_label: source
        replacement: 'git_api'
```
