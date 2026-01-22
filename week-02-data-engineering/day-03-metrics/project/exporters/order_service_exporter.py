#!/usr/bin/env python3
"""
Order Service Prometheus Exporter
Exposes metrics for the ShopFast Order Service
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import random
from threading import Thread

# Define metrics
orders_total = Counter(
    'shopfast_orders_total',
    'Total orders placed',
    ['status', 'payment_method']
)

order_value_total = Counter(
    'shopfast_order_value_total',
    'Total order value in USD',
    ['product_category']
)

order_processing_duration = Histogram(
    'shopfast_order_processing_duration_seconds',
    'Time to process an order',
    ['status'],
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

cart_abandonments_total = Counter(
    'shopfast_cart_abandonments_total',
    'Total cart abandonments',
    ['reason']
)

# Simulate order processing
def simulate_order_processing():
    """Simulate order creation and processing"""
    statuses = ['pending', 'processing', 'completed', 'failed', 'cancelled']
    payment_methods = ['credit_card', 'debit_card', 'paypal', 'apple_pay', 'google_pay']
    product_categories = ['electronics', 'clothing', 'books', 'food', 'home', 'sports']
    abandonment_reasons = ['price_too_high', 'shipping_cost', 'checkout_complexity', 'payment_issue']
    
    while True:
        # Simulate order creation
        status = random.choice(statuses)
        payment_method = random.choice(payment_methods)
        category = random.choice(product_categories)
        
        # Update order counter
        orders_total.labels(status=status, payment_method=payment_method).inc()
        
        # Simulate order value (between $10 and $500)
        order_value = random.uniform(10.0, 500.0)
        order_value_total.labels(product_category=category).inc(order_value)
        
        # Simulate processing time
        if status == 'completed':
            processing_time = random.uniform(0.5, 2.0)
        elif status == 'failed':
            processing_time = random.uniform(1.0, 5.0)
        else:
            processing_time = random.uniform(0.1, 1.0)
        
        order_processing_duration.labels(status=status).observe(processing_time)
        
        # Simulate cart abandonment (10% of interactions)
        if random.random() < 0.1:
            reason = random.choice(abandonment_reasons)
            cart_abandonments_total.labels(reason=reason).inc()
        
        # Sleep to simulate order rate (5-20 orders/sec)
        time.sleep(random.uniform(0.05, 0.2))

if __name__ == '__main__':
    # Start HTTP server on port 8003
    start_http_server(8003)
    print("Order Service Exporter started on port 8003")
    print("Metrics available at http://localhost:8003/metrics")
    
    # Start order simulation in background
    order_thread = Thread(target=simulate_order_processing, daemon=True)
    order_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down exporter...")
