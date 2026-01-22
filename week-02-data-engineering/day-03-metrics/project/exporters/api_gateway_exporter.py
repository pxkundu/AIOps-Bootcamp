#!/usr/bin/env python3
"""
API Gateway Prometheus Exporter
Exposes metrics for the ShopFast API Gateway service
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import random
from threading import Thread

# Define metrics
api_requests_total = Counter(
    'shopfast_api_requests_total',
    'Total API requests',
    ['method', 'status', 'endpoint']
)

api_request_duration = Histogram(
    'shopfast_api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

api_active_connections = Gauge(
    'shopfast_api_active_connections',
    'Current active connections'
)

api_cache_hits_total = Counter(
    'shopfast_api_cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

# Simulate API traffic
def simulate_api_traffic():
    """Simulate realistic API traffic patterns"""
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    endpoints = ['/api/products', '/api/users', '/api/orders', '/api/cart', '/api/checkout']
    status_codes = ['200', '201', '400', '401', '404', '500']
    cache_types = ['redis', 'memcached', 'cdn']
    
    while True:
        # Simulate request
        method = random.choice(methods)
        endpoint = random.choice(endpoints)
        status = random.choice(status_codes)
        
        # Update request counter
        api_requests_total.labels(method=method, status=status, endpoint=endpoint).inc()
        
        # Simulate request duration
        duration = random.uniform(0.05, 2.0)
        if status == '500':
            duration = random.uniform(1.0, 5.0)  # Errors take longer
        
        api_request_duration.labels(method=method, endpoint=endpoint).observe(duration)
        
        # Update active connections (fluctuates)
        connections = random.randint(50, 500)
        api_active_connections.set(connections)
        
        # Simulate cache hits (70% hit rate)
        if random.random() < 0.7:
            cache_type = random.choice(cache_types)
            api_cache_hits_total.labels(cache_type=cache_type).inc()
        
        # Sleep to simulate request rate (10-100 req/sec)
        time.sleep(random.uniform(0.01, 0.1))

if __name__ == '__main__':
    # Start HTTP server on port 8001
    start_http_server(8001)
    print("API Gateway Exporter started on port 8001")
    print("Metrics available at http://localhost:8001/metrics")
    
    # Start traffic simulation in background
    traffic_thread = Thread(target=simulate_api_traffic, daemon=True)
    traffic_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down exporter...")
