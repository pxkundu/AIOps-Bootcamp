"""
The Root Cause Detective: Chaos Event Injector
This script pushes a 'Custom Event' to Dynatrace to simulate a failure (e.g., a bad deployment or config change).
This allows Davis AI to correlate the event with performance drops.
"""

import requests
import os
import time

def inject_chaos_event(entity_id):
    """
    Push a 'Configuration Change' event to a specific entity (e.g., an Azure App Service).
    entity_id: The Dynatrace ID of the component (e.g., PROCESS_GROUP_INSTANCE-123)
    """
    tenant = os.environ.get('DT_TENANT_URL').rstrip('/')
    token = os.environ.get('DT_API_TOKEN')
    
    url = f"{tenant}/api/v2/events/ingest"
    
    headers = {
        "Authorization": f"Api-Token {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "eventType": "CUSTOM_CONFIGURATION_CHANGE",
        "title": "AIOps Bootcamp: Bad Config Deploy",
        "properties": {
            "pushed_by": "Aegis-Simulator",
            "fix_action": "Rollback to v1.2",
            "description": "Simulated misconfiguration causing high latency."
        },
        "entitySelector": f"type(SERVICE),entityId({entity_id})"
    }

    print(f"🚀 Injecting Chaos Event into {entity_id}...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("✅ Event successfully ingested. Davis AI will now correlate this.")
    else:
        print(f"❌ Failed to ingest event: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if not os.environ.get('DT_TENANT_URL') or not os.environ.get('DT_API_TOKEN'):
        print("ERROR: Environment variables missing.")
        exit(1)
        
    # Example Entity ID - in a real lab, get this from the Entity API
    TARGET = input("Enter the Dynatrace Entity ID for the service to attack (e.g. SERVICE-12345): ").strip()
    inject_chaos_event(TARGET)
