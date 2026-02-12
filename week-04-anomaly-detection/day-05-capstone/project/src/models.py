from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import numpy as np

class PointDetector:
    def __init__(self, contamination=0.01):
        """
        Detects anomalies in multi-variate space.
        Suitable for: Flash Crash, Correlated Failures, Contextual Spikes.
        """
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def train(self, X):
        """
        X: DataFrame of features (e.g. CPU, Fan, Hour)
        """
        self.model.fit(X)

    def predict(self, X_sample):
        """
        Returns -1 for anomaly, 1 for normal.
        """
        return self.model.predict(X_sample)

class TrendDetector:
    def __init__(self, threshold=3.0):
        """
        Simple Z-Score based trend detector.
        Suitable for: Slow Burn, Linear Drift.
        """
        self.mean = 0
        self.std = 1
        self.threshold = threshold

    def train(self, series):
        """
        series: Pandas Series or NumPy array of a metric (e.g. CPU)
        """
        self.mean = np.mean(series)
        self.std = np.std(series)
        print(f"  [TrendDetector] Mean: {self.mean:.2f}, Std: {self.std:.2f}")

    def predict(self, value):
        """
        Returns True if value is outside Mean +/- 3*Std.
        """
        z_score = abs(value - self.mean) / self.std
        return z_score > self.threshold
