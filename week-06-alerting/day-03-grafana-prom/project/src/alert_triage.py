"""
The Self-Adjusting Sentinel: Alert Triage Helper
This script queries the Prometheus API to validate if a firing alert meets 
advanced statistical criteria (Z-Score) before escalating to a human.
"""

import requests
import time
import os

PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")

def calculate_z_score(metric_query, window_1m="5m", window_history="1h"):
    """
    Manually calculates the Z-Score of a metric using the Prometheus API.
    A Z-Score > 3 means the data point is a extreme outlier.
    """
    # 1. Get Current Value
    current_resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': metric_query})
    current_val = float(current_resp.json()['data']['result'][0]['value'][1])

    # 2. Get Mean of History
    mean_query = f"avg_over_time(({metric_query})[{window_history}:{window_1m}])"
    mean_resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': mean_query})
    mean_val = float(mean_resp.json()['data']['result'][0]['value'][1])

    # 3. Get StdDev of History
    stddev_query = f"stddev_over_time(({metric_query})[{window_history}:{window_1m}])"
    stddev_resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': stddev_query})
    stddev_val = float(stddev_resp.json()['data']['result'][0]['value'][1])

    # 4. Math: Z = (Current - Mean) / StdDev
    if stddev_val == 0: return 0
    z_score = (current_val - mean_val) / stddev_val
    return z_score

def triage_active_alerts():
    print(f"🕵️ Scanning Prometheus Alerts at {PROMETHEUS_URL}...")
    try:
        resp = requests.get(f"{PROMETHEUS_URL}/api/v1/alerts")
        alerts = resp.json()['data']['alerts']
        
        if not alerts:
            print("✅ No firing alerts. System is quiet.")
            return

        for alert in alerts:
            if alert['state'] == 'firing':
                name = alert['labels']['alertname']
                print(f"\n📢 Firing Alert: {name}")
                
                # If it's a latency alert, we perform an AIOps deep dive
                if "Latency" in name:
                    # Example metric query for the specific instance
                    instance = alert['labels'].get('instance', '')
                    metric = f'rate(http_request_duration_seconds_sum{{instance="{instance}"}}[5m]) / rate(http_request_duration_seconds_count{{instance="{instance}"}}[5m])'
                    
                    z = calculate_z_score(metric)
                    print(f"   [AIOPS ANALYSIS] Z-Score for this instance: {z:.2f}")
                    
                    if abs(z) > 3:
                        print("   🔴 CRITICAL: This is a 1-in-1000 event. Escalate IMMEDIATELY.")
                    elif abs(z) > 2:
                        print("   🟡 WARNING: Significant deviation. Keep an eye on it.")
                    else:
                        print("   🟢 NOISE: Statistical variation is low. Likely a false positive.")

    except Exception as e:
        print(f"❌ Error connecting to Prometheus: {e}")

if __name__ == "__main__":
    triage_active_alerts()
