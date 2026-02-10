# Deep Learning Cheat Sheet

> **Libraries:** `tensorflow.keras`, `sklearn.preprocessing`  
> **Key Layers:** `LSTM`, `Dense`, `RepeatVector`, `TimeDistributed`

---

## 🏗️ Data Preparation (Crucial!)

LSTMs require **3D Input**: `(Samples, Time Steps, Features)`.

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# 1. Scale Data (0-1)
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# 2. Reshape into Windows (Sliding Window)
def create_dataset(dataset, look_back=10):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)

# Reshape for Keras: [samples, time steps, features]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
```

---

## 🔮 LSTM Forecasting (Many-to-One)

Predict next value based on past sequence.

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential()
# complex LSTM layer
model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 1)))
# usually stacking 2 layers works better
model.add(LSTM(50))
model.add(Dense(1)) # Output is 1 number (prediction)

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=2)
```

---

## 🪞 Autoencoder for Anomaly Detection (Many-to-Many)

Reconstruct sequence. High error = Anomaly.

```python
from tensorflow.keras.layers import RepeatVector, TimeDistributed

model = Sequential()

# Encoder
model.add(LSTM(128, activation='relu', input_shape=(timesteps, n_features), return_sequences=True))
model.add(LSTM(64, activation='relu', return_sequences=False))
model.add(RepeatVector(timesteps))

# Decoder
model.add(LSTM(64, activation='relu', return_sequences=True))
model.add(LSTM(128, activation='relu', return_sequences=True))
model.add(TimeDistributed(Dense(n_features)))

model.compile(optimizer='adam', loss='mse')
model.summary()
```

---

## 📉 Diagnostics

Visualize Loss during training to detect Overfitting.

```python
history = model.fit(...)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.show()
```

Detect Anomaly Threshold:

```python
# Create distribution of loss on normal training data
train_pred = model.predict(X_train)
train_mae_loss = np.mean(np.abs(train_pred - X_train), axis=1)

# Pick threshold (e.g. max error on training data)
threshold = np.max(train_mae_loss)
print(f"Reconstruction error threshold: {threshold}")
```

---

## ⚡ Common Pitfalls

| Problem | Fix |
|---|---|
| **Exploding Gradients** | Use `clipnorm=1.0` in optimizer or LeakyReLU. |
| **Vanishing Gradients** | Use LSTM/GRU instead of SimpleRNN. |
| **Overfitting** | Add `Dropout(0.2)` layers. Early Stopping. |
| **Bad Predictions** | Did you `MinMaxScaler`? Check input shape `(N, T, F)`. |
