# Exercise 01: Discovering Log Patterns with Clustering

## 🎯 Objective
Use K-Means clustering to automatically group thousands of raw log messages into meaningful categories (e.g., "Database Errors", "Network Timeouts"). This is a key capability for "Log Reduction" in AIOps.

---

## 📊 The Data
You have a list of raw log messages. Many are similar but not identical (e.g., different timestamps or IDs).

```python
logs = [
    "2026-01-20 10:00:01 Connection timeout while connecting to db-01",
    "2026-01-20 10:00:02 Connection timeout while connecting to db-02",
    "2026-01-20 10:00:05 User 452 failed to login: invalid password",
    "2026-01-20 10:00:06 User 881 failed to login: invalid password",
    "2026-01-20 10:00:10 Disk usage critical on host-alpha (95%)",
    "2026-01-20 10:00:12 Disk usage critical on host-beta (98%)"
]
```

---

## 🛠️ Step 1: Preprocessing & Vectorization

Computers can't cluster text directly. We need to convert logs into numbers.

```python
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Clean logs (remove timestamps and variable numbers/IDs)
def clean_log(log):
    log = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', '', log)  # Remove timestamp
    log = re.sub(r'\d+', 'N', log)  # Replace numbers with 'N'
    return log.strip()

cleaned_logs = [clean_log(log) for log in logs]
print("Cleaned:", cleaned_logs)

# 2. Vectorize using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(cleaned_logs)

print(f"\nFeature names: {vectorizer.get_feature_names_out()}")
print(f"Shape: {X.shape}")
```

**Task:** Why do we replace numbers with 'N'? What happens if we don't?

---

## 🛠️ Step 2: Determine Optimal Clusters (Elbow Method)

Use the "Elbow Method" to find the right number of clusters ($K$).

```python
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Generate more synthetic data for this step
# (Imagine you have 1000 logs now)
# ...

inertias = []
K_range = range(1, 10)

for k in K_range:
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X)
    inertias.append(model.inertia_)

plt.plot(K_range, inertias, 'bx-')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.title('Elbow Method For Optimal k')
plt.show()
```

**Task:** Look at the plot. Where is the "elbow"? That's your optimal $K$.

---

## 🛠️ Step 3: Apply K-Means Clustering

```python
k = 3  # Assume 3 from elbow method
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(X)

# Organize results
df = pd.DataFrame({'log': logs, 'cleaned': cleaned_logs, 'cluster': labels})
print(df.sort_values('cluster'))
```

---

## 🛠️ Step 4: Interpret Clusters

Now, let's see what each cluster represents by finding the top keywords.

```python
print("\nTop terms per cluster:")
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

for i in range(k):
    print(f"Cluster {i}: ", end='')
    for ind in order_centroids[i, :3]:  # Top 3 words
        print(f"{terms[ind]} ", end='')
    print()
```

**Output Example:**
```
Cluster 0: timeout connecting db
Cluster 1: usage critical disk
Cluster 2: failed login invalid
```

---

## 🎯 Challenge: Moving to DBSCAN

K-Means forces every point into a cluster. What if some logs are just random noise?

**Task:** Implement DBSCAN on the same dataset.
1. Use `sklearn.cluster.DBSCAN`
2. Tune `eps` (try 0.3 to 0.7) and `min_samples` (try 2)
3. Identify which logs are marked as `-1` (noise).

```python
from sklearn.cluster import DBSCAN

# Your code here
```

**Question:** Which algorithm is better for this log data? Why?

---

## 📝 Submission
Submit a Python script or Notebook that:
1. Cleans and vectorizes a sample list of 20+ mixed logs.
2. Performs K-Means clustering.
3. Prints the original logs grouped by their new cluster ID.
4. Includes a 1-paragraph explanation of why you chose your specific $K$.
