# Solution for Exercise 01: LSTM Forecasting (The Vanishing Gradient)
# Week 4 Day 4

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ---------------------------------------------------------
# 1. GENERATE CHIRP SIGNAL
# ---------------------------------------------------------
print("Generating Non-Linear Chirp Signal...")
def generate_chirp(n_steps=1000):
    t = np.linspace(0, 50, n_steps)
    # Frequency increases (non-linear)
    data = np.sin(t**2 / 10) 
    return data.reshape(-1, 1)

data = generate_chirp()

# ---------------------------------------------------------
# 2. PREPROCESSING
# ---------------------------------------------------------
print("Scaling Data (MinMax)...")
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data)

# Split Train/Test (80/20)
train_size = int(len(data_scaled) * 0.8)
train, test = data_scaled[0:train_size,:], data_scaled[train_size:len(data_scaled),:]

# Create Sliding Window Dataset
def create_dataset(dataset, look_back=20):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

look_back = 20
X_train, y_train = create_dataset(train, look_back)
X_test, y_test = create_dataset(test, look_back)

# Reshape for LSTM: [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

print(f"Input Shape: {X_train.shape}")

# ---------------------------------------------------------
# 3. BUILD & TRAIN LSTM
# ---------------------------------------------------------
print("Training LSTM...")
model = Sequential()
model.add(LSTM(50, activation='tanh', input_shape=(look_back, 1))) # tanh is standard for LSTM
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

# Train
history = model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)
print(f"Final Loss: {history.history['loss'][-1]:.4f}")

# ---------------------------------------------------------
# 4. PREDICT & VISUALIZE
# ---------------------------------------------------------
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Invert predictions
train_predict = scaler.inverse_transform(train_predict)
y_train_inv = scaler.inverse_transform([y_train])
test_predict = scaler.inverse_transform(test_predict)
y_test_inv = scaler.inverse_transform([y_test])

# Plot Test Results
plt.figure(figsize=(10, 6))
plt.plot(y_test_inv.flatten(), label='Actual (Test Set)')
plt.plot(test_predict.flatten(), label='LSTM Prediction', linestyle='--')
plt.title("LSTM Forecasting Non-Linear Patterns")
plt.legend()
plt.show()

# Insight Check
# Does the line follow the oscillating pattern?
# If so, the LSTM learned the non-linear "chirp" frequency change.
