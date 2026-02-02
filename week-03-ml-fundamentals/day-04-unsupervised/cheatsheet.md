# Unsupervised Learning Cheat Sheet

> Quick reference for clustering, anomaly detection, and dimensionality reduction.

---

## 🎯 Core Concepts

### Unsupervised Learning
**No labels** - find hidden patterns, structure, and groupings in data.

**Three Main Tasks:**
1. **Clustering:** Group similar data points
2. **Anomaly Detection:** Find outliers
3. **Dimensionality Reduction:** Reduce features while preserving information

---

## 🔵 Clustering Algorithms

### 1. K-Means
```python
from sklearn.cluster import KMeans

# Fit
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X)

# Get centroids
centroids = kmeans.cluster_centers_

# Predict new data
new_labels = kmeans.predict(X_new)
```

**Choosing K (Elbow Method):**
```python
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X)
    inertias.append(km.inertia_)

# Plot and look for "elbow"
plt.plot(range(1, 11), inertias, marker='o')
```

**Pros:** Fast, simple  
**Cons:** Must choose K, assumes spherical clusters

---

### 2. DBSCAN
```python
from sklearn.cluster import DBSCAN

# Fit
dbscan = DBSCAN(eps=0.5, min_samples=5)
labels = dbscan.fit_predict(X)

# -1 = noise/outlier
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)
```

**Parameters:**
- `eps`: Max distance between neighbors
- `min_samples`: Min points to form dense region

**Pros:** Finds arbitrary shapes, detects outliers, no need to choose K  
**Cons:** Sensitive to parameters, struggles with varying densities

---

### 3. Hierarchical Clustering
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Compute linkage
Z = linkage(X, method='ward')

# Plot dendrogram
dendrogram(Z)

# Cut tree to get clusters
clustering = AgglomerativeClustering(n_clusters=3)
labels = clustering.fit_predict(X)
```

**Linkage Methods:**
- `ward`: Minimize variance (most common)
- `complete`: Maximum distance
- `average`: Average distance
- `single`: Minimum distance

**Pros:** No need to choose K upfront, visualize relationships  
**Cons:** Slow for large datasets (O(n²))

---

## 🚨 Anomaly Detection

### 1. Isolation Forest
```python
from sklearn.ensemble import IsolationForest

# Fit
iso_forest = IsolationForest(
    contamination=0.05,  # Expected % of anomalies
    random_state=42
)
predictions = iso_forest.fit_predict(X)

# -1 = anomaly, 1 = normal
anomalies = X[predictions == -1]
```

**Pros:** Fast, handles high-D data, no assumptions about distribution  
**Cons:** Contamination parameter must be set

---

### 2. One-Class SVM
```python
from sklearn.svm import OneClassSVM

# Fit on normal data only
svm = OneClassSVM(nu=0.05, kernel='rbf', gamma='auto')
svm.fit(X_normal)

# Predict
predictions = svm.predict(X_test)  # -1 = anomaly
```

**Parameters:**
- `nu`: Upper bound on fraction of outliers
- `kernel`: 'rbf', 'linear', 'poly'

**Pros:** Tight boundary, works with only normal data  
**Cons:** Slow for large datasets, sensitive to kernel choice

---

### 3. Statistical (Z-Score)
```python
from scipy import stats
import numpy as np

# Calculate Z-scores
z_scores = np.abs(stats.zscore(X))

# Threshold (typically 3)
anomalies = X[z_scores > 3]
```

**Pros:** Simple, interpretable  
**Cons:** Assumes Gaussian distribution, univariate

---

### 4. Local Outlier Factor (LOF)
```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
predictions = lof.fit_predict(X)  # -1 = anomaly
```

**Pros:** Detects local anomalies (different densities)  
**Cons:** Slow, sensitive to n_neighbors

---

## 📉 Dimensionality Reduction

### 1. PCA (Principal Component Analysis)
```python
from sklearn.decomposition import PCA

# Reduce to 2D
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Explained variance
print(pca.explained_variance_ratio_)
print(f"Total: {pca.explained_variance_ratio_.sum():.2%}")

# Transform new data
X_new_reduced = pca.transform(X_new)
```

**Choose n_components:**
```python
# Keep 95% of variance
pca = PCA(n_components=0.95)
X_reduced = pca.fit_transform(X)
print(f"Reduced to {pca.n_components_} components")
```

**Pros:** Fast, interpretable, can inverse transform  
**Cons:** Linear only, assumes high variance = important

---

### 2. t-SNE
```python
from sklearn.manifold import TSNE

# Reduce to 2D (for visualization only!)
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_2d = tsne.fit_transform(X)

