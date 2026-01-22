#!/usr/bin/env python3
"""
User Service Prometheus Exporter
Exposes metrics for the ShopFast User Service
"""

from prometheus_client import Counter, Gauge, Histogram, start_http_server
import time
import random
from threading import Thread

# Define metrics
user_registrations_total = Counter(
    'shopfast_user_registrations_total',
    'Total user registrations',
    ['source']
)

user_logins_total = Counter(
    'shopfast_user_logins_total',
    'Total user logins',
    ['status']
)

active_users = Gauge(
    'shopfast_active_users',
    'Currently active users'
)

login_duration = Histogram(
    'shopfast_login_duration_seconds',
    'Time to authenticate user',
    buckets=[0.1, 0.5, 1.0, 2.0]
)

# Simulate user activity
def simulate_user_activity():
    """Simulate user registrations and logins"""
    sources = ['web', 'mobile', 'api']
    login_statuses = ['success', 'failed', 'locked']
    
    while True:
        # Simulate registration
        if random.random() < 0.3:  # 30% chance
            source = random.choice(sources)
            user_registrations_total.labels(source=source).inc()
        
        # Simulate login
        status = random.choice(login_statuses)
        user_logins_total.labels(status=status).inc()
        
        # Simulate login duration
        if status == 'success':
            duration = random.uniform(0.1, 0.5)
        else:
            duration = random.uniform(0.5, 2.0)  # Failed logins take longer
        
        login_duration.observe(duration)
        
        # Update active users (fluctuates)
        active_users.set(random.randint(100, 1000))
        
        # Sleep to simulate activity rate
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == '__main__':
    start_http_server(8002)
    print("User Service Exporter started on port 8002")
    print("Metrics available at http://localhost:8002/metrics")
    
    user_thread = Thread(target=simulate_user_activity, daemon=True)
    user_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down exporter...")
