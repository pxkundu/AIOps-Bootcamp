# Week 5: Predictive Analytics & Forecasting

> **Theme:** Predicting problems before they impact users

---

## 🎯 Learning Objectives

By the end of this week, you will:

1. Implement time-series forecasting with ARIMA and Prophet
2. Build SLA breach prediction models
3. Apply deep learning to time-series (LSTM/Transformer)
4. Create multi-variate forecasting systems

---

## 📅 Daily Schedule

| Day | Topic | Duration |
|-----|-------|----------|
| 1-2 | [Time-Series Forecasting](day-01-forecasting/) | 8 hours |
| 3-4 | [Failure Prediction](day-02-failure-prediction/) | 8 hours |
| 5-6 | [Deep Learning for Time-Series](day-03-deep-learning/) | 8 hours |
| 7 | [Multi-variate Forecasting](day-04-multivariate/) | 4 hours |

---

## 🛠️ Technologies Covered

- **Prophet** - Facebook's forecasting library
- **statsmodels** - ARIMA implementation
- **TensorFlow/PyTorch** - LSTM, Transformer models
- **pandas** - Time-series manipulation

---

## ✅ Deliverables

- [ ] Capacity forecasting model with Prophet
- [ ] SLA breach prediction system
- [ ] Multi-metric correlation dashboard
- [ ] Week 5 quiz completed

---

## 🔑 Key Concepts

### Forecasting Use Cases in AIOps
| Use Case | Model | Benefit |
|----------|-------|---------|
| Capacity planning | Prophet | Scale before peak |
| SLA prediction | Classification | Alert before breach |
| Disk space | Linear/Prophet | Prevent outages |
| Traffic prediction | LSTM | Proactive scaling |

### Model Selection
```
Simple trends → ARIMA/ETS
Seasonal data → Prophet, SARIMA  
Complex patterns → LSTM, Transformer
Multiple correlated series → VAR, Graph Neural Networks
```

---

<p align="center">
  <a href="../week-04-anomaly-detection/">← Week 4</a> | <a href="day-01-forecasting/">Start Week 5 →</a> | <a href="../week-06-alerting/">Week 6 →</a>
</p>
