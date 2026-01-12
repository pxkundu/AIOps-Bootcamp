# Exercise 2: Building Your First Dashboard

## 🎯 Objective
Create a comprehensive system monitoring dashboard in Grafana.

---

## 📊 Part 1: Create Dashboard

### Step 1: New Dashboard
1. In Grafana, click **+ → Dashboard**
2. Click **Add visualization**
3. Select **Prometheus** as data source

### Step 2: CPU Usage Panel
**Query:**
```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

**Panel Settings:**
- Title: "CPU Usage %"
- Unit: Percent (0-100)
- Thresholds: 
  - Green: 0-70
  - Yellow: 70-85
  - Red: 85-100

### Step 3: Memory Usage Panel
**Query:**
```promql
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```

**Panel Settings:**
- Title: "Memory Usage %"
- Unit: Percent (0-100)
- Visualization: Gauge

### Step 4: Disk Space Panel
**Query:**
```promql
(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100
```

**Panel Settings:**
- Title: "Disk Space Available %"
- Unit: Percent (0-100)
- Invert threshold colors (low is bad)

### Step 5: Network Traffic Panel
**Query (Receive):**
```promql
rate(node_network_receive_bytes_total[5m])
```

**Query (Transmit):**
```promql
rate(node_network_transmit_bytes_total[5m])
```

**Panel Settings:**
- Title: "Network I/O"
- Unit: Bytes/sec
- Visualization: Time series

---

## 🎨 Part 2: Dashboard Organization

### Add Rows
1. Click **Add → Row**
2. Name it "System Resources"
3. Drag CPU and Memory panels into this row

### Add Variables
1. Dashboard settings → Variables → Add variable
2. Name: `instance`
3. Query: `label_values(up, instance)`
4. Update panels to use `{instance="$instance"}`

---

## 📈 Part 3: Advanced Panels

### Request Rate Panel (if demo app is running)
```promql
sum(rate(http_requests_total[5m])) by (method)
```

### Error Rate Panel
```promql
sum(rate(http_requests_total{status=~"5.."}[5m])) 
/ 
sum(rate(http_requests_total[5m]))
```

---

## ✅ Deliverables

1. Export your dashboard as JSON
2. Save to `day-03-dashboard.json`
3. Screenshot of the complete dashboard
4. Document any custom queries you created

---

## 💡 Bonus Challenges

1. Add a panel showing top 5 processes by CPU
2. Create a heatmap for request duration distribution
3. Add annotations for deployment events
4. Set up email alerts for high CPU usage
