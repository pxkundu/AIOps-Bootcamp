"""
The Noise Canceller: Webhook Enrichment Service
This service receives alert payloads from Datadog and 'enriches' them with 
Infrastructure context (e.g., AWS Metadata) before notifying SREs.
"""

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Mock AWS Metadata enrichment
def get_aws_context(host_name):
    """
    In production, this would call 'boto3.client('ec2').describe_instances()'
    """
    print(f"🔍 Fetching AWS Metadata for {host_name}...")
    return {
        "instance_type": "m5.large",
        "region": "us-east-1",
        "launch_time": "2023-10-24 08:00:00",
        "tags": {"cost_center": "checkout-api"}
    }

@app.route('/alert', methods=['POST'])
def handle_datadog_alert():
    # 1. Parse Datadog Webhook Payload
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    alert_id = data.get('id')
    alert_title = data.get('event_title', 'Unknown Alert')
    host = data.get('host', 'unknown-host')
    
    print(f"\n📢 [ALERT RECEIVED] ID: {alert_id} | Title: {alert_title}")

    # 2. AIOps Enrichment Step
    # We add context that Datadog might not have in the brief alert payload
    context = get_aws_context(host)
    
    # 3. Aggregated Response Logic
    # In a full system, you would send this to Slack or PagerDuty
    enriched_message = {
        "incident": alert_title,
        "host_metadata": context,
        "action_taken": "Logged to Triage Dashboard",
        "severity": "CRITICAL" if "Anomaly" in alert_title else "WARNING"
    }
    
    print(f"✅ Alert Enriched: {enriched_message}")
    
    return jsonify({"status": "success", "enriched_data": enriched_message}), 200

if __name__ == '__main__':
    # Run on port 8080 - remember to expose this if using Ngrok for real Datadog connectivity
    print("🛡️  Aegis Enrichment Service listening on port 8080...")
    app.run(port=8080)
