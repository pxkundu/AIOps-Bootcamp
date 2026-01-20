# Exercise: Building a Resilient Log Pipeline (Fluent Bit + Kafka)

## 🎯 Objective
Set up a pipeline where a Python application generates structured logs, Fluent Bit collects them, and Kafka buffers them for analysis.

---

## 🛠️ Step 1: The Infrastructure

Create a `docker-compose.yml` in your current directory:

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
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  fluent-bit:
    image: fluent/fluent-bit:latest
    depends_on:
      - kafka
    volumes:
      - ./fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf
      - ./app-logs:/var/log/app
    ports:
      - "24224:24224"
```

---

## 📝 Step 2: Fluent Bit Configuration

Create `fluent-bit.conf`:

```ini
[SERVICE]
    Flush        1
    Daemon       Off
    Log_Level    info

[INPUT]
    Name         tail
    Path         /var/log/app/events.log
    Tag          app.v1

[OUTPUT]
    Name         kafka
    Match        *
    Brokers      kafka:29092
    Topics       app-logs
    Format       json
```

---

## 🐍 Step 3: The Log Generator

Create `log_gen.py`:

```python
import time
import json
import random

LOG_FILE = "app-logs/events.log"

def generate_log():
    levels = ["INFO", "ERROR", "DEBUG"]
    users = [101, 202, 303, 404]
    
    event = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": random.choice(levels),
        "user_id": random.choice(users),
        "message": "User action performed",
        "latency_ms": random.randint(10, 500)
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    import os
    if not os.path.exists("app-logs"):
        os.makedirs("app-logs")
        
    print("Generating logs... Press Ctrl+C to stop.")
    while True:
        generate_log()
        time.sleep(1)
```

---

## 🚀 Step 4: Execution & Validation

1. **Start the stack:**
   ```bash
   docker-compose up -d
   ```

2. **Run the generator:**
   ```bash
   python3 log_gen.py
   ```

3. **Verify Kafka is receiving logs:**
   ```bash
   docker exec -it $(docker ps -qf name=kafka) \
     kafka-console-consumer --bootstrap-server localhost:9092 --topic app-logs --from-beginning
   ```

---

## 🧪 Challenge Questions

1. **Schema Check:** Are the logs in Kafka identical to the ones in `events.log`, or has Fluent Bit added metadata? If so, which fields?
2. **Crash Test:** Stop the Kafka container (`docker-compose stop kafka`). Keep the Python script running. Wait 1 minute. Start Kafka. Did you lose the logs generated during wait? Why or why not? (Check Fluent Bit's `Flush` and `Retry_Limit` parameters).
3. **Filtering:** Modify `fluent-bit.conf` to add a `grep` filter that EXCLUDES all logs with `level: DEBUG`. Restart Fluent Bit and verify results in Kafka.
