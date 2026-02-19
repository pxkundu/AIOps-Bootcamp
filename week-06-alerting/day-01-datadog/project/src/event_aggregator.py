"""
The Noise Canceller: Event Aggregator
This script demonstrates how to correlate raw Datadog events into a single logical incident.
It groups alerts by 'service' and 'env' within a specific time window.
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
import time
import os

def correlate_events():
    configuration = Configuration()
    
    with ApiClient(configuration) as api_client:
        api_instance = EventsApi(api_client)
        
        # 1. Fetch alerts from the last 1 hour
        now = int(time.time())
        start = now - 3600
        
        try:
            # Query for alert events with specific project tag
            api_response = api_instance.list_events(
                start=start,
                end=now,
                tags="project:noise-canceller,status:error"
            )
            
            events = api_response.events
            print(f"Captured {len(events)} individual alert events.")
            
            # 2. Correlation Business Logic
            # We group by 'service' tag to turn 10 web-server alerts into 1 logical incident
            incidents = {}
            for event in events:
                # Extract service tag
                tags = event.get('tags', [])
                service_tag = next((t.split(':')[1] for t in tags if t.startswith('service:')), 'unknown')
                
                if service_tag not in incidents:
                    incidents[service_tag] = []
                incidents[service_tag].append(event['title'])
                
            # 3. Output Aggregated View
            print("\n--- Intelligent Incident Summary ---")
            if not incidents:
                print("No correlated incidents found. System is healthy.")
            
            for service, alerts in incidents.items():
                print(f"🔥 INCIDENT: Service [{service.upper()}] has {len(alerts)} firing monitors.")
                print(f"   Primary Symptom: {alerts[0]}")
                print(f"   Action: Suppressing {len(alerts)-1} redundant alerts. Notify SRE On-Call.")
                
        except Exception as e:
            print(f"Exception when fetching events: {e}")

if __name__ == "__main__":
    if not os.environ.get('DD_API_KEY') or not os.environ.get('DD_APP_KEY'):
        print("ERROR: Please set DD_API_KEY and DD_APP_KEY environment variables.")
    else:
        correlate_events()
