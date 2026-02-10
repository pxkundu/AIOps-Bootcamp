# Exercise 02: The Neural Mirror (Autoencoders)

## 🎯 Objective
Use an **LSTM Autoencoder** to reconstruct normal time series data. Then, feed it anomalous data and watch it *fail* to reconstruct it. The reconstruction error IS the anomaly score.

---

## 📊 The Data
We will simulate "Heartbeat" traffic:
- **Normal:** Repeating Sine Wave with noise.
- **Anomaly:** Flatline (Dead Server) or Square Wave (Attack).

```python
import numpy as np
import matplotlib.pyplot as plt

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
```

## 🛠️ Step 1: Preprocessing
1.  Reshape features to `(Samples, TimeSteps, 1)`. `X_train.shape` should become `(1000, 30, 1)`.
2.  (Optional) Scale data if not already centered.

## 🛠️ Step 2: The Encoder-Decoder
Build an LSTM Autoencoder.

```python
from tensorflow.keras.layers import RepeatVector, TimeDistributed, Dense, LSTM
from tensorflow.keras.models import Sequential

model = Sequential()
# Encoder: Reduce from 30 -> 16
model.add(LSTM(16, activation='relu', input_shape=(30, 1), return_sequences=False))
model.add(RepeatVector(30)) # Copy compressed vector 30 times

# Decoder: Expand from 16 -> 30
model.add(LSTM(16, activation='relu', return_sequences=True))
model.add(TimeDistributed(Dense(1))) # Output 1 feature per step

model.compile(optimizer='adam', loss='mse')
```

## 🛠️ Step 3: Train & Reconstruct
1.  Fit on `X_train` only.
2.  Predict on `X_test_normal` and calculate MSE (Reconstruction Error).
    *   Error should be LOW (~0.01).
3.  Predict on `X_test_anomaly` and calculate MSE.
    *   Error should be HIGH (> 0.5).

## 🛠️ Step 4: Visualize Understanding
Plot:
- Original sequence (Blue)
- Reconstructed sequence (Red)
- Anomaly Threshold (Green Line)

Notice how the Red line hugs the Normal Blue line, but fails completely on the Anomalous Blue line?

## 📝 Deliverable
A notebook showing the plot of "Normal Reconstruction" vs "Anomaly Reconstruction".
