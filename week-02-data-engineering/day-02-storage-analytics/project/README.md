# Day 2 Project: Log Sentinel - The AIOps Performance & Security Dashboard

> **Objective:** Build a unified monitoring solution that utilizes Elasticsearch's analytical power to detect performance bottlenecks and security anomalies.

---

## 🎯 Project Scenario
You have been hired by **CloudSecure Inc.** Their main payment gateway is experiencing intermittent latency and suspicious login attempts. They have a high-volume log stream but no way to see the "Big Picture." 

Your task is to build a **Sentinel Dashboard** that automatically highlights issues using Logstash for enrichment and Kibana for visualization.

---

## 🏗️ Architecture

1. **Log Source:** A Python simulator generating global payment logs.
2. **Buffer:** Kafka (optional, can go direct to Logstash for simplicity in this lab).
3. **Engine:** Logstash (for GeoIP and User-Agent parsing).
4. **Storage:** Elasticsearch (Indexing).
5. **UI:** Kibana (Discovery & Visuals).

---

## 📋 Requirements

### 1. Data Enrichment Pipeline
Your Logstash configuration must:
- [ ] Correctly parse the JSON log stream.
- [ ] Add **GeoIP** metadata based on the `client_ip`.
- [ ] Use a **Conditional** to tag any log with `latency > 2000` as `high_latency`.
- [ ] Use a **Fingerprint** or **UUID** filter to ensure all events have a unique ID.

### 2. The Sentinel Dashboard (Kibana)
Create a dashboard with the following 4 visualizations:

1. **The Global Threat Map:** A coordinate map showing where current transactions are originating.
2. **Latency Heatmap:** Visualize `latency` over time. Highlight the "red zones."
3. **Top Culprits Table:** A table showing the top 5 `client_ips` generating 5xx errors.
4. **Status Breakdown:** A pie chart of HTTP status code distribution (2xx, 4xx, 5xx).

### 3. AIOps Insight Challenge
Using **Kibana Lens**, create a formula that calculates:
`Percentage of High Latency Requests = (count(high_latency) / total_count) * 100`

---

## 🛠️ Implementation Steps

### Step 1: The Simulator
Create `payment_sim.py`:
- Use `faker` or a simple randomizer to generate IPs from different countries.
- Randomly inject "Spikes" where latency jump to 5000ms for 30 seconds.
- Randomly inject "Error Bursts" from a specific IP (simulating a DDoS).

### Step 2: Logstash Configuration
Ensure your pipeline is robust. What happens if a log is missing the IP? (Use `if [client_ip]`).

### Step 3: Index Management
Set a mapping in Elasticsearch so that `latency` is a `float` and `geo.location` is a `geo_point`. 

---

## ✅ Evaluation Rubric

| Criteria | Points |
|----------|--------|
| **Enrichment:** GeoIP is working (Map shown in Kibana). | 30 |
| **Logic:** `high_latency` tags are correctly applied. | 20 |
| **UX:** Dashboard is intuitive and uses proper colors (Red for errors). | 25 |
| **Performance:** Indexing mapping is optimized (no "text" fields where "keyword" should be). | 15 |
| **Bonus:** Use a Scripted Field in Kibana to normalize data. | 10 |

---

## 📤 Submission
Submit your `docker-compose.yml`, `logstash.conf`, and screenshots of your 4 Kibana visualizations.
