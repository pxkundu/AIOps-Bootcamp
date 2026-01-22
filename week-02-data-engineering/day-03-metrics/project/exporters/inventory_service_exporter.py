#!/usr/bin/env python3
"""
Inventory Service Prometheus Exporter
Exposes metrics for the ShopFast Inventory Service
"""

from prometheus_client import Counter, Gauge, Histogram, start_http_server
import time
import random
from threading import Thread

# Define metrics
inventory_updates_total = Counter(
    'shopfast_inventory_updates_total',
    'Total inventory updates',
    ['operation', 'product_category']
)

stock_level = Gauge(
    'shopfast_stock_level',
    'Current stock level',
    ['product_id', 'warehouse']
)

inventory_check_duration = Histogram(
    'shopfast_inventory_check_duration_seconds',
    'Time to check inventory',
    buckets=[0.1, 0.5, 1.0, 2.0]
)

low_stock_alerts = Counter(
    'shopfast_low_stock_alerts_total',
    'Total low stock alerts',
    ['product_category']
)

# Simulate inventory operations
def simulate_inventory_operations():
    """Simulate inventory management operations"""
    operations = ['add', 'remove', 'reserve', 'release']
    categories = ['electronics', 'clothing', 'books', 'food']
    warehouses = ['warehouse-east', 'warehouse-west', 'warehouse-central']
    
    # Initialize some stock levels
    products = {}
    for i in range(10):
        products[f'product_{i}'] = {
            'warehouse': random.choice(warehouses),
            'stock': random.randint(50, 500)
        }
    
    while True:
        # Simulate inventory update
        operation = random.choice(operations)
        category = random.choice(categories)
        inventory_updates_total.labels(operation=operation, product_category=category).inc()
        
        # Update stock level for a random product
        if random.random() < 0.5:
            product_id = random.choice(list(products.keys()))
            product = products[product_id]
            
            if operation == 'add':
                product['stock'] += random.randint(10, 100)
            elif operation == 'remove':
                product['stock'] = max(0, product['stock'] - random.randint(5, 50))
            
            stock_level.labels(
                product_id=product_id,
                warehouse=product['warehouse']
            ).set(product['stock'])
            
            # Check for low stock
            if product['stock'] < 20:
                low_stock_alerts.labels(product_category=category).inc()
        
        # Simulate inventory check duration
        check_time = random.uniform(0.1, 1.0)
        inventory_check_duration.observe(check_time)
        
        # Sleep to simulate operation rate
        time.sleep(random.uniform(1.0, 3.0))

if __name__ == '__main__':
    start_http_server(8005)
    print("Inventory Service Exporter started on port 8005")
    print("Metrics available at http://localhost:8005/metrics")
    
    inventory_thread = Thread(target=simulate_inventory_operations, daemon=True)
    inventory_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down exporter...")
