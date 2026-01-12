# Chaos Engineering Lab: Break It to Learn It

> **"You can't learn to fix what you've never seen broken."**

---

## 🎯 Objective

Intentionally inject failures into your observability stack to:
1. Learn how failures manifest in metrics/logs/traces
2. Test your alerting rules
3. Practice incident response in a safe environment
4. Build muscle memory for debugging

---

## 🧪 Safety Rules

**🚨 ONLY run these experiments on your LOCAL bootcamp environment, NEVER in production!**

✅ Safe: Your Docker Compose stack  
❌ Unsafe: Any shared/production system

---

## 🔥 Experiment 1: Resource Exhaustion

### Scenario: CPU Spike

**Hypothesis:** Your high CPU alert should fire when CPU > 80%.

**Inject Failure:**
```bash
# Install stress tool (if not already installed)
brew install stress  # macOS
# or
sudo apt-get install stress  # Linux

# Stress 4 CPU cores for 3 minutes
stress --cpu 4 --timeout 180
```

**Observe:**
1. **Prometheus Query:**
   ```promql
   100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
   ```
   
2. **Expected:** Should exceed 80% threshold

3. **Grafana Dashboard:** Watch your CPU panel spike

4. **Check Alerts:** Go to Prometheus → Alerts  
   Should see `HighCPUUsage` transition: Inactive → Pending → Firing

**⏱️ Timing:**
- Alert should go to Pending immediately
- Should FIRE after 2 minutes (based on `for: 2m`)

**📸 Deliverable:** Screenshot showing alert in Firing state

---

## 💥 Experiment 2: Service Down

### Scenario: Container Crash

**Hypothesis:** Your service health alert should fire within 1 minute of a service going down.

**Inject Failure:**
```bash
# Stop the node-exporter
docker-compose stop node-exporter
```

**Observe:**
1. **Prometheus Targets:** Status → Targets  
   `node-exporter` should show as DOWN

2. **Query:**
   ```promql
   up{job="node-exporter"}
   ```
   Should return `0`

3. **Alert:** `InstanceDown` should fire

**Recover:**
```bash
docker-compose start node-exporter
```

**Watch:** Alert should auto-resolve

**📊 Measure:**
- Time to detection: ___ seconds
- Time to alert: ___ seconds
- Time to auto-resolve after restart: ___ seconds

---

## 🌊 Experiment 3: Network Partition

### Scenario: Simulate network issues

**Hypothesis:** Services can't scrape each other when network is broken.

**Inject Failure:**
```bash
# Create network isolation
docker network disconnect aiops-network prometheus

# Wait 30 seconds...

# Reconnect
docker network connect aiops-network prometheus
```

**Observe:**
- All targets should go DOWN simultaneously
- Prometheus itself should remain UP (self-monitoring)
- Multiple alerts should fire

**Questions:**
1. How many alerts fired?
2. Did they fire simultaneously or cascaded?
3. How long until they auto-resolved?

---

## 🐌 Experiment 4: Slow Response Times

### Scenario: Latency injection

**Setup:** Create a simple Flask app with controllable latency:

**File: `slow-service/app.py`**
```python
from flask import Flask, request
import time
import random

app = Flask(__name__)

@app.route('/slow')
def slow():
    # Random latency between 100ms and 5s
    delay = random.uniform(0.1, 5.0)
    time.sleep(delay)
    return {"delay": delay}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
```

**Inject Failure:**
```bash
# Run the slow service
python slow-service/app.py &

# Generate traffic
for i in {1..100}; do curl http://localhost:9999/slow & done
```

**Observe:**
- If you have latency histogram metrics, you should see P95/P99 spike
- Response time distribution changes dramatically

**Practice:**
Create a dashboard panel showing:
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

---

## 💣 Experiment 5: Cascading Failure

### Scenario: Dependency chain failure

**Architecture:**
```
Service A → Service B → Service C
```

**Inject Failure:**
```bash
# Kill Service C
docker-compose stop service-c

# Watch Service B start failing (can't reach C)
# Watch Service A start failing (B timeouts)
```

