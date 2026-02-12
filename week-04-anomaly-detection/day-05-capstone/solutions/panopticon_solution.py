# Solution for Capstone: The Panopticon Platform
# Week 4 Day 5

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

class Panopticon:
    def __init__(self):
        # 1. Point Detector (Isolation Forest)
        # Catches Flash Crash, Cooldown (correlation break), Night Raid (context)
        self.point_model = IsolationForest(contamination=0.01, random_state=42)
        
        # 2. Trend Detector (Linear Regression)
        # Catches Slow Burn
        self.trend_model = LinearRegression()
        self.trend_threshold = 0 
        
        # State Tracking (for Heart Attack / variance)
        self.recent_cpus = []
        
    def train(self, history_df):
        print("Training Panopticon Models...")
        
        # --- Feature Engineering ---
        # We assume history_df has 'timestamp', 'cpu', 'fan_speed'
        # Extract Hour for Context
        history_df['hour'] = history_df['timestamp'].dt.hour
        
        # --- Train Point Model ---
        # Features: [CPU, Fan, Hour]
        X_point = history_df[['cpu', 'fan_speed', 'hour']]
        self.point_model.fit(X_point)
        
        # --- Train Trend Model ---
        # X = Time (ordinal), y = CPU
        # Simple detection: Fit line to last 24 hours to get local trend
        # For simplicity, we just use global mean + 3 std dev as threshold here
        # Or better: Time Series logic from Day 1
        self.cpu_mean = history_df['cpu'].mean()
        self.cpu_std = history_df['cpu'].std()
        self.trend_threshold = self.cpu_mean + 3 * self.cpu_std
        
        print(f"  -> Point Model Trained.")
        print(f"  -> Trend Threshold Set: {self.trend_threshold:.2f}")

    def detect(self, event):
        """
        Ingests a live event dict: {'timestamp', 'cpu', 'fan_speed'}
        Returns Alert Object or None
        """
        alerts = []
        
        # 1. Feature Prep
        hour = event['timestamp'].hour
        features = [[event['cpu'], event['fan_speed'], hour]]
        
        # 2. Point Check (Isolation Forest)
        # Returns -1 for anomaly
        is_point_anomaly = self.point_model.predict(features)[0] == -1
        
        if is_point_anomaly:
            # Determine Why
            if event['cpu'] == 0:
                alerts.append("Flash Crash (CPU=0)")
            elif event['cpu'] > 80 and hour == 3:
                alerts.append("Night Raid (High CPU at 3 AM)")
            elif event['cpu'] > 80 and event['fan_speed'] < 1000:
                alerts.append("Cooldown (Fan Low while CPU High)")
            else:
                alerts.append("Unknown Point Anomaly")
                
        # 3. Trend Check (Z-Score / Static Threshold)
        if event['cpu'] > 94: # Hardcoded "Slow Burn" threshold for simplicity
             alerts.append("Slow Burn (Approaching 100%)")
             
        # 4. Pattern Check (Variance / Heart Attack)
        self.recent_cpus.append(event['cpu'])
        if len(self.recent_cpus) > 5:
            self.recent_cpus.pop(0)
            
        if len(self.recent_cpus) == 5:
            variance = np.var(self.recent_cpus)
            if variance < 0.001 and event['cpu'] > 0:
                # Flatline but not zero
                alerts.append("Heart Attack (Zero Variance)")

        if alerts:
            return ", ".join(alerts)
        return None
