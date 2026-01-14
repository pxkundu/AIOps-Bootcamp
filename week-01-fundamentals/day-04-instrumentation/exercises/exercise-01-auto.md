# Exercise 1: Auto-Instrumentation with OpenTelemetry

## 🎯 Objective
Experience zero-code instrumentation using OpenTelemetry's automatic instrumentation capabilities.

---

## 📋 Prerequisites
- Python 3.10+
- Docker and Docker Compose running
- Completed Day 3 stack deployment

---

## 🚀 Part 1: Setup Auto-Instrumentation

### Step 1: Install OTel Distro
```bash
cd ~/codebase/AIOps-Bootcamp/week-01-fundamentals/day-04-instrumentation/examples

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install OpenTelemetry distribution
pip install opentelemetry-distro
pip install opentelemetry-exporter-otlp

# Auto-install instrumentation for detected libraries
opentelemetry-bootstrap -a install
```

### Step 2: Create Simple Flask App
**File: `simple_app.py`**
```python
from flask import Flask, jsonify
import requests
import time
import random

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/users')
def get_users():
    # Simulate database query
    time.sleep(random.uniform(0.01, 0.05))
    return jsonify([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])

@app.route('/external')
def call_external():
    # Simulate external API call
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
```

### Step 3: Run with Auto-Instrumentation
```bash
opentelemetry-instrument \
    --traces_exporter otlp \
    --metrics_exporter otlp \
    --service_name simple-flask-app \
    --exporter_otlp_endpoint http://localhost:4317 \
    python simple_app.py
```

---

## 🔍 Part 2: Generate Traffic & Observe

### Generate Requests
```bash
# In another terminal
for i in {1..20}; do
    curl http://localhost:5000/users
    curl http://localhost:5000/external
    sleep 1
done
```

### Observe in Jaeger
1. Open http://localhost:16686
2. Select Service: `simple-flask-app`
3. Click "Find Traces"

**What to Look For:**
- ✅ Automatic spans for HTTP requests
- ✅ Automatic spans for `requests` library calls
- ✅ Span attributes (http.method, http.url, http.status_code)
- ✅ Parent-child relationships

**Screenshot Challenge:** Take screenshots showing:
1. A complete trace with multiple spans
2. The span details showing automatic attributes

---

## 📊 Part 3: View Metrics in Prometheus

### Query Auto-Generated Metrics
Open http://localhost:9090 and run:

```promql
# Request duration (automatically created!)
http_server_duration_milliseconds_count

# Active requests
http_server_active_requests

# Request size
http_server_request_size_bytes
```

**Questions:**
1. What labels are automatically added to metrics?
2. How does auto-instrumentation determine metric names?

---

## 🎨 Part 4: Environment Variables Configuration

Try different configurations:

### Higher Sampling Rate
```bash
export OTEL_TRACES_SAMPLER=traceidratio
export OTEL_TRACES_SAMPLER_ARG=0.5  # Sample 50%

opentelemetry-instrument python simple_app.py
```

### Custom Resource Attributes
```bash
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=dev,service.version=1.0.0"

opentelemetry-instrument python simple_app.py
```

### Disable Specific Instrumentations
```bash
# Disable requests instrumentation
export OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=requests

opentelemetry-instrument python simple_app.py
```

---

## ✅ Deliverables

Create `exercise-01-report.md` with:
1. Screenshot of Jaeger showing auto-instrumented traces
2. List of automatic span attributes you discovered
3. Three PromQL queries for auto-generated metrics
4. Comparison: What did you get "for free" without code changes?

---

## 💡 Bonus Challenges

1. **Add Database:** Install PostgreSQL instrumentation and observe DB queries
2. **Multi-Service:** Create a second service and watch context propagation
3. **Custom Attributes:** Use environment variables to add custom resource attributes
4. **Sampling Strategy:** Experiment with different sampling rates and observe impact

---

## 🐛 Troubleshooting

**Issue: No traces appearing**
```bash
# Check if exporter endpoint is correct
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Enable debug logging
export OTEL_LOG_LEVEL=debug

# Verify Jaeger is running
docker ps | grep jaeger
```

**Issue: Some libraries not auto-instrumented**
```bash
# List available instrumentations
opentelemetry-bootstrap -a list

# Check if library is supported
pip list | grep opentelemetry
```
