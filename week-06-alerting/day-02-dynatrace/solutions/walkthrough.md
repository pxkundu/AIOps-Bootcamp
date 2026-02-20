# Project Solution: The Root Cause Detective Walkthrough

This guide explains how to use the code and the Dynatrace environment to prove that Davis AI can find the root cause of an outage.

---

## 🛠️ 1. Environmental Setup

Export your credentials:
```bash
export DT_TENANT_URL="https://xxx12345.live.dynatrace.com"
export DT_API_TOKEN="dt0c01.XXXXXXXX.XXXXXXXX"
```

Install requirements:
```bash
pip install requests
```

---

## 🏗️ 2. Step 1: Identifying a Target

Before you can "attack" your system, you need to know what to attack.
1.  Run the **Problem Analyzer** to see what's currently happening:
    ```bash
    python project/src/problem_analyzer.py
    ```
2.  In the Dynatrace UI, navigate to **Services**. Find your Azure App Service and copy its **Entity ID** (e.g., `SERVICE-AB12345`).

---

## 📉 3. Step 2: Triggering the Root Cause

Now, simulate a "Bad Config Deployment":
```bash
python project/src/chaos_injector.py
# Enter your Entity ID when prompted.
```

**What is happening?**
We are pushing a metadata event to Dynatrace at precisely this timestamp. Within 3-5 minutes, Davis AI will notice a performance drop and look for events at that time.

---

## 🕵️ 4. Step 3: Detecting the Detective

Run the analyzer again:
```bash
python project/src/problem_analyzer.py
```

**Expected Result:**
If Davis has completed its analysis, the script will output:
`💡 ROOT CAUSE IDENTIFIED: [AIOps Bootcamp: Bad Config Deploy]`

**The Intelligence:**
Instead of telling you "The Web App is slow" (a symptom), Davis tells you "The Web App is slow **BECAUSE** of the Configuration Change event you pushed."

---

## 📊 5. Step 4: Deploying the Serverless Triage Dashboard (DQL)

For modern AWS Serverless stacks, we use **DQL (Dynatrace Query Language)** to correlate cross-account Lambda and API Gateway health.

1.  Run the **Dashboard Builder**:
    ```bash
    python project/src/dashboard_dql.py
    ```
2.  **What is being created?**
    - **Tile 1:** Lambda Invocations vs. Errors per function.
    - **Tile 2:** P95 Latency hotspots in API Gateway.
    - **Tile 3:** Failure heatmap for serverless entities using **Grail** data.

---

## 🛡️ 6. Comparison: Datadog vs. Dynatrace

| Feature | Datadog (Day 1) | Dynatrace (Day 2) |
|---|---|---|
| **AI Type** | Probabilistic (Patterns) | Deterministic (Topology) |
| **Alerting** | Anomaly Detection | Causal Problem Analysis |
| **RCA** | Human analyzes Dashboards | Davis points to the Entity/Event |
| **Best For** | Metrics, Logs, Observability | Complex Microservices, Code-level RCA |
