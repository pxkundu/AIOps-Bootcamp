#!/usr/bin/env python3
"""
Real-Time Anomaly Detection Pipeline
Consumes metrics from Kafka and detects anomalies
"""

from kafka import KafkaConsumer, KafkaProducer
import json
import time
from collections import defaultdict, deque
import numpy as np
from datetime import datetime
import requests
import joblib
from sklearn.ensemble import IsolationForest

class MetricWindow:
    """Rolling window for metric values"""
    
    def __init__(self, window_size=300):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)
        self.timestamps = deque(maxlen=window_size)
    
    def add(self, timestamp, value):
        """Add a new value to the window"""
        self.values.append(value)
        self.timestamps.append(timestamp)
    
    def mean(self):
        """Calculate mean of window values"""
        return np.mean(self.values) if self.values else 0.0
    
    def std(self):
        """Calculate standard deviation"""
        if len(self.values) < 2:
            return 0.0
        return np.std(self.values)
    
    def z_score(self, value):
        """Calculate z-score for a value"""
        mean = self.mean()
        std = self.std()
        if std == 0:
            return 0.0
        return (value - mean) / std
    
    def compute_features(self):
        """Extract features for ML model"""
        if len(self.values) < 10:
            return None
        
        values_array = np.array(self.values)
        return np.array([
            values_array[-1],           # Current value
            self.mean(),               # Rolling mean
            self.std(),                # Rolling std
            self.z_score(values_array[-1]),  # Z-score
            len(self.values),          # Window size
            np.min(values_array),      # Min
            np.max(values_array),      # Max
            np.median(values_array),   # Median
        ])

class AnomalyDetector:
    """Detects anomalies using multiple methods"""
    
    def __init__(self, model_path=None):
        self.windows = defaultdict(lambda: MetricWindow(window_size=300))
        self.model = None
        
        if model_path:
            try:
                self.model = joblib.load(model_path)
                print(f"Loaded ML model from {model_path}")
            except FileNotFoundError:
                print(f"Model file not found: {model_path}. Using statistical detection only.")
    
    def detect_statistical(self, metric_name, value, window):
        """Detect anomalies using z-score (3-sigma rule)"""
        z_score = abs(window.z_score(value))
        
        if z_score > 3:
            severity = 'high' if z_score > 4 else 'medium'
            return {
                'method': 'statistical',
                'z_score': z_score,
                'severity': severity,
                'expected_value': window.mean(),
                'actual_value': value
            }
        return None
    
    def detect_ml(self, metric_name, value, window):
        """Detect anomalies using ML model"""
        if self.model is None:
            return None
        
        features = window.compute_features()
        if features is None:
            return None
        
        prediction = self.model.predict(features.reshape(1, -1))[0]
        
        if prediction == -1:  # Anomaly
            return {
                'method': 'ml',
                'severity': 'high',
                'actual_value': value,
                'expected_value': window.mean()
            }
        return None
    
    def detect_threshold(self, metric_name, value, window):
        """Detect anomalies using threshold (2x mean)"""
        mean = window.mean()
        if mean == 0:
            return None
        
        if value > 2 * mean or value < 0.5 * mean:
            return {
                'method': 'threshold',
                'severity': 'medium',
                'actual_value': value,
                'expected_value': mean,
                'ratio': value / mean if mean > 0 else 0
            }
        return None
    
    def detect(self, metric_name, value, timestamp):
        """Detect anomalies using all methods"""
        window = self.windows[metric_name]
        window.add(timestamp, value)
        
        # Try all detection methods
        anomalies = []
        
        # Statistical detection
        stat_anomaly = self.detect_statistical(metric_name, value, window)
        if stat_anomaly:
            anomalies.append(stat_anomaly)
        
        # ML detection
        ml_anomaly = self.detect_ml(metric_name, value, window)
        if ml_anomaly:
            anomalies.append(ml_anomaly)
        
        # Threshold detection
        threshold_anomaly = self.detect_threshold(metric_name, value, window)
        if threshold_anomaly:
            anomalies.append(threshold_anomaly)
        
        if anomalies:
            # Return the most severe anomaly
            return {
                'metric_name': metric_name,
                'value': value,
                'timestamp': timestamp,
                'detections': anomalies,
                'severity': max(a.get('severity', 'low') for a in anomalies)
            }
        
        return None

class AnomalyPipeline:
    """Main pipeline for anomaly detection"""
    
    def __init__(self, kafka_broker='localhost:9092', model_path=None):
        self.consumer = KafkaConsumer(
            'prometheus-metrics',
            bootstrap_servers=kafka_broker,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self.detector = AnomalyDetector(model_path=model_path)
        self.alertmanager_url = 'http://localhost:9093/api/v1/alerts'
    
    def process_metric(self, message):
        """Process a single metric message"""
        try:
            metric_data = message.value
            metric_name = metric_data.get('metric', {}).get('__name__', 'unknown')
            value = float(metric_data.get('value', 0))
            timestamp = metric_data.get('timestamp', time.time())
            
            # Detect anomalies
            anomaly = self.detector.detect(metric_name, value, timestamp)
            
            if anomaly:
                print(f"🚨 Anomaly detected: {metric_name} = {value}")
                print(f"   Severity: {anomaly['severity']}")
                print(f"   Methods: {[d['method'] for d in anomaly['detections']]}")
                
                # Publish to Kafka
                self.producer.send('anomaly-alerts', anomaly)
                
                # Send to Alertmanager
                self.send_alert(anomaly)
        
        except Exception as e:
            print(f"Error processing metric: {e}")
    
    def send_alert(self, anomaly):
        """Send alert to Prometheus Alertmanager"""
        alert = {
            'labels': {
                'alertname': 'MetricAnomaly',
                'metric': anomaly['metric_name'],
                'severity': anomaly['severity']
            },
            'annotations': {
                'summary': f"Anomaly detected in {anomaly['metric_name']}",
                'description': f"Value: {anomaly['value']:.2f}, Expected: {anomaly['detections'][0].get('expected_value', 'N/A'):.2f}"
            },
            'startsAt': datetime.utcnow().isoformat() + 'Z'
        }
        
        try:
            response = requests.post(self.alertmanager_url, json=[alert], timeout=5)
            if response.status_code == 200:
                print(f"✓ Alert sent to Alertmanager")
            else:
                print(f"✗ Failed to send alert: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Error sending alert: {e}")
    
    def run(self):
        """Run the anomaly detection pipeline"""
        print("Starting anomaly detection pipeline...")
        print("Consuming from: prometheus-metrics")
        print("Publishing to: anomaly-alerts")
        
        try:
            for message in self.consumer:
                self.process_metric(message)
        except KeyboardInterrupt:
            print("\nShutting down pipeline...")
        finally:
            self.consumer.close()
            self.producer.close()

if __name__ == '__main__':
    import sys
    
    model_path = sys.argv[1] if len(sys.argv) > 1 else None
    pipeline = AnomalyPipeline(model_path=model_path)
    pipeline.run()
