# Solution for "The Signal Hunter" Game
# Week 4 Day 3 Gamification

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def solve_level_1_spy(data):
    """
    Level 1: Point Anomaly (Huge Outlier).
    Tool: Isolation Forest (Raw).
    """
    print("🛡️ Guardian Level 1: The Spy")
    # Reshape for sklearn
    X = data.values.reshape(-1, 1)
    
    # Contamination=0.01 (Expect 1 outlier)
    clf = IsolationForest(contamination=0.01, random_state=42)
    # Return -1 for anomaly
    return clf.fit_predict(X)

def solve_level_2_sleeper(df):
    """
    Level 2: Contextual Anomaly (Normal value, Wrong time with 'hour').
    Tool: Isolation Forest (Contextual Features).
    """
    print("🛡️ Guardian Level 2: The Sleeper")
    # Use both 'value' and 'hour' as features
    X = df[['value', 'hour']]
    
    clf = IsolationForest(contamination=0.01, random_state=42)
    return clf.fit_predict(X)

def solve_level_3_swarm(data):
    """
    Level 3: Density Anomaly (Cluster is tight, outliers are loose).
    Tool: Local Outlier Factor.
    """
    print("🛡️ Guardian Level 3: The Swarm")
    X = data.values.reshape(-1, 1)
    
    # Use LOF to find points in low-density regions
    clf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
    return clf.fit_predict(X)

# Mock Runner
if __name__ == "__main__":
    # Test Level 1
    d1 = pd.Series([10, 10, 10, 1000, 10, 10]) # 1000 is Spy
    pred1 = solve_level_1_spy(d1)
    print(f"Level 1 Predictions: {pred1}")
    
    # Test Level 2
    # 3 AM = 10, 12 PM = 100.
    # At 3 AM, value is 100 (Sleeper).
    d2 = pd.DataFrame({
        'value': [10, 100, 10, 100, 100], # Index 4 is 3AM but 100
        'hour':  [3,  12,  3,  12,  3]
    })
    pred2 = solve_level_2_sleeper(d2)
    print(f"Level 2 Predictions: {pred2}")
    
    print("\n🏆 MISSION ACCOMPLISHED. SYSTEM SECURE.")
