# Exercise 01: Deploying and Querying InfluxDB 2.x

## 🎯 Objective
Deploy a native TSDB (InfluxDB 2.x) and learn the "Functional" approach to time-series data using Flux.

---

## 📋 Prerequisites
- Docker and Docker Compose installed.
- Python 3.10+ installed locally.

---

## 🛠️ Step 1: Deploying the Stack

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  influxdb:
    image: influxdb:2.7
    ports:
      - "8086:8086"
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=adminpassword
      - DOCKER_INFLUXDB_INIT_ORG=aiops_academy
      - DOCKER_INFLUXDB_INIT_BUCKET=telemetry_bucket
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token
```

Start the service:
```bash
docker-compose up -d
```

---

## 📝 Step 2: Writing Data (The Python Way)

Install the client:
```bash
pip install influxdb-client
```

Create `ingest_metrics.py`:
```python
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

token = "my-super-secret-auth-token"
org = "aiops_academy"
bucket = "telemetry_bucket"

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    point = Point("cpu_usage") \
        .tag("host", f"server-{random.randint(1, 4)}") \
        .field("usage", random.uniform(20.0, 90.0)) \
        .time(time.time_ns(), WritePrecision.NS)
    
    write_api.write(bucket, org, point)
    print(f"Sent point: {point}")
    time.sleep(1)
```

Run the script:
```bash
python ingest_metrics.py
```

---

## 🔍 Step 3: Querying with Flux

1. Open http://localhost:8086 (Login: admin / adminpassword)
2. Go to **Explore**
3. Switch to **Script Editor** and run these queries:

### Task 1: Basic View
```js
from(bucket: "telemetry_bucket")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
```

### Task 2: Aggregated Window (Moving Average)
```js
from(bucket: "telemetry_bucket")
  |> range(start: -15m)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
  |> aggregateWindow(every: 10s, fn: mean)
```

### Task 3: Identify the "Hottest" Host
```js
from(bucket: "telemetry_bucket")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "cpu_usage")
  |> mean()
  |> group(columns: ["_value"])
  |> sort(columns: ["_value"], desc: true)
```

---

## 🧪 Challenge Question
Look at how many "Series" you've created. Go to **Dashboards -> InfluxDB Measurements** and check the storage stats. What happens to the internal index if you add `process_id` as a **Tag**? (Hint: DON'T DO IT in production!)

## ✅ Submission
Submit a screenshot of your Flux query result showing the moving average of at least 3 simulated hosts.
