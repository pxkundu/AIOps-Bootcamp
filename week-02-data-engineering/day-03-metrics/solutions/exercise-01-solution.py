#!/usr/bin/env python3
"""
Solution for Exercise 1: Custom Prometheus Exporter
E-commerce API exporter with multi-process support
"""

from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server
from prometheus_client import multiprocess, CollectorRegistry, generate_latest
from flask import Flask, Response
import time
import random
import os

# Set multiprocess directory
os.environ['PROMETHEUS_MULTIPROC_DIR'] = '/tmp/prometheus_multiproc_dir'
os.makedirs(os.environ['PROMETHEUS_MULTIPROC_DIR'], exist_ok=True)

# Create multiprocess registry
registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

# Define metrics with registry
orders_total = Counter(
    'ecommerce_orders_total',
    'Total orders placed',
    ['product_category', 'status'],
    registry=registry
)

active_carts = Gauge(
    'ecommerce_active_carts',
    'Currently active shopping carts',
    registry=registry
)

order_duration = Histogram(
    'ecommerce_order_duration_seconds',
    'Time to process an order',
    ['product_category'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
    registry=registry
)

revenue_total = Counter(
    'ecommerce_revenue_total',
    'Total revenue in USD',
    ['product_category'],
    registry=registry
)

# Optional: Summary metric for order values
order_value_summary = Summary(
    'ecommerce_order_value_seconds',
    'Order value distribution',
    ['product_category'],
    registry=registry
)

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    """Expose metrics endpoint"""
    return Response(generate_latest(registry), mimetype='text/plain')

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy'}, 200

def simulate_orders():
    """Simulate order events"""
    categories = ['electronics', 'clothing', 'books', 'food']
    statuses = ['completed', 'pending', 'failed']
    
    while True:
        # Random order
        category = random.choice(categories)
        status = random.choice(statuses)
        
        # Update order counter
        orders_total.labels(product_category=category, status=status).inc()
        
        # Update active carts (fluctuates)
        active_carts.set(random.randint(10, 100))
        
        # Simulate order processing time
        processing_time = random.uniform(0.1, 2.0)
        if status == 'failed':
            processing_time = random.uniform(1.0, 5.0)
        
        order_duration.labels(product_category=category).observe(processing_time)
        
        # Update revenue (only for completed orders)
        if status == 'completed':
            order_value = random.uniform(10.0, 500.0)
            revenue_total.labels(product_category=category).inc(order_value)
            order_value_summary.labels(product_category=category).observe(order_value)
        
        time.sleep(random.uniform(1.0, 3.0))

if __name__ == '__main__':
    import threading
    
    # Start order simulation in background
    order_thread = threading.Thread(target=simulate_orders, daemon=True)
    order_thread.start()
    
    # Start Flask app
    print("E-commerce Exporter started")
    print("Metrics available at http://localhost:8000/metrics")
    app.run(host='0.0.0.0', port=8000, debug=False)
