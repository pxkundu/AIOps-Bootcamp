# Solution for Exercise 02: Autoencoder Anomaly Detection (The Mirror)
# Week 4 Day 4

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed

# ---------------------------------------------------------
# 1. GENERATE DATA
# ---------------------------------------------------------
print("Generating Heartbeat Data...")

def generate_sequences(n_samples=1000, time_steps=30):
    # Normal: Sine Wave
    X = []
    for _ in range(n_samples):
        start = np.random.rand()
        t = np.linspace(start, start + 3, time_steps)
        signal = np.sin(t) + np.random.normal(0, 0.1, time_steps) 
        X.append(signal) # Shape (30,)
    return np.array(X)

X_train = generate_sequences(n_samples=1000)
X_test_normal = generate_sequences(n_samples=100)

# Simulate Anomaly: Flatline
X_test_anomaly = np.zeros((20, 30)) + np.random.normal(0, 0.1, (20, 30))

# Reshape for LSTM: [samples, time steps, features]
X_train = np.reshape(X_train, (1000, 30, 1))
X_test_normal = np.reshape(X_test_normal, (100, 30, 1))
X_test_anomaly = np.reshape(X_test_anomaly, (20, 30, 1))

print(f"X_train Shape: {X_train.shape}")
print(f"X_test_anomaly Shape: {X_test_anomaly.shape}")

# ---------------------------------------------------------
# 2. BUILD AUTOENCODER
# ---------------------------------------------------------
print("Training Autoencoder...")

model = Sequential()
# Encoder: Reduce from 30 -> 16
model.add(LSTM(16, activation='relu', input_shape=(30, 1), return_sequences=False))
model.add(RepeatVector(30)) # Copy compressed vector 30 times

# Decoder: Expand from 16 -> 30
model.add(LSTM(16, activation='relu', return_sequences=True))
model.add(TimeDistributed(Dense(1))) # Output 1 feature per step

model.compile(optimizer='adam', loss='mse')
history = model.fit(X_train, X_train, epochs=10, batch_size=32, verbose=0)

print(f"Final Train Loss: {history.history['loss'][-1]:.4f}")

# ---------------------------------------------------------
# 3. PREDICT & CALCULATE ERROR
# ---------------------------------------------------------
# Reconstruct Normal
pred_normal = model.predict(X_test_normal)
mse_normal = np.mean(np.power(X_test_normal - pred_normal, 2), axis=1)

# Reconstruct Anomaly
pred_anomaly = model.predict(X_test_anomaly)
mse_anomaly = np.mean(np.power(X_test_anomaly - pred_anomaly, 2), axis=1)

print(f"\nReconstruction Error (Normal): {np.mean(mse_normal.flatten()):.4f}")
print(f"Reconstruction Error (Anomaly): {np.mean(mse_anomaly.flatten()):.4f}")

# ---------------------------------------------------------
# 4. VISUALIZATION
# ---------------------------------------------------------
plt.figure(figsize=(12, 6))

# Plot Error Distribution
plt.hist(mse_normal.flatten(), bins=20, alpha=0.5, label='Normal Error', color='blue')
plt.hist(mse_anomaly.flatten(), bins=20, alpha=0.5, label='Anomaly Error', color='red')
plt.title("Reconstruction Error Histogram")
plt.xlabel("Reconstruction Error (MSE)")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Insight Check
# Do you see two distinct histograms?
# Blue (Normal) should be near 0. Red (Anomaly) should be > 0.5.
# If so, you have built a successful Anomaly Detector!
