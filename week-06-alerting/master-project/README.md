# Master Project: The Alert Sentinel

> **End-to-End AIOps Alerting Platform**

This project consolidates everything we've learned in Week 6:
1. **Deduplication** (Day 1-2)
2. **Correlation** (Day 3)
3. **Topological RCA** (Day 4)
4. **Scoring & Prioritization** (Day 5)

---

## 🏗️ Architecture

The **Alert Sentinel** acts as a middle-layer between monitoring tools (Datadog, Prometheus, Loki) and incident response tools (PagerDuty, Slack).

1. **Ingestion**: Standardizes disparate alert formats into a common JSON schema.
2. **Correlation Engine**: Groups alerts based on a sliding temporal window (Temporal Correlation).
3. **Inference Engine**:
   - Maps alerts to a **Dependency Graph**.
   - Identifies the **Root Cause** by finding the most downstream failing node.
4. **Prioritization**: Ranks incidents by calculating a score derived from node criticality and blast radius.

---

## 🏃 Getting Started

### 1. Requirements
Ensure you have `networkx` and `pandas` installed:
```bash
pip install networkx pandas
```

### 2. File Structure
- `src/data/topology.json`: Defines the system map (LB -> API -> DB -> Storage).
- `src/data/alerts.json`: A simulated stream of alerts representing a hardware failure in the data center.
- `src/aiops_engine.py`: The core logic that processes raw signals into intelligent incidents.

### 3. Run the Simulation
```bash
cd src
python aiops_engine.py
```

---

## 📊 The Scenario: "Storage Array Failure"

In this project, we simulate a hardware failure in `Storage-Array`. 
- **The Symptom**: User sees 500 errors on the `Web-App`.
- **The Noise**: Datadog, Prometheus, and Loki all send alerts.
- **The AIOps Solution**:
   - Sentinel correlates all 4 alerts into **one incident**.
   - Sentinel identifies `Storage-Array` as the root cause.
   - Sentinel assigns a `P0 - CRITICAL` priority.

---

## ✅ Deliverables

- [ ] Successful correlation of multi-tool alerts.
- [ ] Correct root cause identification in a multi-tier dependency chain.
- [ ] Automated prioritization based on blast radius calculation.

---

<p align="center">
  <a href="../day-05-causality/lecture-notes.md">⬅️ Back: Day 5</a> | <strong>Master Project</strong> | <a href="../../week-07-remediation/README.md">Go to Week 7 ➡️</a>
</p>
