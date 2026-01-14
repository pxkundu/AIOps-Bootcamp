# Exercise 2: Manual Instrumentation & Custom Spans

## 🎯 Objective
Learn to manually instrument code with custom spans, metrics, and events for business logic visibility.

---

##🛠️ Part 1: Custom Span Creation

### Task: Instrument an E-Commerce Checkout Flow

**File: `checkout_service.py`**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import time
import random

# Setup tracing
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

def checkout(cart_items, user_id):
    """Complete checkout process with detailed instrumentation."""
    with tracer.start_as_current_span("checkout") as span:
        span.set_attribute("user.id", user_id)
        span.set_attribute("cart.item_count", len(cart_items))
        span.set_attribute("cart.total_value", sum(item['price'] for item in cart_items))
        
        # Step 1: Validate cart
        validate_cart(cart_items)
        
        # Step 2: Process payment
        payment_success = process_payment(user_id, cart_items)
        
        if not payment_success:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "Payment failed"))
            return {"status": "failed"}
        
        # Step 3: Update inventory
        update_inventory(cart_items)
        
        # Step 4: Send confirmation
        send_confirmation(user_id)
        
        span.add_event("Checkout completed successfully")
        return {"status": "success"}

def validate_cart(cart_items):
    with tracer.start_as_current_span("validate_cart") as span:
        time.sleep(0.01)  # Simulate validation
        span.set_attribute("validation.rules_checked", 5)

def process_payment(user_id, cart_items):
    with tracer.start_as_current_span("process_payment") as span:
        total = sum(item['price'] for item in cart_items)
        span.set_attribute("payment.amount", total)
        span.set_attribute("payment.currency", "USD")
        
        # Simulate payment gateway call
        time.sleep(random.uniform(0.05, 0.2))
        
        # 10% failure rate
        if random.random() < 0.1:
            span.add_event("Payment declined")
            span.set_attribute("payment.status", "declined")
            return False
        
        span.add_event("Payment approved")
        span.set_attribute("payment.status", "approved")
        return True

def update_inventory(cart_items):
    with tracer.start_as_current_span("update_inventory") as span:
        span.set_attribute("inventory.items_updated", len(cart_items))
        time.sleep(0.03)

def send_confirmation(user_id):
    with tracer.start_as_current_span("send_confirmation") as span:
        span.set_attribute("notification.channel", "email")
        time.sleep(0.02)

# Test it
if __name__ == "__main__":
    cart = [
        {"name": "Widget", "price": 29.99},
        {"name": "Gadget", "price": 49.99}
    ]
    
    for i in range(10):
        result = checkout(cart, user_id=f"user-{i}")
        print(f"Checkout {i}: {result}")
        time.sleep(1)
```

### Run and Observe
```bash
python checkout_service.py
```

**Jaeger Analysis Questions:**
1. How many spans are in a successful checkout trace?
2. Which operation takes the longest?
3. How do failed payments appear in traces?

---

## 📊 Part 2: Custom Metrics

### Task: Add Business Metrics

**Add to `checkout_service.py`:**
```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# Setup metrics
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Business metrics
checkouts_total = meter.create_counter(
    "checkouts_total",
    description="Total checkout attempts"
)

checkout_value = meter.create_histogram(
    "checkout_value_usd",
    description="Checkout cart value in USD"
)

payment_failures = meter.create_counter(
    "payment_failures_total",
    description="Failed payment attempts"
)

# Start Prometheus server
start_http_server(8000)

# Update checkout function
def checkout(cart_items, user_id):
    with tracer.start_as_current_span("checkout") as span:
        total_value = sum(item['price'] for item in cart_items)
        
        # Record metrics
        checkouts_total.add(1, {"user_tier": "standard"})
        checkout_value.record(total_value)
        
        # ... rest of code ...
        
        if not payment_success:
            payment_failures.add(1, {"reason": "declined"})
```

**Query Your Metrics:**
```promql
# Total checkouts
checkouts_total

# Average cart value
histogram_quantile(0.5, checkout_value_usd_bucket)

# Payment failure rate
rate(payment_failures_total[5m]) / rate(checkouts_total[5m])
```

---

## 🎯 Part 3: Span Events & Exception Handling

### Task: Add Detailed Events

```python
def process_payment_detailed(user_id, cart_items):
    with tracer.start_as_current_span("process_payment") as span:
        try:
            span.add_event("Calling payment gateway")
            
            # Simulate API call
            time.sleep(0.1)
            
            if random.random() < 0.05:
                raise Exception("Network timeout")
            
            span.add_event("Payment response received", {
                "response.code": "200",
                "transaction.id": f"txn-{random.randint(1000, 9999)}"
            })
            
            return True
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            span.add_event("Payment failed", {
                "error.type": type(e).__name__,
                "error.message": str(e)
            })
            raise
```

**Observe:** How do exceptions appear in Jaeger?

---

## ✅ Deliverables

Create `exercise-02-report.md` with:
1. **Span Hierarchy:** Diagram showing parent-child spans in checkout
2. **Custom Attributes:** List of all custom attributes you added
3. **Business Metrics:** 3 PromQL queries using your custom metrics
4. **Performance Insights:** Which step is the bottleneck? Evidence from traces.

---

## 💡 Challenges

1. **Add Caching:** Instrument a cache layer (Redis) with custom spans
2. **Retry Logic:** Add spans showing retry attempts on payment failures
3. **A/B Testing:** Use span attributes to track different checkout flows
4. **SLO Tracking:** Create metrics to track if checkout completes in <500ms
