# Solution for Day 4 Project: Predictive Maintenance
# Week 4 Day 4

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed

# ---------------------------------------------------------
# 1. LOAD & PREPROCESS
# ---------------------------------------------------------
print("Loading Sensor Data from 'data/bearing_sim.py'...")
# Run the generator inline for simplicity
def generate_bearing_data(n_steps=10000):
    np.random.seed(42)
    time = np.arange(n_steps)
    vib_x = np.random.normal(0, 1, n_steps)
    temp = 50 + 5 * np.sin(time / 500) 
    # Degrading 6000-8000
    mask = (time >= 6000) & (time < 8000)
    factor = (time[mask] - 6000) / 2000
    vib_x[mask] *= (1 + 5 * factor)
    temp[mask] += 20 * factor
    # Critical 8000+
    mask2 = time >= 8000
    vib_x[mask2] *= 10
    temp[mask2] += 50
    return pd.DataFrame({'vib_x': vib_x, 'temp': temp})

df = generate_bearing_data()
data = df.values

# Use only Healthy (0-5000) for Training
train_len = 5000
data_train = data[:train_len]
data_test = data

# Scale
scaler = MinMaxScaler()
scaler.fit(data_train)
data_train_scaled = scaler.transform(data_train)
data_test_scaled = scaler.transform(data_test)

def create_windows(X, window=50):
    Xs = []
    for i in range(len(X) - window - 1):
        Xs.append(X[i:(i + window)])
    return np.array(Xs)

X_train = create_windows(data_train_scaled)
X_test = create_windows(data_test_scaled)

print(f"X_train Shape: {X_train.shape}")
print(f"X_test Shape: {X_test.shape}")

# ---------------------------------------------------------
# 2. TRAIN AUTOENCODER
# ---------------------------------------------------------
print("Training Autoencoder on Healthy Data...")

model = Sequential()
model.add(LSTM(64, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
model.add(LSTM(32, activation='relu', return_sequences=False))
model.add(RepeatVector(X_train.shape[1]))
model.add(LSTM(32, activation='relu', return_sequences=True))
model.add(LSTM(64, activation='relu', return_sequences=True))
model.add(TimeDistributed(Dense(X_train.shape[2])))

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, X_train, epochs=5, batch_size=64, verbose=1)

# ---------------------------------------------------------
# 3. DETECT ANOMALIES
# ---------------------------------------------------------
print("Predicting Anomalies...")
X_pred = model.predict(X_test)
# Mean Absolute Error per window
mae_loss = np.mean(np.abs(X_pred - X_test), axis=1) # Shape (N, 50, 2) -> (N, 50) -> Need mean over time
mae_loss = np.mean(mae_loss, axis=1) # Shape (N,)

# Threshold: Max Train Loss + Buffer
train_pred = model.predict(X_train)
train_mae = np.mean(np.abs(train_pred - X_train), axis=1)
train_mae = np.mean(train_mae, axis=1)
threshold = np.max(train_mae) * 1.05 # 5% buffer

anomalies = mae_loss > threshold
print(f"Threshold: {threshold:.4f}")
print(f"Total Anomalies Detected: {np.sum(anomalies)}")

# ---------------------------------------------------------
# 4. VISUALIZE
# ---------------------------------------------------------
plt.figure(figsize=(12, 6))
plt.plot(mae_loss, label='Reconstruction Error')
plt.axhline(threshold, color='r', linestyle='--', label='Anomaly Threshold')

# Ground Truth Overlay (Start of Degradation)
plt.axvline(6000, color='orange', linestyle=':', label='Degradation Starts (True)')
plt.axvline(8000, color='red', linestyle=':', label='Simulation Failure (True)')

plt.title("Early Warning System: Loss vs Time")
plt.legend()
plt.show()

# Insight Check
# Does the blue line (Error) curve upwards > Threshold BEFORE 8000?
# Ideally around 6200. That gives us 1800 steps (hours) of warning!
