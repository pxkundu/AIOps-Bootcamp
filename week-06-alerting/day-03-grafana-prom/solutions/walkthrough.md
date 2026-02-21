# Project Solution: The Self-Adjusting Sentinel Walkthrough

This guide explains how to deploy and test the Intelligent Alerting system using Prometheus and Grafana.

---

## 🛠️ 1. Environmental Setup

1.  **Deploy the K8s Stack**: Follow the steps in `project/infrastructure/k8s_setup.md` to install Prometheus and Grafana.
2.  **Port-Forward Services**:
    - Prometheus: `localhost:9090`
    - Grafana: `localhost:3000`

---

## 🏗️ 2. Step 1: Deploying the Dynamic Rules

Normally, you would add these rules to your Prometheus `values.yaml` in Helm. For a quick test:
1.  Access the Prometheus UI.
2.  Paste the PromQL from `project/src/alert_rules.yaml` into the expression browser.
3.  Observe the "Confidence Bands" being calculated.

---

## 📊 3. Step 2: Importing the AIOps Dashboard

1.  Log in to **Grafana** (admin/prom-operator).
2.  Go to **Dashboards** -> **Import**.
3.  Paste the content of `project/src/sentinel_dashboard.json`.
4.  **Observation:** You will see your latency metric plotted alongside a "Upper" and "Lower" band.
    - If the line stays inside the bands, it's **Normal**.
    - If it breaks the band, it's an **Anomaly**.

---

## 🕵️ 4. Step 3: Statistical Triage (The "AIOps" Layer)

When an alert fires in Prometheus, use the Python triage script to validate it:
```bash
export PROMETHEUS_URL="http://localhost:9090"
python project/src/alert_triage.py
```

**Scenario:**
- **Static Alert:** Fired because latency > 500ms.
- **Sentinel Analysis:** Checks the Z-Score. If the historical average was 450ms, the Z-Score will be low (< 1). The script will label this as `🟢 NOISE`.
- **The Result:** You saved a human from being paged for a minor variance.

---

## 🛡️ 5. Statistical Pattern Comparison

| Method | Threshold Type | Benefit | Risk |
|---|---|---|---|
| **Static** | Manual (e.g., > 100) | Easy to understand | High Noise; Doesn't adapt |
| **Z-Score** | Statistical (Mean + 3SD) | Adapts to variance | Cold Start (needs history) |
| **Forecasting** | Predictive (`predict_linear`) | Proactive Alerting | False trends in volatile data |

**Conclusion:** Use **Static** alerts for binary failures (Server Down). Use **Sentinel/Dynamic** alerts for performance and traffic (Latency, RPS).
