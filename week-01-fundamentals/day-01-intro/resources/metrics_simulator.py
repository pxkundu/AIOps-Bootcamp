#!/usr/bin/env python3
"""
Simple script to generate a CSV dataset of metrics for Day 1 theory exercises.
Simulates a web server CPU usage pattern with seasonality and random spikes.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_dataset(days=7, output_file="seasonal_metrics.csv"):
    start_time = datetime.now() - timedelta(days=days)
    data = []
    
    # Generate data every 1 minute
    for i in range(days * 24 * 60):
        current_time = start_time + timedelta(minutes=i)
        
        # Seasonality: higher usage during business hours (9-17)
        hour = current_time.hour
        if 9 <= hour <= 17:
            base_load = 60 + np.sin(current_time.minute / 60 * np.pi) * 10
        else:
            base_load = 20 + np.random.normal(0, 5)
            
        # Add random noise
        noise = np.random.normal(0, 2)
        
        # Add occasional spikes (anomalies)
        spike = 0
        if np.random.random() < 0.005:  # 0.5% chance per minute
            spike = 35
            
        cpu_usage = min(max(base_load + noise + spike, 0), 100)
        
        data.append({
            "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_usage_pct": round(cpu_usage, 2),
            "mem_usage_pct": round(max(30 + cpu_usage * 0.2 + np.random.normal(0, 1), 0), 2)
        })
        
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"✅ Generated {len(df)} data points in {output_file}")

if __name__ == "__main__":
    generate_dataset()
