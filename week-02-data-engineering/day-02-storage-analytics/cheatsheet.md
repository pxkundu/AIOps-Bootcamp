# Log Analytics & Querying Cheat Sheet

> Master the languages of log search and transformation.

---

## 🔍 Elasticsearch / Kibana (KQL & Lucene)

### Kibana Query Language (KQL)
Used in the Kibana search bar.
- **Match field:** `level: "error"`
- **Range:** `duration_ms > 500`
- **AND/OR:** `level: "error" AND service: "checkout"`
- **Wildcard:** `user_agent: *Chrome*`
- **Exists:** `transaction_id: *`

### Lucene Syntax
Used in advanced filters.
- **Regex:** `message: /.*timeout.*/`
- **Proximity:** `"service crash"~3` (words within 3 positions)
- **Fuzzy:** `service: chekout~1` (matches checkout)

---

## 📈 Grafana Loki (LogQL)

### Selection & Filtering
`{app="api", env="prod"} |= "error" != "timeout"`
- `{label="value"}`: Stream selector.
- `|=`: Contains string.
- `!=`: Does not contain string.
- `|~`: Regex match.
- `!~`: Regex not match.

### Transformations & Aggregations
`sum(count_over_time({app="api"} |= "error" [5m]))`
- **JSON extraction:** `| json` (automatically turns JSON keys into labels)
- **Logfmt parsing:** `| logfmt`
- **Label extraction:** `| regexp "(?P<user_id>\d+)"`

---

## 🛠️ Logstash Grok Patterns (Common)

| Pattern | Description | Example |
|---------|-------------|---------|
| `%{COMBINEDAPACHELOG}` | Standard Apache/Nginx logs | `127.0.0.1 - - [10/Jan...] "GET /..."` |
| `%{TIMESTAMP_ISO8601:ts}` | ISO8601 Times | `2024-01-20T22:21:41Z` |
| `%{LOGLEVEL:level}` | INFO, ERROR, WARN, etc. | `ERROR` |
| `%{UUID:req_id}` | UUID / GUIDs | `550e8400-e29b-...` |
| `%{GREEDYDATA:msg}` | Match everything else | `... rest of line` |

---

## 🏎️ Vector.dev (Remap Language - VRL)

### Basic Parse
```vrl
. = parse_json!(.message)
.new_field = "AIOps-Processed"
.latency_s = .latency_ms / 1000.0
```

### Conditional Filter
```vrl
if .level == "DEBUG" {
    abort
}
```

---

## 📊 Dashboard Visualizations Checklist

- [ ] **Heatmap:** Request latency over time.
- [ ] **Data Table:** List of recent errors with TraceIDs.
- [ ] **Gauge:** Current CPU saturation of the logging node.
- [ ] **Pie Chart:** Distribution of HTTP Status Codes (2xx vs 4xx vs 5xx).
- [ ] **Time Series:** Ingestion rate (logs per second) to monitor "Log Storms."

---

## 💡 AIOps Pro-Tip: "Rare Event" Detection
In Kibana, use the **Significant Terms** aggregation to find log messages that are suddenly appearing more frequently than their historical baseline. This is often the first sign of a new bug.
