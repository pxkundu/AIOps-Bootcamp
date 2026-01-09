# Exercise 2: Explore Observability Data

> **Duration:** 2 hours | **Difficulty:** Beginner

---

## 🎯 Objective

Understand the three pillars of observability by exploring real examples of metrics, logs, and traces.

---

## 📝 Tasks

### Task 1: Exploring Metrics

Create a file `explore_metrics.py`:

```python
#!/usr/bin/env python3
"""Explore time-series metrics data."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample CPU metrics (simulating Prometheus data)
def generate_cpu_metrics(hours=24, interval_seconds=15):
    """Generate realistic CPU usage metrics."""
    timestamps = []
    values = []
    
    start = datetime.now() - timedelta(hours=hours)
    current = start
    
    # Base pattern: lower at night, higher during business hours
    while current < datetime.now():
        hour = current.hour
        
        # Base load varies by time of day
        if 9 <= hour <= 17:  # Business hours
            base = 0.60
        elif 23 <= hour or hour <= 6:  # Night
            base = 0.20
        else:  # Transition periods
            base = 0.40
        
        # Add noise and occasional spikes
        noise = np.random.normal(0, 0.05)
        spike = 0.3 if np.random.random() < 0.02 else 0  # 2% chance of spike
        
        value = min(max(base + noise + spike, 0), 1)  # Clamp 0-1
        
        timestamps.append(current)
        values.append(value)
        
        current += timedelta(seconds=interval_seconds)
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'cpu_usage': values,
        'host': 'web-server-01'
    })

# Generate and explore
print("📊 Generating CPU metrics...\n")
df = generate_cpu_metrics()

print(f"Total data points: {len(df)}")
print(f"Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"\nStatistics:")
print(df['cpu_usage'].describe())

print("\n📈 Sample data (first 10 rows):")
print(df.head(10).to_string(index=False))

# Find anomalies (simple threshold)
threshold = 0.9
anomalies = df[df['cpu_usage'] > threshold]
print(f"\n🚨 High CPU events (>{threshold*100}%): {len(anomalies)}")
if len(anomalies) > 0:
    print(anomalies.head().to_string(index=False))

# Save for later use
df.to_csv('sample_metrics.csv', index=False)
print("\n✅ Saved to sample_metrics.csv")
```

Run and observe the output:
```bash
python explore_metrics.py
```

**Questions to answer:**
1. What patterns do you see in the data?
2. How would you define a "normal" range for this metric?
3. What would make a good alerting threshold?

---

### Task 2: Exploring Logs

Create a file `explore_logs.py`:

```python
#!/usr/bin/env python3
"""Explore structured log data."""

import json
from datetime import datetime, timedelta
import random

# Sample log entries (structured JSON logs)
log_templates = [
    {"level": "INFO", "message": "Request processed successfully", "status": 200},
    {"level": "INFO", "message": "User logged in", "status": 200},
    {"level": "WARN", "message": "Slow query detected", "duration_ms": None},
    {"level": "ERROR", "message": "Connection timeout", "target": "database-01"},
    {"level": "ERROR", "message": "Authentication failed", "user_id": None},
    {"level": "DEBUG", "message": "Cache hit", "key": None},
]

def generate_logs(count=100):
    """Generate realistic log entries."""
    logs = []
    start = datetime.now() - timedelta(hours=1)
    
    for i in range(count):
        template = random.choices(
            log_templates,
            weights=[50, 20, 15, 8, 5, 2]  # Weighted by frequency
        )[0].copy()
        
        # Add common fields
        template["timestamp"] = (start + timedelta(seconds=i*36)).isoformat()
        template["request_id"] = f"req-{random.randint(10000, 99999)}"
        template["service"] = random.choice(["api", "auth", "orders", "payments"])
        
        # Fill in dynamic fields
        if "duration_ms" in template and template["duration_ms"] is None:
            template["duration_ms"] = random.randint(1000, 5000)
        if "user_id" in template and template["user_id"] is None:
            template["user_id"] = f"user-{random.randint(1, 100)}"
        if "key" in template and template["key"] is None:
            template["key"] = f"cache:{random.choice(['user', 'product', 'order'])}:{random.randint(1, 1000)}"
        
        logs.append(template)
    
    return logs

# Generate and analyze
print("📋 Generating log entries...\n")
logs = generate_logs(100)

# Count by level
level_counts = {}
for log in logs:
    level = log["level"]
    level_counts[level] = level_counts.get(level, 0) + 1

print("Log level distribution:")
for level, count in sorted(level_counts.items()):
    print(f"  {level}: {count}")

# Find errors
errors = [log for log in logs if log["level"] == "ERROR"]
print(f"\n🚨 Error logs ({len(errors)}):")
for error in errors[:5]:
    print(f"  [{error['timestamp']}] {error['message']} - {error['service']}")

# Extract insights
print("\n📊 Insights:")
services = {}
for log in logs:
    svc = log["service"]
    services[svc] = services.get(svc, {"total": 0, "errors": 0})
    services[svc]["total"] += 1
    if log["level"] == "ERROR":
        services[svc]["errors"] += 1

print("\nError rate by service:")
for svc, stats in services.items():
    error_rate = (stats["errors"] / stats["total"]) * 100
    print(f"  {svc}: {error_rate:.1f}% ({stats['errors']}/{stats['total']})")

# Save sample logs
with open('sample_logs.json', 'w') as f:
    json.dump(logs[:20], f, indent=2)
print("\n✅ Sample saved to sample_logs.json")
```