# Plot
plt.scatter(X_2d[:, 0], X_2d[:, 1])
```

**Parameters:**
- `perplexity`: Balance local vs global structure (5-50)
- `n_iter`: Iterations (default 1000)

**Pros:** Preserves local structure, great for visualization  
**Cons:** Slow, non-deterministic, can't transform new data

**Pro Tip:** Use PCA first to reduce to ~50D, then t-SNE.

---

### 3. UMAP (Modern Alternative)
```python
import umap

reducer = umap.UMAP(n_components=2, random_state=42)
X_2d = reducer.fit_transform(X)
```

**Pros:** Faster than t-SNE, preserves global + local structure  
**Cons:** Requires extra library (`pip install umap-learn`)

---

## 📊 Evaluation Metrics

### 1. Silhouette Score
```python
from sklearn.metrics import silhouette_score

score = silhouette_score(X, labels)
# Range: [-1, 1], higher is better
# 1 = perfect, 0 = overlapping, -1 = wrong clusters
```

---

### 2. Davies-Bouldin Index
```python
from sklearn.metrics import davies_bouldin_score

score = davies_bouldin_score(X, labels)
# Lower is better (0 = perfect)
```

---

### 3. Calinski-Harabasz Index
```python
from sklearn.metrics import calinski_harabasz_score

score = calinski_harabasz_score(X, labels)
# Higher is better
```

---

### 4. Inertia (K-Means only)
```python
inertia = kmeans.inertia_
# Sum of squared distances to nearest centroid
# Lower is better, but watch for overfitting
```

---

## 🛠️ Feature Extraction for Text

### TF-IDF Vectorization
```python
from sklearn.feature_extraction.text import TfidfVectorizer

logs = ["error timeout", "network failed", "error timeout"]

vectorizer = TfidfVectorizer(max_features=100)
X_tfidf = vectorizer.fit_transform(logs).toarray()

# Get feature names
print(vectorizer.get_feature_names_out())
```

**Parameters:**
- `max_features`: Limit vocabulary size
- `ngram_range`: (1, 2) for unigrams + bigrams
- `min_df`: Ignore terms in < N documents
- `max_df`: Ignore terms in > N% of documents

---

### Count Vectorizer
```python
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
X_counts = vectorizer.fit_transform(logs).toarray()
```

---

## 🔄 Pipelines

### Clustering Pipeline
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('kmeans', KMeans(n_clusters=3, random_state=42))
])

labels = pipeline.fit_predict(X)
```

---

### Anomaly Detection Pipeline
```python
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('iso_forest', IsolationForest(contamination=0.05, random_state=42))
])

predictions = pipeline.fit_predict(X)
```

---

## 🎯 Quick Decision Guide

### Clustering
| Scenario | Algorithm |
|----------|-----------|
| Know K, spherical clusters | K-Means |
| Unknown K, arbitrary shapes | DBSCAN |
| Need hierarchy/dendrogram | Hierarchical |
| Text data | K-Means on TF-IDF |

---

### Anomaly Detection
| Scenario | Algorithm |
|----------|-----------|
| High-dimensional, fast | Isolation Forest |
| Only normal data for training | One-Class SVM |
| Simple, univariate | Z-Score |
| Varying densities | LOF |

---

### Dimensionality Reduction
| Scenario | Algorithm |
|----------|-----------|
| Feature reduction for modeling | PCA |
| Visualization only | t-SNE or UMAP |
| Need to transform new data | PCA |
| Preserve local structure | t-SNE/UMAP |

---

## 🐛 Common Pitfalls

### ❌ Not Scaling Data
```python
# WRONG
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)  # Features have different scales!

# RIGHT
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans.fit(X_scaled)
```

---

### ❌ Using t-SNE for Feature Reduction
```python
# WRONG - t-SNE can't transform new data!
tsne = TSNE(n_components=2)
X_train_2d = tsne.fit_transform(X_train)
X_test_2d = tsne.transform(X_test)  # ERROR!

# RIGHT - Use PCA
pca = PCA(n_components=2)
X_train_2d = pca.fit_transform(X_train)
X_test_2d = pca.transform(X_test)  # Works!
```

---

### ❌ Ignoring Curse of Dimensionality
```python
# WRONG - DBSCAN in 100D
dbscan = DBSCAN(eps=0.5)
dbscan.fit(X_100d)  # Everything is far apart!

# RIGHT - Reduce dimensions first
pca = PCA(n_components=10)
X_10d = pca.fit_transform(X_100d)
dbscan.fit(X_10d)
```

---

## 📚 Essential Imports

```python
# Clustering
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# Anomaly Detection
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from scipy import stats

# Dimensionality Reduction
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
# import umap  # pip install umap-learn

# Text Vectorization
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# Evaluation
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)

# Preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
```

---

## 🔗 Resources

- [Scikit-learn Clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [Anomaly Detection Guide](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [PCA Explained](https://builtin.com/data-science/step-step-explanation-principal-component-analysis)
- [t-SNE Explained](https://distill.pub/2016/misread-tsne/)
