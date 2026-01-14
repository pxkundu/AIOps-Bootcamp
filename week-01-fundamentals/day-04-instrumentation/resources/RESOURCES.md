# Day 4 Resources: OpenTelemetry Best Practices

> **Advanced materials for mastering OpenTelemetry instrumentation.**

---

## 🌐 Official Documentation

### OpenTelemetry Core
*   **[OpenTelemetry Docs](https://opentelemetry.io/docs/)** - Official comprehensive guide
*   **[Specification](https://github.com/open-telemetry/opentelemetry-specification)** - Technical specifications
*   **[Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)** - Standard attribute naming
*   **[Registry](https://opentelemetry.io/ecosystem/registry/)** - All available instrumentations

### Language-Specific Guides
*   **[Python](https://opentelemetry.io/docs/instrumentation/python/)** - Python SDK and instrumentation
*   **[JavaScript/Node.js](https://opentelemetry.io/docs/instrumentation/js/)** - JS ecosystem
*   **[Go](https://opentelemetry.io/docs/instrumentation/go/)** - Go implementation
*   **[Java](https://opentelemetry.io/docs/instrumentation/java/)** - Java agent and SDK

---

## 📖 Learning Resources

### Interactive Tutorials
*   **[OTel Playground](https://killercoda.com/opentelemetry)** - Hands-on scenarios
*   **[Lightstep Learning](https://lightstep.com/learn/opentelemetry)** - Video courses
*   **[Grafana Labs Tutorials](https://grafana.com/tutorials/opentelemetry/)** - Integration guides

### Articles & Blog Posts
*   **[OTel Best Practices](https://opentelemetry.io/docs/concepts/instrumentation/libraries/)** - Official patterns
*   **[Context Propagation Deep Dive](https://medium.com/opentelemetry/context-propagation-in-opentelemetry-d5f52d15ff0e)** - Technical explanation
*   **[Sampling Strategies](https://lightstep.com/blog/opentelemetry-sampling/)** - When and how to sample

### Books
*   **"Distributed Tracing in Practice"** by Austin Parker et al. - OTel patterns
*   **"Observability Engineering"** by Charity Majors - Context and philosophy

---

## 🛠️ Tools & Ecosystem

### OTel Collector
*   **[Collector Documentation](https://opentelemetry.io/docs/collector/)** - Deployment and configuration
*   **[Collector Builder](https://github.com/open-telemetry/opentelemetry-collector-builder)** - Custom builds
*   **[Contrib Repo](https://github.com/open-telemetry/opentelemetry-collector-contrib)** - Additional receivers/exporters

### Testing Tools
*   **[OTel CLI](https://github.com/equinix-labs/otel-cli)** - Command-line testing
*   **[Tracegen](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/tracegen)** - Generate test traces
*   **[OTel Demo App](https://github.com/open-telemetry/opentelemetry-demo)** - Full microservices example

---

## 🎯 Instrumentation Best Practices

### When to Use Auto vs Manual

**Auto-Instrumentation:**
- ✅ Standard frameworks (Flask, Express, Gin)
- ✅ Common libraries (HTTP clients, ORMs)
- ✅ Quick prototyping
- ❌ Custom business logic
- ❌ Fine-grained control needed

**Manual Instrumentation:**
- ✅ Business-specific operations
- ✅ Custom metrics
- ✅ Internal function calls
- ✅ Queue processing logic
- ❌ Repetitive boilerplate needed

### Span Naming Conventions

```
Good:
- `HTTP GET /api/users`
- `db.query.select_users`
- `message.queue.publish`
- `cache.get`

Bad:
- `operation` (too generic)
- `function_123` (meaningless)
- `/api/users/42` (includes variable data)
```

### Attribute Guidelines

```python
# ✅ Good: Low cardinality
span.set_attribute("http.method", "GET")
span.set_attribute("db.system", "postgresql")
span.set_attribute("user.tier", "premium")

# ❌ Bad: High cardinality
span.set_attribute("user.id", "abc123")  # Too many unique values
span.set_attribute("request.body", json_data)  # Too large
```

---

## 🔧 Performance Optimization

### 1. Sampling Strategies

**Probability Sampling:**
```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

# Sample 10% of traces
sampler = TraceIdRatioBased(0.1)
```

**Parent-Based Sampling:**
```python
from opentelemetry.sdk.trace.sampling import ParentBased, ALWAYS_ON

# Always sample if parent is sampled
sampler = ParentBased(root=ALWAYS_ON)
```

**Custom Sampling:**
```python
class ErrorSampler(Sampler):
    """Always sample errors, 1% for success."""
    def should_sample(self, ...):
        if is_error(span_context):
            return Decision(SamplingDecision.RECORD_AND_SAMPLE)
        return Decision(SamplingDecision.DROP) if random() > 0.01 else Decision(SamplingDecision.RECORD_AND_SAMPLE)
```

### 2. Batch Processing

```python
from opentelemetry.sdk.trace.export import BatchSpanProcessor

processor = BatchSpanProcessor(
    exporter,
    max_queue_size=2048,          # Buffer size
    schedule_delay_millis=5000,   # Export every 5s
    max_export_batch_size=512,    # Spans per batch
)
```

### 3. Resource Detection

```python
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.resources import ProcessResourceDetector, HostResourceDetector

# Auto-detect host and process info
resource = Resource.create({
    SERVICE_NAME: "my-service",
    SERVICE_VERSION: "1.0.0"
}).merge(
    ProcessResourceDetector().detect()
).merge(
    HostResourceDetector().detect()
)
```

---

## 🐛 Debugging & Troubleshooting

### Enable Debug Logging

```bash
# Python
export OTEL_LOG_LEVEL=debug
python app.py

# Node.js  
export OTEL_LOG_LEVEL=DEBUG
node app.js

# Go
export OTEL_LOG_LEVEL=debug
./app
```

### Common Issues

**Issue: No traces appearing in backend**

```python
# Add console exporter for debugging
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

console_exporter = ConsoleSpanExporter()
provider.add_span_processor(BatchSpanProcessor(console_exporter))
```

**Issue: Context not propagating**

```python
# Verify headers are being sent
from opentelemetry.propagate import inject

headers = {}
inject(headers)
print(headers)  # Should see 'traceparent'
```

**Issue: Metrics not exported**

```python
# Force metric export immediately
from opentelemetry import metrics

meter_provider = metrics.get_meter_provider()
meter_provider.force_flush()
```

---

## 🎓 Next Steps: Preparation for Day 5

Tomorrow we'll explore industry AIOps tools. To prepare:
1. Review your Week 1 Day 1-4 implementations
2. Document what worked well and what didn't
3. Think about tool selection criteria for production

---

## 💡 Pro Tips

1. **Start Simple:** Auto-instrument first, add manual spans for business logic
2. **Follow Conventions:** Use semantic conventions for interoperability
3. **Test Locally:** Use console exporters before connecting to backends
4. **Monitor Overhead:** OTel adds ~1-5% latency, measure it
5. **Version Your Schema:** Track instrumentation changes like code changes

---

<p align="center">
  <a href="../lecture-notes.md">Back to Lecture Notes</a>
</p>
