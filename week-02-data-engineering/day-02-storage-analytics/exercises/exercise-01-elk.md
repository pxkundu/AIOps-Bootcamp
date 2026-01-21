# Exercise 1: The ELK Transformation Lab

## 🎯 Objective
Assemble a full ELK stack (Elasticsearch, Logstash, Kibana) and build a transformation pipeline that enriches logs with geographic data and statistical metadata.

---

## 🛠️ Step 1: The Stack Setup

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:7.17.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

---

## 📝 Step 2: The Logstash Pipeline

Create `logstash.conf`. This pipeline will:
1. Accept logs on UDP port 5000.
2. Use a **Grok** filter to parse a custom web log format.
3. Use a **GeoIP** filter.
4. Add a field `log_processed_by: "AIOps-Logstash"`.

```ruby
input {
  udp {
    port => 5000
    codec => json
  }
}

filter {
  # Example: Parsing an IP from a message if it wasn't already JSON
  if [client_ip] {
    geoip {
      source => "client_ip"
      target => "geo"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "aiops-logs-%{+YYYY.MM.dd}"
  }
  stdout { codec => rubydebug }
}
```

---

## 🐍 Step 3: Pushing Enriched Data

Create `push_logs.py`:

```python
import socket
import json
import time
import random

def send_log(ip):
    data = {
        "client_ip": ip,
        "method": "GET",
        "url": "/api/checkout",
        "status": 200,
        "latency": random.randint(100, 2000)
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(data).encode(), ("localhost", 5000))

# Sample Global IPs
ips = ["8.8.8.8", "1.1.1.1", "139.130.4.5", "185.33.22.1"]

while True:
    send_log(random.choice(ips))
    time.sleep(2)
```

---

## 📊 Step 4: Verification in Kibana

1. Open http://localhost:5601.
2. Go to **Management > Stack Management > Index Patterns**.
3. Create index pattern: `aiops-logs-*`.
4. Go to **Analytics > Discover**.
5. **Analyze:** Check the `geo.country_name` field. Did Logstash successfully resolve the IPs?

---

## 🧪 Challenges

1. **Latencies:** Some logs have `latency > 1500`. In Kibana, use the search bar to find only these logs.
2. **Alerting Simulation:** What if you wanted to alert when `geo.country_name: "China"`? Draft the KQL query.
3. **Drop Fields:** Modify the Logstash filter to `remove_field => ["@version", "host"]` to save space. Restart Logstash and verify.
