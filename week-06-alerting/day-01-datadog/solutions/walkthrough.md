# Project Solution: The Noise Canceller Walkthrough

This guide explains how to verify the end-to-end solution for Intelligent Alerting in Datadog.

---

## 🛠️ 1. Environmental Setup

Ensure you have your Datadog keys exported:
```bash
export DD_API_KEY="your_api_key"
export DD_APP_KEY="your_app_key"
```

Install dependencies:
```bash
pip install -r project/requirements.txt
```

---

## 🏗️ 2. Step 1: Deploying the Intelligent Monitor

Run the monitor manager to create your first anomaly detection rule:
```bash
python project/src/monitor_manager.py
```
**What happens?** 
The script calls the Datadog API and creates a monitor named `[AIOps] EC2 CPU Anomaly Detection`. 
Instead of a flat line at 90%, you will see a shaded "Expected Range" in the Datadog UI. This range is calculated by the `agile` ML algorithm based on the last 4 hours of data.

---

## 📉 3. Step 2: Correlating "Chaos"

In a real scenario, you would launch an AWS EC2 instance and run a stress test to trigger an anomaly. 
*   **Manual Trigger:** You can simulate this by tagging any existing monitor with `project:noise-canceller` and forcing it into an alert state.

Run the aggregator to see the "Intelligence" in action:
```bash
python project/src/event_aggregator.py
```
**Expected Output:**
If multiple EC2 instances in your `checkout` service are spiking, the script will show:
`🔥 INCIDENT: Service [CHECKOUT] has 12 firing monitors.`
`   Action: Suppressing 11 redundant alerts. Notify SRE On-Call.`

This demonstrates how we turn **Alert Fatigue** (12 emails) into **Actionable Data** (1 incident).

---

## 🛡️ 4. Resilience Check (The "Why")

Why is this better than CloudWatch Alarms?
1.  **Seasonality:** If your CPU spikes every day at 12:00 PM because of a scheduled job, Datadog's anomaly detection learns this as "Normal". A static CloudWatch alarm would wake you up every night at 12:00 PM.
2.  **Service Context:** CloudWatch sees "Instances". The Noise Canceller sees "The Checkout Service".
