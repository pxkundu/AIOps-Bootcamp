# Week 3 Day 4 Resources: Unsupervised Learning

> Essential reading and tools for mastering clustering, anomaly detection, and dimensionality reduction.

---

## 📚 Essential Reading

### Anomaly Detection
- **[Isolation Forest (Original Paper)](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)** - Read the intro to understand why "isolation" works better than "distance".
- **[Novelty and Outlier Detection (Scikit-learn)](https://scikit-learn.org/stable/modules/outlier_detection.html)** - Comparison of Isolation Forest, One-Class SVM, and LOF.
- **[AIOps: Anomaly Detection with Metrics](https://landing.ai/blog/anomaly-detection-vs-supervised-learning/)** - When to use which.

### Clustering
- **[Visualizing K-Means](https://www.naftaliharris.com/blog/visualizing-k-means-clustering/)** - Excellent interactive demo.
- **[DBSCAN Visualized](https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/)** - See how it handles arbitrary shapes.
- **[Hierarchical Clustering Explained](https://towardsdatascience.com/understanding-the-concept-of-hierarchical-clustering-technique-c6e8243758ec)**

### Dimensionality Reduction
- **[The Curse of Dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality)** - Why distance becomes meaningless in high dimensions.
- **[PCA Explained Visually](https://setosa.io/ev/principal-component-analysis/)**
- **[t-SNE Guide](https://distill.pub/2016/misread-tsne/)** - Critical reading: "How to Use t-SNE Effectively".

---

## 🛠️ Tools & Libraries

### Python
- **[Scikit-learn](https://scikit-learn.org/)** - The gold standard for these algorithms.
- **[PyOD (Python Outlier Detection)](https://pyod.readthedocs.io/en/latest/)** - Comprehensive toolbox specifically for anomaly detection (includes Deep Learning models like AutoEncoders).
- **[UMAP](https://umap-learn.readthedocs.io/en/latest/)** - Faster and often better alternative to t-SNE for visualization.

### Visualization
- **[Yellowbrick](https://www.scikit-yb.org/en/latest/)** - Visual analysis and diagnostic tools (e.g., Elbow Method plots, Silhouette Visualizers).

```bash
pip install pyod yellowbrick umap-learn
```

---

## 📊 Datasets for Practice

- **[KDD Cup 99](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)** - Network intrusion detection (classic AIOps dataset).
- **[NASA Bearing Dataset](https://www.kaggle.com/datasets/vinayak1209/nasa-bearing-dataset)** - Sensor data for predictive maintenance/anomaly detection.
- **[Credit Card Fraud](https://www.kaggle.com/mlg-ulb/creditcardfraud)** - Highly imbalanced, often treated as anomaly detection.

---

## 💡 Best Practices

1. **Scale Your Data**: Distance-based algorithms (K-Means, KNN, SVM) FAIL if features aren't scaled (e.g., `StandardScaler`).
2. **Reduce Dimensions First**: If you have >50 features, try PCA before clustering to remove noise.
3. **Don't Trust t-SNE Blindly**: It preserves local structure but distorts global distances. Use it for "hinting", not proof.
4. **Baseline with Simple Rules**: Before deploying an Isolation Forest, ask "Would a simple standard deviation check work?"
