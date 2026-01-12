# AIOps Observability Cheat Sheet

> **Quick reference for Metrics, Logs, and Traces.**

---

## 📊 Metrics (Prometheus/OpenMetrics)

### Common Metric Types
| Type | Use Case | Example |
| :--- | :--- | :--- |
| **Counter** | Cumulative totals | `http_requests_total` |
| **Gauge** | Value at a point in time | `node_memory_usage_bytes` |
| **Histogram** | Latency distribution (server-side) | `http_request_duration_seconds_bucket` |
| **Summary** | Latency distribution (client-side) | `http_request_duration_seconds{quantile="0.95"}` |

### PromQL Basics
*   `rate(metric_total[5m])`: Average per-second increase over 5 mins.
*   `sum by (job) (rate(...))`: Group results by a specific label.
*   `histogram_quantile(0.95, sum by (le) (rate(...)))`: Calculate p95 latency.

---

## 📝 Logs (Structured Logging)

### Recommended JSON Fields
```json
{
  "timestamp": "ISO8601 string",
  "level": "INFO, WARN, ERROR, DEBUG",
  "service": "Service name",
  "trace_id": "For correlation",
  "span_id": "For specific operation",
  "msg": "Human readable message",
  "context": { "user_id": 123, "org_id": "abc" }
}
```

### Log Levels
*   **DEBUG**: Verbose info for dev/troubleshooting.
*   **INFO**: Standard operational events (e.g., service started).
*   **WARN**: System is still healthy but might have future issues.
*   **ERROR**: Call became a failure (e.g., 500 error).
*   **FATAL**: Service is unrecoverable and stopping.

---

## 🔗 Traces (Otel/Jaeger)

### Key Terms
*   **Trace ID**: 128-bit unique ID for one request.
*   **Span ID**: 64-bit ID for a single unit of work.
*   **Tags/Attributes**: Key-value pairs (e.g., `db.statement`, `http.status_code`).
*   **Events**: Log-like messages attached to a span (e.g., "Cache Miss").

### Context Propagation
How the Trace ID is sent between services:
*   **W3C Trace Context**: The modern standard (`traceparent` header).
*   **B3**: Legacy Zipkin/Jaeger standard.

---

## 🚦 Troubleshooting Decision Matrix

| IF | USE |
| :--- | :--- |
| "Is my system up?" | **Metrics** |
| "Are we hitting our SLA?" | **Metrics** |
| "Which step in the checkout is slow?" | **Traces** |
| "What exactly did the DB say when it failed?" | **Logs** |
| "Is my CPU spiking every Monday morning?" | **Metrics** |

---

## 🧠 Cardinality Checklist
- [ ] Is it a unique ID (User, Request, Email)? → **DON'T** use as a label.
- [ ] Is it a constant or small set of values (Region, Env, Code)? → **DO** use as a label.
- [ ] Will this create > 100,000 unique series? → **Re-evaluate** labels.
