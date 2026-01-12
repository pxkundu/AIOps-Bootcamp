# Exercise 3: Creating Alert Rules

## 🎯 Objective
Configure Prometheus alerting rules and test them.

---

## 🚨 Part 1: Create Alert Rules File

### Step 1: Create Rules File
Create `infrastructure/docker-compose/prometheus/rules/alerts.yml`:

```yaml
groups:
  - name: system_alerts
    rules:
      # CPU Alert
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 2m
        labels:
          severity: warning
          component: system
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value | humanize }}%"

      # Memory Alert
      - alert: HighMemoryUsage
        expr: |
          (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 > 85
        for: 2m
        labels:
          severity: warning
          component: system
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanize }}%"

      # Instance Down
      - alert: InstanceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
          component: infrastructure
        annotations:
          summary: "Instance {{ $labels.instance }} is down"
          description: "{{ $labels.job }} has been down for more than 1 minute"
```

### Step 2: Update Prometheus Config
Edit `prometheus.yml` to include the rules file:

```yaml
rule_files:
  - /etc/prometheus/rules/*.yml
```

### Step 3: Update Docker Compose
Add volume mount for rules:

```yaml
volumes:
  - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
  - ./prometheus/rules:/etc/prometheus/rules
  - prometheus_data:/prometheus
```

### Step 4: Reload Prometheus
```bash
docker-compose restart prometheus
```

---

## 🧪 Part 2: Test Alerts

### Verify Rules Loaded
1. Go to http://localhost:9090/rules
2. Verify your alert rules appear

### Trigger a Test Alert

**Method 1: Stress Test (CPU)**
```bash
# Install stress tool
brew install stress  # macOS
# or
sudo apt-get install stress  # Linux

# Run CPU stress
stress --cpu 8 --timeout 180s
```

**Method 2: Stop a Service**
```bash
docker-compose stop node-exporter
```

Watch the alert in Prometheus:
- **Inactive** → **Pending** (waiting for `for` duration)
- **Pending** → **Firing** (alert is active)

---

## 📧 Part 3: Alert Routing (Optional)

### Configure Alertmanager
Create `alertmanager/alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'webhook'

receivers:
  - name: 'webhook'
    webhook_configs:
      - url: 'http://localhost:5001/alerts'
        send_resolved: true
```

### Add to Docker Compose
```yaml
alertmanager:
  image: prom/alertmanager:v0.26.0
  ports:
    - "9093:9093"
  volumes:
    - ./alertmanager:/etc/alertmanager
  command:
    - '--config.file=/etc/alertmanager/alertmanager.yml'
```

---

## ✅ Deliverables

1. Your complete `alerts.yml` file
2. Screenshot of alerts in **Firing** state
3. Documentation of how you triggered the alert
4. Screenshot of alert resolution

---

## 💡 Advanced Challenges

1. Create an alert for disk space < 20%
2. Set up multi-level severity (info, warning, critical)
3. Create a "runbook" annotation with troubleshooting steps
4. Implement alert inhibition rules
