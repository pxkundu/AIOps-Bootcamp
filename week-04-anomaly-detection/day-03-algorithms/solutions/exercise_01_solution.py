# Solution for Exercise 01: Isolation Forest Lab
# Week 4 Day 3

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ---------------------------------------------------------
# 1. GENERATE DATA
# ---------------------------------------------------------
print("Generating synthetic server metrics...")
np.random.seed(42)

# Normal Traffic (Two Clusters)
# Cluster 1: Night Shift (Low CPU, Low Mem) centered at (2, 2)
X1 = 0.3 * np.random.randn(100, 2) + [2, 2]
# Cluster 2: Day Shift (High CPU, High Mem) centered at (-2, -2)
X2 = 0.3 * np.random.randn(100, 2) + [-2, -2]
X_train = np.r_[X1, X2]

# Anomalies (Attacks) - Uniform Random Noise
X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))

X = np.r_[X_train, X_outliers]

# ---------------------------------------------------------
# 2. DETECT OUTLIERS
# ---------------------------------------------------------
print("Training Isolation Forest...")
# contamination=0.1 means we expect ~10% anomalies
# Use 0.1 because 20/220 ~ 9%
clf = IsolationForest(contamination=0.1, random_state=42)
clf.fit(X)

# Predict (-1 = Anomaly, 1 = Normal)
y_pred = clf.predict(X)

# ---------------------------------------------------------
# 3. VISUALIZATION
# ---------------------------------------------------------
print("Plotting decision boundary...")

# Create meshgrid
xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(10, 8))
plt.title("IsolationForest Decision Boundary")
# Plot contours (darker blue = more normal)
plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

# Correct Predictions
inliers = X[y_pred == 1]
outliers = X[y_pred == -1]

plt.scatter(inliers[:, 0], inliers[:, 1], c='white', s=20, edgecolor='k', label='Normal (Pred)')
plt.scatter(outliers[:, 0], outliers[:, 1], c='red', s=20, edgecolor='k', label='Anomaly (Pred)')
plt.legend()
plt.show()

# ---------------------------------------------------------
# 4. ANALYSIS
# ---------------------------------------------------------
n_errors = (y_pred != -1).sum() # Assuming all X_outliers should be -1 (simplified check)
# In reality, we don't know ground truth for unlabeled data, but here we do.
# Let's count how many of the LAST 20 points (X_outliers) were caught.
caught = (y_pred[-20:] == -1).sum()
missed = 20 - caught

print(f"\nAnalysis:")
print(f"Attacks Caught: {caught}/20")
print(f"Attacks Missed: {missed}/20")
if missed > 0:
    print("  -> Try increasing 'contamination' or 'n_estimators' to catch more.")
else:
    print("  -> Perfect detection!")
