# Exercise 3: Real-Time Metrics Pipeline for Anomaly Detection

> **Duration:** 3 hours | **Difficulty:** Advanced
> **Objective:** Build an end-to-end pipeline that streams metrics to a ML model for real-time anomaly detection.

---

## 🎯 Learning Goals

By completing this exercise, you will:
1. Set up Prometheus Remote Write to stream metrics.
2. Build a Kafka-based metrics streaming pipeline.
3. Implement a simple anomaly detection model.
4. Create alerting based on ML predictions.

---

## 📋 Scenario

You're building an **AIOps platform** that needs to:
- Stream metrics from Prometheus in real-time
- Detect anomalies using statistical methods
- Alert operations team when anomalies are detected
- Store predictions for model improvement

**Architecture:**
```
Prometheus → Remote Write → Kafka → Spark/Flink → ML Model → Alert Manager
```

---

## 🛠️ Requirements

### Part 1: Prometheus Remote Write Setup (45 minutes)

1. **Install and configure Prometheus with remote write:**
   ```yaml
   # prometheus.yml
   global:
     scrape_interval: 15s
   
   remote_write:
     - url: "http://kafka-connect:8083/connectors/prometheus-remote-write"
       queue_config:
         max_samples_per_send: 1000
         batch_send_deadline: 5s
   
   scrape_configs:
     - job_name: 'node-exporter'
       static_configs:
         - targets: ['node-exporter:9100']
   ```

2. **Alternative: Use Prometheus Remote Write Adapter for Kafka**
   - Create a service that receives remote write requests
   - Convert Prometheus samples to Kafka messages
   - Publish to Kafka topic: `prometheus-metrics`

3. **Create `remote_write_adapter.py`:**
   ```python
   from flask import Flask, request
   from kafka import KafkaProducer
   import json
   import time
   
   app = Flask(__name__)
   producer = KafkaProducer(
       bootstrap_servers='localhost:9092',
       value_serializer=lambda v: json.dumps(v).encode('utf-8')
   )
   
   @app.route('/receive', methods=['POST'])
   def receive_metrics():
       data = request.get_json()
       # Parse Prometheus remote write format
       for timeseries in data.get('timeseries', []):
           for sample in timeseries.get('samples', []):
               message = {
                   'metric': timeseries['labels'],
                   'value': sample['value'],
                   'timestamp': sample['timestamp']
               }
               producer.send('prometheus-metrics', message)
       return {'status': 'ok'}, 200
   
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8080)
   ```

### Part 2: Kafka Consumer & Feature Engineering (60 minutes)

1. **Create `metrics_processor.py`** that:
   - Consumes from `prometheus-metrics` topic
   - Computes rolling window statistics (mean, std, z-score)
   - Detects anomalies using statistical methods
   - Publishes anomalies to `anomaly-alerts` topic

2. **Implement rolling window:**
   ```python
   from collections import deque
   import statistics
   
   class RollingWindow:
       def __init__(self, window_size=60):
           self.window_size = window_size
           self.values = deque(maxlen=window_size)
       
       def add(self, value):
           self.values.append(value)
       
       def mean(self):
           return statistics.mean(self.values) if self.values else 0
       
       def std(self):
           return statistics.stdev(self.values) if len(self.values) > 1 else 0
       
       def z_score(self, value):
           mean = self.mean()
           std = self.std()
           if std == 0:
               return 0
           return (value - mean) / std
   ```

3. **Anomaly Detection Logic:**
   ```python
   def detect_anomaly(metric_name, value, window):
       z_score = window.z_score(value)
       
       # Anomaly if |z-score| > 3 (3-sigma rule)
       if abs(z_score) > 3:
           return {
               'metric': metric_name,
               'value': value,
               'z_score': z_score,
               'mean': window.mean(),
               'std': window.std(),
               'timestamp': time.time(),
               'severity': 'high' if abs(z_score) > 4 else 'medium'
           }
       return None
   ```

### Part 3: ML Model Integration (45 minutes)

