# Exercise 01: The Vanishing Gradient (LSTM Forecast)

## 🎯 Objective
Learn why **Long Short-Term Memory (LSTM)** networks are superior to standard RNNs for long sequences. You will build a model to forecast a complex, non-linear sine wave.

---

## 📊 The Data
We'll generate a sine wave with varying frequency (chirp signal). This is harder than a simple sine wave because the pattern changes over time.

```python
import numpy as np
import matplotlib.pyplot as plt

def generate_chirp(n_steps=1000):
    t = np.linspace(0, 50, n_steps)
    # Frequency increases over time
    data = np.sin(t**2 / 10) 
    return data

data = generate_chirp()
plt.plot(data[:200])
plt.title("Chirp Signal (Frequency Increases)")
plt.show()
```

## 🛠️ Step 1: Preprocessing
LSTMs are sensitive to scale.
1.  Use `MinMaxScaler` to scale data to `[0, 1]`.
2.  Create a Sliding Window dataset (`X`, `y`).
    *   `X`: Past 20 steps.
    *   `y`: Next step.
3.  Reshape `X` to `(Samples, 20, 1)`.

## 🛠️ Step 2: Build the LSTM
Use Keras `Sequential` API.

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential()
# Input shape: (TimeSteps, Features)
model.add(LSTM(50, activation='relu', input_shape=(20, 1))) 
model.add(Dense(1)) 
model.compile(optimizer='adam', loss='mse')
```

## 🛠️ Step 3: Train & Predict
1.  Fit for 20 epochs.
2.  Predict on the **Test Set** (Last 200 points).
3.  Inverse Transform the predictions back to original scale.

## 🛠️ Step 4: Compare
Plot Actual vs Predicted. Does the LSTM capture the changing frequency?

## 📝 Deliverable
A notebook showing the plot of Predicted vs Actual values on the test set.