**Observe in Traces:**
1. Open Jaeger
2. Search for traces during the failure window
3. You should see:
   - Incomplete traces (missing Service C spans)
   - Long-running spans (timeouts)
   - Error tags on spans

**Advanced:** Can you identify the root cause from traces alone?

---

## 🎲 Experiment 6: Random Errors

### Scenario: Intermittent failures

**Setup:** Modify a service to randomly fail:

```python
import random

@app.route('/unreliable')
def unreliable():
    if random.random() < 0.1:  # 10% failure rate
        abort(500)
    return {"status": "ok"}
```

**Observe:**
```promql
# Error rate should hover around 10%
rate(http_requests_total{status="500"}[5m]) 
/ 
rate(http_requests_total[5m])
```

**Challenge:** At what error rate % would you set an alert?

---

## 📊 Experiment 7: Metric Explosion (High Cardinality)

### Scenario: Cardinality bomb

**WARNING:** This can crash Prometheus! Use a test instance.

**Inject Failure:**
```python
from prometheus_client import Counter

# BAD: User ID as label (high cardinality)
requests = Counter('bad_requests', 'Requests', ['user_id'])

for i in range(10000):
    requests.labels(user_id=str(i)).inc()
```

**Observe:**
```promql
# Check number of time series
prometheus_tsdb_symbol_table_size_bytes
```

**Expected:** Prometheus memory usage spikes, queries slow down

**Lesson:** Why high cardinality labels are dangerous!

---

## 🧩 Experiment 8: Dashboard Chaos

### Scenario: Broken queries

**Inject Failure:**
Intentionally create broken

 PromQL queries in Grafana:

```promql
# Missing metric
this_metric_does_not_exist

# Invalid aggregation
sum(up) by (nonexistent_label)

# Syntax error
rate(up{job="test"[5m])  # Missing }
```

**Practice:**
1. Can you identify the error from Grafana's error message?
2. How fast can you fix it?

---

## 🏆 Chaos Engineering Scorecard

Track your experiments:

| Experiment | Time to Detect | Time to Diagnose | Alert Fired? | Learned |
|------------|---------------|------------------|--------------|---------|
| CPU Spike | ___ sec | ___ sec | ✅/❌ | |
| Service Down | ___ sec | ___ sec | ✅/❌ | |
| Network Partition | ___ sec | ___ sec | ✅/❌ | |
| Slow Response | ___ sec | ___ sec | ✅/❌ | |
| Cascading Failure | ___ sec | ___ sec | ✅/❌ | |
| Random Errors | ___ sec | ___ sec | ✅/❌ | |
| Metric Explosion | ___ sec | ___ sec | ✅/❌ | |
| Dashboard Chaos | ___ sec | ___ sec | N/A | |

---

## 🎓 Post-Chaos Analysis

### Questions to Answer:

1. **Which failures were hardest to detect?** Why?
2. **Which alerts fired too early/late?** How to tune them?
3. **Did any failures NOT trigger alerts?** What's missing?
4. **What would you do differently in production?**

### Action Items:

Based on your experiments, create:
- [ ] New alert rules for un-caught failures
- [ ] Dashboard improvements
- [ ] Runbook for each failure type
- [ ] List of "known unknowns" (things you still can't detect)

---

## 💡 Advanced Challenges

1. **Automate Chaos:** Create a script that randomly injects one failure every 10 minutes
2. **Game Mode:** Have a friend inject a failure, you have 5 minutes to diagnose
3. **Chaos Calendar:** Schedule daily mini-chaos experiments
4. **Chaos Documentation:** Create a "Chaos Lab Notebook" with findings

---

## 🔐 Production Readiness Checklist

Before running chaos in production (GameDay):

- [ ] Get explicit approval from management
- [ ] Run during low-traffic hours
- [ ] Have rollback plan ready
- [ ] Team on standby
- [ ] Blast radius limited (one service at a time)
- [ ] Monitoring is healthy
- [ ] Customer communication plan ready

---

**"The best way to ensure reliability is to practice failure."** - Principles of Chaos Engineering

**Share your chaos results in GitHub Discussions!** 🔥
