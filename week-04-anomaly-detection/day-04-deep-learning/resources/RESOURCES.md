# Week 4 Day 4 Resources: Deep Learning

> Essential reading for LSTM, Autoencoders, and modern Time Series AI.

---

## 📚 Essential Reading

### Understanding LSTM
- **[Understanding LSTM Networks (Colah's Blog)](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)** - The definitive guide with clear diagrams. Mandatory reading.
- **[Illustrated Guide to Recurrent Neural Networks](https://towardsdatascience.com/illustrated-guide-to-recurrent-neural-networks-79e5eb8049c9)** - Visual explanation of vanishing gradients.

### Anomaly Detection with Autoencoders
- **[Timeseries Anomaly Detection with Autoencoder (Keras)](https://keras.io/examples/timeseries/timeseries_anomaly_detection/)** - Official tutorial using `Conv1D` and `LSTM`.
- **[Deep Learning for Anomaly Detection: A Survey](https://arxiv.org/abs/1901.03407)** - Comprehensive paper on all DL methods (GANs, VAEs).

### Predictive Maintenance
- **[NASA Bearing Dataset](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/)** - Real-world vibration data for failure prediction.
- **[Remaining Useful Life (RUL) Prediction](https://towardsdatascience.com/remaining-useful-life-prediction-with-lstm-9d7e63289019)** - Estimating *when* it will fail.

---

## 🛠️ Tools & Libraries

### Deep Learning Frameworks
- **[TensorFlow / Keras](https://www.tensorflow.org/)** - Creating models with `tf.keras.layers.LSTM`.
- **[PyTorch](https://pytorch.org/)** - For more control (research-heavy).
- **[GluonTS](https://ts.gluon.ai/)** - Amazon's probabilistic time series library (built on MXNet/PyTorch).

### Visualization
- **[TensorBoard](https://www.tensorflow.org/tensorboard)** - Visualizing training loss curves in real-time.

```bash
pip install tensorflow matplotlib scikit-learn
```

---

## 💡 Pro Tips for SREs

1.  **Don't Overkill:**
    - If `ARIMA` gives 95% accuracy, do NOT use `LSTM`. LSTMs are 100x slower to train and harder to debug.
    - Only use DL for complex, non-linear, multi-variate problems (e.g., correlating 1000 sensors).

2.  **Sequence Length Matters:**
    - Setting `window_size=10` might miss long-term patterns.
    - Setting `window_size=1000` will vanish gradients.
    - Start small (e.g., 50-100 steps).

3.  **Data Quality is Everything:**
    - Neural Nets fail spectacularly on bad data (garbage in, garbage out).
    - Always normalize/scale your data (`MinMaxScaler`) before feeding it to an LSTM.
