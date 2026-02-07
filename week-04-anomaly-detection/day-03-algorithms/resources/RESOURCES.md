# Week 4 Day 3 Resources: Anomaly Detection

> Essential reading for Isolation Forest, LOF, and Real-world Intrusion Detection.

---

## 📚 Essential Reading

### The Core Algorithms
- **[Isolation Forest (Liu et al. 2008)](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)** - The original paper. Surprisingly readable.
- **[Local Outlier Factor (LOF)](https://scikit-learn.org/stable/modules/outlier_detection.html#local-outlier-factor)** - Scikit-learn guide comparing IF, LOF, and One-Class SVM.
- **[Anomaly Detection with RCF (AWS)](https://docs.aws.amazon.com/sagemaker/latest/dg/randomcutforest.html)** - How AWS uses Random Cut Forest (a variant of IF) for CloudWatch Anomaly Detection.

### Applied SRE Context
- **[Datadog: Anomaly Detection vs Thresholds](https://www.datadoghq.com/blog/anomaly-detection-algorithms-guide/)** - Why static thresholds fail.
- **[Elasticsearch: Machine Learning Anomaly Detection](https://www.elastic.co/guide/en/machine-learning/current/ml-overview.html)** - Uses unsupervised learning on log streams.

---

## 🛠️ Tools & Libraries

### Python Ecosystem
- **[Scikit-Learn](https://scikit-learn.org/stable/modules/outlier_detection.html)** - Standard for `IsolationForest`, `LocalOutlierFactor`, `OneClassSVM`.
- **[PyOD (Python Outlier Detection)](https://pyod.readthedocs.io/en/latest/)** - Comprehensive toolbox with 30+ algorithms (COPOD, ECOD, AutoEncoder). Highly recommended for advanced use.
  - `pip install pyod`
- **[Alibi Detect](https://docs.seldon.io/projects/alibi-detect/en/latest/)** - Specializes in Drift Detection and Adversarial detection (for Week 6).

### Visualization
- **[Yellowbrick](https://www.scikit-yb.org/en/latest/)** - Has specific visualizers for clustering and outliers.

```bash
pip install pyod yellowbrick
```

---

## 📊 Datasets for Practice

- **[KDD Cup 99](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)** - The classic Network Intrusion Detection dataset.
- **[Credit Card Fraud](https://www.kaggle.com/mlg-ulb/creditcardfraud)** - Imbalanced classification vs Anomaly Detection.
- **[NAB (Numenta Anomaly Benchmark)](https://github.com/numenta/NAB)** - Real-world streaming data with labeled anomalies.

---

## 💡 Pro Tips for SREs

1.  **Don't Trust Default Contamination:**
    - Sklearn defaults to `contamination='auto'`. Often better to set it to your expected attack rate (e.g., `0.01` for 1%).
    - If you set it too high, you flag legitimate users. Too low, you miss attacks.

2.  **Feature Engineering is king:**
    - Raw timestamps are useless. Converting to `hour_of_day`, `is_weekend`, `time_since_last_error` gives the algorithm *context*.
    - Difference/Lag features (Day 1) work wonders here too.

3.  **Explainability:**
    - Why is this point an anomaly?
    - Use SHAP (Day 5 Week 3) on your Isolation Forest model! It will tell you "High Latency + Low CPU" caused the flag.
