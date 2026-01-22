# Exercise 1: Building a Custom Prometheus Exporter

> **Duration:** 2 hours | **Difficulty:** Intermediate
> **Objective:** Create a Prometheus exporter for a Python web application that tracks business metrics.

---

## 🎯 Learning Goals

By completing this exercise, you will:
1. Understand how to expose metrics in Prometheus format.
2. Implement different metric types (Counter, Gauge, Histogram).
3. Handle multi-process scenarios (Gunicorn workers).
4. Test and validate your exporter.

---

## 📋 Scenario

You're building a **E-commerce API** and need to track:
- Total orders placed (Counter)
- Current active shopping carts (Gauge)
- Order processing time (Histogram)
- Revenue per product category (Counter with labels)

---

## 🛠️ Requirements

### Part 1: Basic Exporter (30 minutes)

Create a file `exporter.py` that:

1. **Exposes a `/metrics` endpoint** using `prometheus_client`.
2. **Defines the following metrics:**
   ```python
   # Counter: Total orders
   orders_total = Counter('ecommerce_orders_total', 
                          'Total orders placed', 
                          ['product_category', 'status'])
   
   # Gauge: Active carts
   active_carts = Gauge('ecommerce_active_carts', 
                        'Currently active shopping carts')
   
   # Histogram: Order processing time
   order_duration = Histogram('ecommerce_order_duration_seconds',
                              'Time to process an order',
                              ['product_category'])
   
   # Counter: Revenue
   revenue_total = Counter('ecommerce_revenue_total',
                           'Total revenue in USD',
                           ['product_category'])
   ```

3. **Simulates order events** in a loop:
   - Every 2 seconds, create a random order
   - Update all metrics accordingly
   - Use random categories: `['electronics', 'clothing', 'books', 'food']`
   - Use random statuses: `['completed', 'pending', 'failed']`
   - Simulate processing time: 0.1 to 2.0 seconds

### Part 2: Multi-Process Support (30 minutes)

Modify `exporter.py` to work with **Gunicorn** (multiple worker processes):

1. **Install dependencies:**
   ```bash
   pip install prometheus-client gunicorn
   ```

2. **Use multiprocess mode:**
   ```python
   from prometheus_client import multiprocess, CollectorRegistry
   from prometheus_client import generate_latest, Counter, Gauge, Histogram
   from flask import Flask, Response
   
   app = Flask(__name__)
   
   # Create multiprocess registry
   registry = CollectorRegistry()
   multiprocess.MultiProcessCollector(registry)
   
   # Define metrics with registry
   orders_total = Counter('ecommerce_orders_total', 
                          'Total orders placed',
                          ['product_category', 'status'],
                          registry=registry)
   # ... other metrics
   
   @app.route('/metrics')
   def metrics():
       return Response(generate_latest(registry), 
                      mimetype='text/plain')
   ```

3. **Create a Gunicorn config file** `gunicorn_config.py`:
   ```python
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "sync"
   ```

4. **Run with Gunicorn:**
   ```bash
   gunicorn -c gunicorn_config.py exporter:app
   ```

### Part 3: Testing & Validation (30 minutes)

1. **Start your exporter:**
   ```bash
   python exporter.py  # or gunicorn -c gunicorn_config.py exporter:app
   ```

2. **Verify metrics endpoint:**
   ```bash
   curl http://localhost:8000/metrics
   ```

3. **Check specific metrics:**
   ```bash
   curl http://localhost:8000/metrics | grep ecommerce
   ```

4. **Expected output format:**
   ```
   # HELP ecommerce_orders_total Total orders placed
   # TYPE ecommerce_orders_total counter
   ecommerce_orders_total{product_category="electronics",status="completed"} 5.0
   ecommerce_orders_total{product_category="clothing",status="pending"} 2.0
   
   # HELP ecommerce_active_carts Currently active shopping carts
   # TYPE ecommerce_active_carts gauge
   ecommerce_active_carts 12.0
   
   # HELP ecommerce_order_duration_seconds Time to process an order
   # TYPE ecommerce_order_duration_seconds histogram
   ecommerce_order_duration_seconds_bucket{product_category="electronics",le="0.5"} 3.0
   ecommerce_order_duration_seconds_bucket{product_category="electronics",le="1.0"} 5.0
   ecommerce_order_duration_seconds_bucket{product_category="electronics",le="+Inf"} 5.0
   ecommerce_order_duration_seconds_sum{product_category="electronics"} 2.5
   ecommerce_order_duration_seconds_count{product_category="electronics"} 5.0
   ```

### Part 4: Integration with Prometheus (30 minutes)

1. **Create `prometheus.yml`:**
   ```yaml
   global:
     scrape_interval: 10s
   
   scrape_configs:
     - job_name: 'ecommerce-exporter'
       static_configs:
         - targets: ['localhost:8000']
   ```

2. **Run Prometheus:**
   ```bash
   docker run -p 9090:9090 \
     -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
     prom/prometheus:latest
   ```

3. **Verify in Prometheus UI:**
   - Open http://localhost:9090
   - Go to Status → Targets
   - Verify your exporter is "UP"
   - Query: `ecommerce_orders_total`

---

## ✅ Success Criteria

- [ ] Exporter exposes `/metrics` endpoint
- [ ] All 4 metric types are implemented correctly
- [ ] Metrics follow Prometheus naming conventions
- [ ] Multi-process mode works with Gunicorn
- [ ] Prometheus can scrape the exporter successfully
- [ ] Metrics appear in Prometheus query interface

---

## 🎓 Bonus Challenges

1. **Add a Summary metric** for order value distribution.
2. **Implement metric relabeling** to drop low-value categories.
3. **Add authentication** to the `/metrics` endpoint (basic auth).
4. **Create a Grafana dashboard** visualizing your metrics.

---

## 📚 Resources

- [Prometheus Client Library (Python)](https://github.com/prometheus/client_python)
- [Writing Exporters Guide](https://prometheus.io/docs/instrumenting/writing_exporters/)
- [Multi-Process Mode](https://github.com/prometheus/client_python#multiprocess-mode-gunicorn)

---

## 💡 Hints

- Use `random.choice()` for random category/status selection
- Use `time.time()` to measure duration for Histogram
- For multiprocess, set `PROMETHEUS_MULTIPROC_DIR` environment variable
- Test with `curl` before integrating with Prometheus

---

<p align="center">
  <a href="../lecture-notes.md">← Back to Lecture Notes</a> | 
  <a href="exercise-02-aggregation.md">Next Exercise →</a>
</p>
