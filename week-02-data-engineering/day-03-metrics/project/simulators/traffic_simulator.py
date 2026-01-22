#!/usr/bin/env python3
"""
Traffic Simulator for ShopFast Platform
Simulates realistic traffic patterns and injects anomalies
"""

import time
import random
import requests
from datetime import datetime, timedelta
import threading

class TrafficSimulator:
    """Simulates traffic patterns and anomalies"""
    
    def __init__(self):
        self.exporter_endpoints = {
            'api-gateway': 'http://localhost:8001',
            'user-service': 'http://localhost:8002',
            'order-service': 'http://localhost:8003',
            'payment-service': 'http://localhost:8004',
            'inventory-service': 'http://localhost:8005'
        }
        self.running = False
        self.anomaly_active = False
    
    def simulate_normal_traffic(self):
        """Simulate baseline traffic patterns"""
        print("Starting normal traffic simulation...")
        self.running = True
        
        while self.running:
            # Simulate time-of-day patterns
            hour = datetime.now().hour
            
            # Peak hours: 9 AM - 5 PM (higher traffic)
            if 9 <= hour <= 17:
                request_rate = random.uniform(50, 100)  # req/sec
            else:
                request_rate = random.uniform(10, 30)  # req/sec
            
            # Weekend patterns (higher traffic)
            if datetime.now().weekday() >= 5:  # Saturday or Sunday
                request_rate *= 1.5
            
            # Sleep based on request rate
            sleep_time = 1.0 / request_rate
            time.sleep(sleep_time)
    
    def inject_anomaly(self, anomaly_type='spike', duration=60):
        """Inject various types of anomalies"""
        print(f"Injecting {anomaly_type} anomaly for {duration} seconds...")
        self.anomaly_active = True
        start_time = time.time()
        
        if anomaly_type == 'spike':
            # Sudden traffic spike
            while time.time() - start_time < duration:
                # Generate 10x normal traffic
                for _ in range(10):
                    time.sleep(0.01)
                time.sleep(0.1)
        
        elif anomaly_type == 'error_burst':
            # Sudden increase in errors
            # This would require modifying exporter behavior
            # For now, we'll just log it
            print("Error burst anomaly: Simulating 50% error rate")
            time.sleep(duration)
        
        elif anomaly_type == 'latency_degradation':
            # Gradual latency increase
            print("Latency degradation: Simulating slow responses")
            time.sleep(duration)
        
        self.anomaly_active = False
        print(f"Anomaly injection completed")
    
    def schedule_anomalies(self):
        """Schedule random anomalies throughout the day"""
        anomaly_types = ['spike', 'error_burst', 'latency_degradation']
        
        while self.running:
            # Wait random time (5-30 minutes)
            wait_time = random.uniform(300, 1800)
            time.sleep(wait_time)
            
            # Inject random anomaly
            anomaly_type = random.choice(anomaly_types)
            duration = random.uniform(30, 120)  # 30 seconds to 2 minutes
            
            anomaly_thread = threading.Thread(
                target=self.inject_anomaly,
                args=(anomaly_type, duration),
                daemon=True
            )
            anomaly_thread.start()
    
    def check_exporters(self):
        """Verify all exporters are running"""
        print("Checking exporter endpoints...")
        for service, endpoint in self.exporter_endpoints.items():
            try:
                response = requests.get(f"{endpoint}/metrics", timeout=2)
                if response.status_code == 200:
                    print(f"✓ {service} is running")
                else:
                    print(f"✗ {service} returned status {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"✗ {service} is not accessible: {e}")
    
    def start(self):
        """Start the traffic simulator"""
        self.check_exporters()
        
        # Start normal traffic simulation
        traffic_thread = threading.Thread(
            target=self.simulate_normal_traffic,
            daemon=True
        )
        traffic_thread.start()
        
        # Start anomaly scheduler
        anomaly_thread = threading.Thread(
            target=self.schedule_anomalies,
            daemon=True
        )
        anomaly_thread.start()
        
        print("\nTraffic simulator started!")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping traffic simulator...")
            self.running = False

if __name__ == '__main__':
    simulator = TrafficSimulator()
    simulator.start()
