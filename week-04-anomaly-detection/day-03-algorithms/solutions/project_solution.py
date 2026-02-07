# Solution for Day 3 Project: The Network Guardian
# Week 4 Day 3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import classification_report, confusion_matrix

# ---------------------------------------------------------
# 1. TRAFFIC GENERATOR
# ---------------------------------------------------------
def generate_traffic(n=1000):
    np.random.seed(42)
    
    # Normal Traffic (98%)
    n_normal = int(n * 0.98)
    # Attack Traffic (2%)
    n_attack = n - n_normal
    
    # Features: [Bytes, Duration, Source_Port, Packets_Sec]
    # Normal: Small bytes, short duration, low ports (80/443), low packets/sec
    normal_data = np.c_[
        np.random.normal(500, 100, n_normal),  # Bytes
        np.random.normal(0.1, 0.05, n_normal), # Duration
        np.random.choice([80, 443], n_normal), # Ports
        np.random.normal(10, 2, n_normal)      # Packets/sec
    ]
    
    # Attack: Large bytes (Exfil), Long duration (Slowloris), High Ports, High Packets (DDoS)
    # We mix different attack types
    attack_data = np.c_[
        np.random.normal(50000, 10000, n_attack), # Huge Bytes (Exfil)
        np.random.normal(10, 2, n_attack),        # Long Duration
        np.random.randint(1024, 65535, n_attack), # Random High Ports
        np.random.normal(1000, 200, n_attack)     # DDoS Packets
    ]
    
    X = np.r_[normal_data, attack_data]
    
    # Ground Truth Labels: 1 = Normal, -1 = Attack
    y_true = np.r_[np.ones(n_normal), -np.ones(n_attack)]
    
    # Feature Names
    columns = ['bytes', 'duration', 'src_port', 'packets_sec']
    df = pd.DataFrame(X, columns=columns)
    
    return df, y_true

print("Simulating Network Traffic...")
df, y_true = generate_traffic(n=1000)

# ---------------------------------------------------------
# 2. ISOLATION FOREST DETECTION
# ---------------------------------------------------------
print("\n--- Model 1: Isolation Forest ---")
# Contamination is 0.02 (2% attack rate)
clf_if = IsolationForest(contamination=0.02, random_state=42)
y_pred_if = clf_if.fit_predict(df)

print("Confusion Matrix:")
print(confusion_matrix(y_true, y_pred_if))
print("\nClassification Report:")
print(classification_report(y_true, y_pred_if, target_names=['Attack', 'Normal']))

# ---------------------------------------------------------
# 3. LOCAL OUTLIER FACTOR (LOF)
# ---------------------------------------------------------
print("\n--- Model 2: Local Outlier Factor ---")
# n_neighbors=20
clf_lof = LocalOutlierFactor(n_neighbors=20, contamination=0.02)
y_pred_lof = clf_lof.fit_predict(df)

print("Confusion Matrix:")
print(confusion_matrix(y_true, y_pred_lof))

# ---------------------------------------------------------
# 4. VISUALIZATION (Packets/Sec vs Bytes)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
# Plot Normal (Predicted)
normal = df[y_pred_if == 1]
attack = df[y_pred_if == -1]

plt.scatter(normal['packets_sec'], normal['bytes'], c='blue', alpha=0.5, label='Normal (Pred)')
plt.scatter(attack['packets_sec'], attack['bytes'], c='red', marker='x', label='Attack (Pred)')

plt.title("Network Traffic Anomaly Detection (Isolation Forest)")
plt.xlabel("Packets per Second")
plt.ylabel("Bytes Sent")
plt.legend()
plt.show()

# Insight Check
# Isolation Forest should separate the clusters cleanly.
# Attacks (High Packets, High Bytes) should be far from Normal (Low Packets, Low Bytes).
