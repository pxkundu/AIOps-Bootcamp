import pandas as pd
import numpy as np

def engineer_features(df):
    """
    Transforms raw metrics into AIOps features.
    
    Input: DataFrame with ['timestamp', 'cpu', 'fan_speed']
    Output: DataFrame with ['cpu', 'fan_speed', 'hour', 'cpu_diff']
    """
    df = df.copy()
    
    # 1. Time Features (Context)
    # Convert 'timestamp' to hour of day (0-23)
    df['hour'] = df['timestamp'].dt.hour
    
    # 2. Lag Features (Trend)
    # Calculate difference from previous minute
    # Fill NaN with 0 for the first row
    # Use fillna(0) for simplicity in demo
    df['cpu_diff'] = df['cpu'].diff().fillna(0)
    
    return df

def create_event_features(event):
    """
    Transforms a single live event dict into a feature list.
    Matching the training set order.
    """
    hour = event['timestamp'].hour
    cpu = event['cpu']
    fan = event['fan_speed']
    
    # Note: 'cpu_diff' is hard for single event unless we track state.
    # For this demo, we'll keep it simple and omit 'diff' from the live detector
    # Or simulate it if we had state.
    # Let's stick to [cpu, fan, hour] for the Point Model.
    
    return [[cpu, fan, hour]]