Run and observe:
```bash
python explore_logs.py
```

**Questions to answer:**
1. Which service has the highest error rate?
2. How would you search for related log entries?
3. What patterns might indicate a systemic issue?

---

### Task 3: Exploring Traces

Create a file `explore_traces.py`:

```python
#!/usr/bin/env python3
"""Explore distributed trace data."""

import json
from datetime import datetime
import random

def generate_trace():
    """Generate a sample distributed trace."""
    trace_id = f"trace-{random.randint(100000, 999999)}"
    
    # Simulate a request flow
    trace = {
        "trace_id": trace_id,
        "timestamp": datetime.now().isoformat(),
        "spans": []
    }
    
    # Root span - API Gateway
    root_start = 0
    api_duration = random.randint(5, 15)
    
    # Auth service
    auth_start = api_duration
    auth_duration = random.randint(2, 10)
    
    # Database lookup
    db_start = auth_start + auth_duration
    db_duration = random.randint(1, 5)
    
    # Main service
    main_start = auth_start + auth_duration
    main_duration = random.randint(20, 100)
    
    # External API call (sometimes slow)
    ext_start = main_start + 10
    ext_duration = random.randint(10, 500)  # Can be slow!
    
    trace["spans"] = [
        {
            "span_id": "span-001",
            "parent_id": None,
            "service": "api-gateway",
            "operation": "handleRequest",
            "start_ms": root_start,
            "duration_ms": main_start + main_duration + 5,
            "status": "OK"
        },
        {
            "span_id": "span-002", 
            "parent_id": "span-001",
            "service": "auth-service",
            "operation": "validateToken",
            "start_ms": auth_start,
            "duration_ms": auth_duration,
            "status": "OK"
        },
        {
            "span_id": "span-003",
            "parent_id": "span-002",
            "service": "user-db",
            "operation": "SELECT",
            "start_ms": db_start,
            "duration_ms": db_duration,
            "status": "OK"
        },
        {
            "span_id": "span-004",
            "parent_id": "span-001",
            "service": "order-service",
            "operation": "processOrder",
            "start_ms": main_start,
            "duration_ms": main_duration,
            "status": "OK"
        },
        {
            "span_id": "span-005",
            "parent_id": "span-004",
            "service": "payment-api",
            "operation": "chargeCard",
            "start_ms": ext_start,
            "duration_ms": ext_duration,
            "status": "OK" if ext_duration < 300 else "SLOW"
        }
    ]
    
    trace["total_duration_ms"] = max(s["start_ms"] + s["duration_ms"] for s in trace["spans"])
    
    return trace

def visualize_trace(trace):
    """Print a visual representation of the trace."""
    print(f"\n🔍 Trace: {trace['trace_id']}")
    print(f"   Total Duration: {trace['total_duration_ms']}ms")
    print("-" * 60)
    
    # Sort spans by start time
    spans = sorted(trace["spans"], key=lambda x: x["start_ms"])
    
    for span in spans:
        indent = "  " if span["parent_id"] else ""
        if span["parent_id"]:
            parent_indent = "  " if any(s["span_id"] == span["parent_id"] and s["parent_id"] for s in spans) else ""
            indent = parent_indent + "└─"
        
        status_icon = "🚨" if span["status"] == "SLOW" else "✅"
        
        print(f"{indent}{span['service']}.{span['operation']}")
        print(f"{indent}  {status_icon} {span['duration_ms']}ms (start: {span['start_ms']}ms)")

# Generate and analyze multiple traces
print("🔗 Generating distributed traces...\n")

traces = [generate_trace() for _ in range(10)]

# Find slow traces
slow_threshold = 200
slow_traces = [t for t in traces if t["total_duration_ms"] > slow_threshold]

print(f"Generated {len(traces)} traces")
print(f"Slow traces (>{slow_threshold}ms): {len(slow_traces)}")

# Visualize a slow trace if found
if slow_traces:
    print("\n📊 Example slow trace:")
    visualize_trace(slow_traces[0])
    
    # Find bottleneck
    bottleneck = max(slow_traces[0]["spans"], key=lambda x: x["duration_ms"])
    print(f"\n⚠️  Bottleneck: {bottleneck['service']}.{bottleneck['operation']} took {bottleneck['duration_ms']}ms")
else:
    print("\n📊 Example trace:")
    visualize_trace(traces[0])

# Service latency analysis
service_durations = {}
for trace in traces:
    for span in trace["spans"]:
        svc = span["service"]
        if svc not in service_durations:
            service_durations[svc] = []
        service_durations[svc].append(span["duration_ms"])

print("\n📈 Average latency by service:")
for svc, durations in sorted(service_durations.items()):
    avg = sum(durations) / len(durations)
    max_d = max(durations)
    print(f"  {svc}: avg={avg:.1f}ms, max={max_d}ms")

# Save sample trace
with open('sample_trace.json', 'w') as f:
    json.dump(traces[0], f, indent=2)
print("\n✅ Sample saved to sample_trace.json")
```

Run and observe:
```bash
python explore_traces.py
```

**Questions to answer:**
1. Which service is the bottleneck?
2. How do traces help identify issues that metrics alone wouldn't reveal?
3. What would you alert on based on trace data?

---

## 📊 Submission

Create a file `answers.md` with your answers to all questions from the three tasks.

---

<p align="center">
  <a href="exercise-01-setup.md">← Previous</a> | <a href="exercise-03-use-cases.md">Next: Exercise 3 →</a>
</p>
