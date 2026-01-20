# Day 1 Project: The Intelligent Log Pre-Processor

> **Challenge:** Build a Python-based middleware that analyzes log streams in real-time to detect volume spikes (potential DDoS or crash loops) and prioritizes data for downstream ML models.

---

## 🎯 Project Overview

In a real AIOps setup, we don't just dump data into a database. We pre-process it. Your goal is to create a service that:
1. Consumes the `raw-logs` stream from Kafka.
2. Identifies a "Rate Spike" (e.g., more than 10 logs in 5 seconds).
3. If a spike is detected, tags the logs as `priority: high`.
4. Routes `ERROR` logs to a `critical-events` topic and everything else to `processed-logs`.

## 🏗️ Architecture

```
[Log Generator] -> [Fluent Bit] -> [Kafka: raw-logs] -> [Your Pre-Processor]
                                                        |
                                                        V
                                          [Kafka: critical-events]
                                          [Kafka: processed-logs]
```

---

## 📋 Requirements

### 1. The Consumer
- Use `kafka-python` or `confluent-kafka-python` library.
- Safely handle JSON parsing errors (unstructured logs should go to a `dead-letter-queue`).

### 2. The Logic (The "Ops" in AIOps)
- **Rate Limit Check:** Keep a windowed count of incoming logs.
- **Pattern Matching:** Detect if a log contains sensitive information (e.g., "password", "token") and mask it with `********`.

### 3. The Producer
- High-priority logs should be sent with a higher compression level or prioritized partitioning (conceptually).
- Add a field `pre_processed_at` with a precise microsecond timestamp to track pipeline latency.

---

## 🚀 Starter Code Snippet

```python
from kafka import KafkaConsumer, KafkaProducer
import json
import time

# Configuration
KAFKA_SERVER = 'localhost:9092'
INPUT_TOPIC = 'raw-logs'

consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

print(f"Pre-Processor started on {INPUT_TOPIC}...")

for message in consumer:
    log = message.value
    # TODO: Implement spike detection logic
    # TODO: Implement masking logic
    # TODO: Implement routing logic
    print(f"Processing log: {log['level']}")
```

---

## ✅ Evaluation Rubric

| Criteria | Points |
|----------|--------|
| **Resilience:** Service doesn't crash on malformed JSON. | 25 |
| **Logic:** Successfully detects a volume spike. | 25 |
| **Security:** Successfully masks sensitive string patterns. | 20 |
| **Routing:** Logs are split into topics based on severity correctly. | 20 |
| **Observability:** Service logs its OWN processing latency. | 10 |

---

## 📤 Submission
Submit your `processor.py` and a short `README.md` explaining how you implemented the spike detection window.
