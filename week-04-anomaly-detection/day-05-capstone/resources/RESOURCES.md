# Week 4 Day 5 Resources: AIOps Architecture

> **Focus:** MLOps, System Design, and Real-World Anomaly Detection at Scale.

---

## 📚 Essential Reading

### System Design
- **[Designing Machine Learning Systems (Chip Huyen)](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)** - *The* book on production ML. Ch 7 (Monitoring) is gold.
- **[Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)** - Why alerts must be actionable.

### Drift & Maintenance
- **[Concept Drift in Streaming Data](https://towardsdatascience.com/machine-learning-in-production-why-you-should-care-about-data-drift-d7b3240cdd36)** - Why models rot.
- **[Shadow Deployment Pattern](https://martinfowler.com/articles/cd4ml.html)** - Testing new models safely alongside old ones.

### Commercial Comparisons
- **[DataDog Anomaly Detection](https://docs.datadoghq.com/monitors/types/anomaly/)** - How the pros do it (ARIMA + Robust Regression).
- **[Elastic (ELK) Machine Learning](https://www.elastic.co/guide/en/machine-learning/current/ml-overview.html)** - Unsupervised anomaly detection on logs.

---

## 🛠️ Tools & Libraries

### Orchestration
- **[MLflow](https://mlflow.org/)** - Managing experiments and model registry (`model.pkl` versions).
- **[Airflow](https://airflow.apache.org/)** - Scheduling the "Weekly Retrain" job.

### Serving (Low Latency)
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance Python API for serving predictions (<10ms).
- **[ONNX Runtime](https://onnxruntime.ai/)** - optimizing models to run faster than native PyTorch/Sklearn.
- **[Triton Inference Server](https://developer.nvidia.com/nvidia-triton-inference-server)** - NVIDIA's production server (Overkill for now, but industry standard).

### Streaming
- **[Apache Kafka](https://kafka.apache.org/)** - The backbone of real-time AIOps.
- **[Faust](https://faust.readthedocs.io/en/latest/)** - Python stream processing library (Kafka Streams for Python).

---

## 💡 Pro Tips for SREs

1.  **The "Simple Baseline" Rule:**
    - Before deploying an LSTM Autoencoder, deploy a `Z-Score` check (Mean + 3*Std).
    - If the complex model doesn't beat the simple one, throw it away.

2.  **Alert Routing:**
    - **P1 (Critical):** High Confidence Anomaly (> 0.9) AND Business Metric Impact (Revenue Drop). -> Page Human.
    - **P3 (Warning):** High Confidence Anomaly (> 0.9) BUT No Business Impact (yet). -> Slack Channel / Log Ticket.
    - **P5 (Info):** Low Confidence (< 0.7). -> Dashboard Only.

3.  **Feedback Loops:**
    - Add a "Thumbs Up / Thumbs Down" button to your alerts.
    - If an SRE marks an alert as "False Positive", add that timestamp to a "Ignore List" or retrain the model to suppress it. THIS IS CRITICAL. Without feedback, the model never improves.
