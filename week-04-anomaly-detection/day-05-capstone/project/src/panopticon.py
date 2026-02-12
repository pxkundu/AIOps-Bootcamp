# The Panopticon: Unified AIOps Platform

import pandas as pd
import numpy as np
from models import PointDetector, TrendDetector
from utils import create_event_features

class Panopticon:
    def __init__(self):
        # 1. Point Detector (IsolationForest)
        self.point_model = PointDetector(contamination=0.01)
        
        # 2. Trend Detector (Z-Score)
        self.trend_model = TrendDetector(threshold=3.0)
        
        # State
        self.variance_buffer = [] 
        self.variance_threshold = 0.001
        
    def train(self, history_df):
        print("\n--- Training Panopticon ---")
        
        # Feature Engineering: CPU, Fan, Hour
        history_df['hour'] = history_df['timestamp'].dt.hour
        
        # Train Point Model (Multi-variate)
        X_train = history_df[['cpu', 'fan_speed', 'hour']]
        print(f"Training Point Detector on {len(X_train)} samples...")
        self.point_model.train(X_train)
        
        # Train Trend Model (Uni-variate CPU)
        print("Training Trend Detector on CPU...")
        self.trend_model.train(history_df['cpu'])
        
        print("--- System Armed ---\n")

    def detect(self, event):
        """
        Main Detection Logic.
        Input: {'timestamp', 'cpu', 'fan_speed'}
        Output: Alert String or None
        """
        alerts = []
        
        # 1. Prepare Features
        hour = event['timestamp'].hour
        # Features must match training order: [cpu, fan, hour]
        # predict() expects DataFrame or 2D array
        features = pd.DataFrame([{
            'cpu': event['cpu'],
            'fan_speed': event['fan_speed'],
            'hour': hour
        }])
        
        # 2. Check Point Model
        # Returns -1 for anomaly
        is_point_anomaly = self.point_model.predict(features)[0] == -1
        
        if is_point_anomaly:
            if event['cpu'] == 0:
                alerts.append("Flash Crash (CPU=0)")
            elif hour == 3 and event['cpu'] > 60:
                alerts.append("Night Raid (High CPU at 3 AM)")
            elif event['fan_speed'] < 1000 and event['cpu'] > 80:
                alerts.append("Cooldown (Inverse Correlation)")
            else:
                alerts.append("Unknown Point Anomaly")
                
        # 3. Check Trend Model
        is_trend_anomaly = self.trend_model.predict(event['cpu'])
        if is_trend_anomaly:
            alerts.append(f"Trend Breach (CPU={event['cpu']:.1f})")
            
        # 4. Check Pattern (Zero Variance)
        self.variance_buffer.append(event['cpu'])
        if len(self.variance_buffer) > 5:
            self.variance_buffer.pop(0)

        if len(self.variance_buffer) == 5:
            variance = np.var(self.variance_buffer)
            if variance < self.variance_threshold and event['cpu'] > 1:
                alerts.append("Heart Attack (Zero Variance)")

        if alerts:
            # Deduplicate
            return " + ".join(list(set(alerts)))
        
        return None
