# Log Engineering Cheat Sheet

> Quick reference for Fluent Bit, Kafka, and JSON Log Processing.

---

## 🔥 Fluent Bit Configuration
Location: `/etc/td-agent-bit/td-agent-bit.conf`

### Common Input (Tail)
```ini
[INPUT]
    Name   tail
    Path   /var/log/syslog
    Tag    system.logs
    DB     /var/log/flb_tail.db  # Track position
```

### Common Filter (Grepping)
```ini
[FILTER]
    Name    grep
    Match   *
    Exclude log /.*health_check.*/
```

### Common Output (Elasticsearch)
```ini
[OUTPUT]
    Name            es
    Match           *
    Host            elasticsearch
    Port            9200
    Index           logs-%Y.%m.%d
    Type            _doc
```

---

## 🦅 Apache Kafka CLI Reference
Assuming Kafka is in Docker.

### List Topics
```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Consume Logs (Debug)
```bash
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic raw-logs --from-beginning
```

### Check Topic Offsets
```bash
docker exec -it kafka kafka-run-class kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic raw-logs
```

---

## 🛠️ Log Parsing & Transformation

### Python: Writing Structured Logs
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        return json.dumps(log_record)

logger = logging.getLogger("App")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

### Regex Helper for Classic Logs
| Pattern | Meaning | Example |
|---------|---------|---------|
| `(?<ts>\d{4}-\d{2}-\d{2})` | Date (YYYY-MM-DD) | `2024-01-19` |
| `(?<ip>\d{1,3}(?:\.\d{1,3}){3})` | IP Address | `192.168.1.1` |
| `(?<level>INFO|DEBUG|ERROR)` | Log Levels | `ERROR` |
| `(?<msg>.*)` | Capture everything | `Service started` |

---

## 🔍 Log Sampling Strategies

| Type | Description | Best For |
|------|-------------|----------|
| **Random** | Keep 10% of all logs. | General trends, high traffic. |
| **Priority** | Keep all ERROR, 5% of INFO. | Troubleshooting & Alerts. |
| **Tail-based** | Keep full trace if error occurs. | Distributed Debugging. |
| **Dynamic** | Increase sampling rate during anomalies. | Adaptive Observability. |

---

## 🚨 Troubleshooting Checklist

1. **Fluent Bit:** Check if internal metrics are exported (`http_server on`).
2. **Buffer:** Monitor `kafka_topic_partition_current_offset` vs `sum(offset)`. Increase partition count if lagging.
3. **Parsing:** Use [regex101.com](https://regex101.com) to test your Fluent Bit parsers.
4. **Volume:** Check if `container_memory_usage_bytes` of the collector is spiking (possible memory leak with high-volume regex).
