# Solution for "The Neural Link" Game
# Week 4 Day 4 Gamification

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed

def solve_level_1_wave(dataset):
    """
    Level 1: Predict complex wave.
    Tool: LSTM Many-to-One.
    """
    print("🧠 Neural Link Level 1: The Wave")
    model = Sequential()
    # Input: (Timesteps, Features)
    model.add(LSTM(50, activation='relu', input_shape=(dataset.shape[1], 1)))
    model.add(Dense(1)) # Predict next step
    model.compile(optimizer='adam', loss='mse')
    return model

def solve_level_2_mirror(timesteps, features):
    """
    Level 2: The Encoder-Decoder.
    Tool: LSTM Autoencoder (Compression).
    """
    print("🧠 Neural Link Level 2: The Mirror")
    model = Sequential()
    # Encoder
    model.add(LSTM(32, activation='relu', input_shape=(timesteps, features), return_sequences=False))
    model.add(RepeatVector(timesteps))
    # Decoder
    model.add(LSTM(32, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(features)))
    model.compile(optimizer='adam', loss='mse')
    return model

def solve_level_3_crack(model, normal_data, anomaly_data):
    """
    Level 3: Detect the Break.
    Tool: Reconstruction Error Thresholding.
    """
    print("🧠 Neural Link Level 3: The Crack")
    
    # 1. Start with Normal Error Baseline
    normal_pred = model.predict(normal_data)
    normal_err = np.mean(np.abs(normal_pred - normal_data), axis=1) # MAE per sample
    threshold = np.max(normal_err)
    
    # 2. Test Anomaly
    anomaly_pred = model.predict(anomaly_data)
    anomaly_err = np.mean(np.abs(anomaly_pred - anomaly_data), axis=1)
    
    # Check if error > threshold
    alarms = anomaly_err > threshold
    return np.sum(alarms)

# Mock Runner
import numpy as np
if __name__ == "__main__":
    # Simulate
    X = np.random.rand(100, 10, 1) # 100 samples, 10 steps, 1 feature
    model_ae = solve_level_2_mirror(10, 1)
    
    print("\nTraining Mock Model...")
    model_ae.fit(X, X, epochs=1, verbose=0)
    
    print("Testing Crack Detection...")
    detections = solve_level_3_crack(model_ae, X, X * 10) # X*10 is anomalous
    print(f"Detected {detections}/100 Anomalies.")
    
    print("\n🏆 MISSION ACCOMPLISHED. NEURAL LINK STABILIZED.")
