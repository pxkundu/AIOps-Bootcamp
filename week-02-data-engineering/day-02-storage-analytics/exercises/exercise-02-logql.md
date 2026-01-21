# Exercise 2: Master of LogQL (Loki)

## 🎯 Objective
Run a high-speed search and aggregation exercise using Grafana Loki. Learn how to transform raw logs into metrics using only the query language.

---

## 🛠️ Step 1: The Loki Stack

Update your `docker-compose.yml` to include Loki:

```yaml
  loki:
    image: grafana/loki:2.9.0
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:2.9.0
    volumes:
      - /var/log:/var/log
      - ./promtail-config.yaml:/etc/promtail/config.yaml
    command: -config.file=/etc/promtail/config.yaml
```

---

## 📝 Step 2: The LogQL Hunt

Open Grafana (usu. http://localhost:3000) and add Loki as a data source (http://loki:3100).

Go to **Explore** and select Loki.

### Task 1: Basic Search
Find all logs containing the string "error" but excluding "timeout".
**Query:** `{job="varlogs"} |= "error" != "timeout"`

### Task 2: Regex Extraction
Extract a `user_id` from a log line formatted like `User 123 logged out`.
**Query:** `{job="varlogs"} | regexp "User (?P<user_id>\\d+) logged out"`

### Task 3: Converting Logs to Metrics (The AIOps Magic)
Calculate the **Error Rate (errors per second)** over the last 5 minutes.
**Query:** `sum(rate({job="varlogs"} |= "error" [5m]))`

---

## 📊 Step 3: Visualization Challenge

Build a Grafana panel that shows the **Average Response Time** extracted from logs using LogQL.

**Hint:**
1. Use `| json` to parse the log.
2. Use `| unwrap latency` to treat the 'latency' field as a number.
3. Apply `avg_over_time(...[5m])`.

---

## 🧪 Questions

1. **Schema-on-Read:** What happens if the log format changes (e.g., `latency` becomes `duration`)? Do you need to update the database schema or just your LogQL query?
2. **Cardinality:** Why is it a bad idea to add `user_id` as a **label** in Loki compared to adding it as a **field** in Elasticsearch?
3. **Performance:** Run a query over the last 24 hours. Does Loki feel faster than a similar query in a plain text file? Why?