1. **Create a simple Isolation Forest model:**
   ```python
   from sklearn.ensemble import IsolationForest
   import numpy as np
   
   class AnomalyDetector:
       def __init__(self):
           self.model = IsolationForest(contamination=0.1, random_state=42)
           self.is_fitted = False
       
       def fit(self, features):
           """Train on historical data"""
           self.model.fit(features)
           self.is_fitted = True
       
       def predict(self, features):
           """Predict anomalies (-1 = anomaly, 1 = normal)"""
           if not self.is_fitted:
               return None
           return self.model.predict(features.reshape(1, -1))[0]
   ```

2. **Feature Engineering:**
   ```python
   def extract_features(metric_name, value, window):
       """Extract features for ML model"""
       return np.array([
           value,                    # Current value
           window.mean(),           # Rolling mean
           window.std(),            # Rolling std
           window.z_score(value),   # Z-score
           len(window.values),      # Window size
       ])
   ```

### Part 4: Alert Manager Integration (30 minutes)

1. **Create `alert_publisher.py`** that:
   - Consumes from `anomaly-alerts` topic
   - Formats alerts in Prometheus Alertmanager format
   - Sends to Alertmanager API

2. **Alert Format:**
   ```python
   alert = {
       'labels': {
           'alertname': 'MetricAnomaly',
           'metric': metric_name,
           'severity': severity,
           'instance': instance
       },
       'annotations': {
           'summary': f'Anomaly detected in {metric_name}',
           'description': f'Value: {value}, Z-score: {z_score:.2f}'
       },
       'startsAt': datetime.utcnow().isoformat()
   }
   ```

3. **Send to Alertmanager:**
   ```python
   import requests
   
   def send_alert(alert):
       url = 'http://alertmanager:9093/api/v1/alerts'
       response = requests.post(url, json=[alert])
       return response.status_code == 200
   ```

---

## 🏗️ Complete Pipeline Architecture

```mermaid
graph LR
    PROM[Prometheus] -->|Remote Write| ADAPTER[Remote Write Adapter]
    ADAPTER -->|Kafka| KAFKA[prometheus-metrics Topic]
    KAFKA -->|Consume| PROCESSOR[Metrics Processor]
    PROCESSOR -->|Features| ML[ML Model]
    ML -->|Anomalies| ALERTS[anomaly-alerts Topic]
    ALERTS -->|Publish| ALERTMGR[Alert Manager]
    ALERTMGR -->|Notify| SLACK[Slack/PagerDuty]
```

---

## ✅ Success Criteria

- [ ] Prometheus successfully writes metrics to Kafka
- [ ] Metrics processor computes rolling statistics
- [ ] Anomaly detection identifies outliers (z-score > 3)
- [ ] ML model is trained and makes predictions
- [ ] Alerts are sent to Alertmanager
- [ ] End-to-end pipeline processes metrics in real-time

---

## 🎓 Bonus Challenges

1. **Multi-Metric Correlation:**
   - Detect anomalies based on correlation between multiple metrics
   - Example: CPU spike + Memory spike + Network drop = potential issue

2. **Adaptive Thresholds:**
   - Learn normal behavior patterns per time-of-day
   - Adjust anomaly thresholds dynamically

3. **Grafana Integration:**
   - Create a Grafana dashboard showing anomaly predictions
   - Visualize z-scores and model confidence

4. **Model Retraining:**
   - Implement periodic retraining on new data
   - A/B test different anomaly detection algorithms

---

## 📚 Resources

- [Prometheus Remote Write](https://prometheus.io/docs/prometheus/latest/storage/#remote-storage-integrations)
- [Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [Kafka Python Client](https://kafka-python.readthedocs.io/)

---

## 💡 Hints

- Use `confluent-kafka-python` for better performance
- Implement backpressure handling (pause/resume consumer)
- Store model state in Redis for distributed processing
- Use async processing for better throughput

---

## 🐳 Docker Compose Setup

```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
  
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
  
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
```

---

<p align="center">
  <a href="exercise-02-aggregation.md">← Previous Exercise</a> | 
  <a href="../project/README.md">Go to Project →</a>
</p>
