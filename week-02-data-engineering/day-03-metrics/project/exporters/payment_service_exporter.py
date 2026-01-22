#!/usr/bin/env python3
"""
Payment Service Prometheus Exporter
Exposes metrics for the ShopFast Payment Service
"""

from prometheus_client import Counter, Histogram, start_http_server
import time
import random
from threading import Thread

# Define metrics
payments_total = Counter(
    'shopfast_payments_total',
    'Total payments processed',
    ['status', 'gateway']
)

payment_amount_total = Counter(
    'shopfast_payment_amount_total',
    'Total payment amounts in USD',
    ['gateway']
)

payment_failures_total = Counter(
    'shopfast_payment_failures_total',
    'Total payment failures',
    ['gateway', 'failure_reason']
)

payment_gateway_latency = Histogram(
    'shopfast_payment_gateway_latency_seconds',
    'Payment gateway response time',
    ['gateway'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Simulate payment processing
def simulate_payment_processing():
    """Simulate payment transactions"""
    statuses = ['success', 'failed', 'pending', 'refunded']
    gateways = ['stripe', 'paypal', 'square', 'adyen']
    failure_reasons = ['insufficient_funds', 'card_declined', 'network_error', 'timeout']
    
    while True:
        gateway = random.choice(gateways)
        status = random.choice(statuses)
        
        # Update payment counter
        payments_total.labels(status=status, gateway=gateway).inc()
        
        # Simulate payment amount (between $5 and $1000)
        if status == 'success':
            payment_amount = random.uniform(5.0, 1000.0)
            payment_amount_total.labels(gateway=gateway).inc(payment_amount)
        
        # Simulate gateway latency
        if gateway == 'stripe':
            latency = random.uniform(0.1, 0.5)  # Fast
        elif gateway == 'paypal':
            latency = random.uniform(0.3, 1.0)  # Medium
        else:
            latency = random.uniform(0.5, 2.0)  # Slower
        
        payment_gateway_latency.labels(gateway=gateway).observe(latency)
        
        # Simulate failures (5% failure rate)
        if status == 'failed':
            reason = random.choice(failure_reasons)
            payment_failures_total.labels(gateway=gateway, failure_reason=reason).inc()
        
        # Sleep to simulate payment rate (2-10 payments/sec)
        time.sleep(random.uniform(0.1, 0.5))

if __name__ == '__main__':
    start_http_server(8004)
    print("Payment Service Exporter started on port 8004")
    print("Metrics available at http://localhost:8004/metrics")
    
    payment_thread = Thread(target=simulate_payment_processing, daemon=True)
    payment_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down exporter...")
