# Exercise 1: Deploy the Observability Stack

## 🎯 Objective
Deploy a complete observability stack and verify all components are working correctly.

---

## 📋 Prerequisites
- Docker Desktop running
- At least 4GB RAM available
- Ports 3000, 9090, 9100, 16686 available

---

## 🚀 Part 1: Stack Deployment

### Step 1: Navigate to Infrastructure Directory
```bash
cd /Users/parthasarathikundu/codebase/AIOps-Bootcamp/infrastructure/docker-compose
```

### Step 2: Start the Stack
```bash
docker-compose up -d
```

### Step 3: Verify All Containers are Running
```bash
docker-compose ps
```

**Expected Output:**
```
NAME                IMAGE                              STATUS
prometheus          prom/prometheus:v2.47.0            Up
grafana             grafana/grafana:10.2.0             Up
jaeger              jaegertracing/all-in-one:1.51      Up
node-exporter       prom/node-exporter:v1.6.1          Up
```

---

## 🔍 Part 2: Verify Services

### Prometheus (Port 9090)
1. Open http://localhost:9090
2. Go to **Status → Targets**
3. Verify all targets are **UP**

**Screenshot Checkpoint:** Take a screenshot showing all targets in UP state.

### Grafana (Port 3000)
1. Open http://localhost:3000
2. Login: `admin` / `admin` (skip password change for now)
3. Go to **Connections → Data Sources**
4. Verify **Prometheus** and **Jaeger** are configured

### Jaeger (Port 16686)
1. Open http://localhost:16686
2. You should see the Jaeger UI (no traces yet)

---

## 📊 Part 3: First PromQL Queries

In the Prometheus UI (http://localhost:9090), run these queries:

### Query 1: Check System Uptime
```promql
up
```
**Expected:** Should show `1` for all targets

### Query 2: CPU Usage
```promql
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```
**Expected:** Current CPU usage percentage

### Query 3: Memory Usage
```promql
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```
**Expected:** Current memory usage percentage

---

## ✅ Deliverables

Create a file `day-03-verification.md` with:
1. Screenshot of Prometheus targets (all UP)
2. Screenshot of Grafana data sources
3. Results of the 3 PromQL queries above
4. Any errors encountered and how you resolved them

---

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
# Find process using port 9090
lsof -i :9090

# Stop the process or change port in docker-compose.yml
```

### Issue: Container fails to start
```bash
# Check logs
docker-compose logs prometheus

# Restart specific service
docker-compose restart prometheus
```

### Issue: Targets showing as DOWN
- Check network connectivity between containers
- Verify service names in prometheus.yml match container names
- Check firewall settings
