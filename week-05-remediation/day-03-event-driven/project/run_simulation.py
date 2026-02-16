# Simulation Script for Week 5 Day 3: The Reactor
# This script sends 10 mock events to your Flask API.

import requests
import time
import uuid

API_URL = "http://localhost:5000/events"

def fire_events():
    print(f"[SIMULATION] Connecting to {API_URL}...")
    
    # 10 Test Cases
    events = [
        {"type": "server.down", "source": "cloudwatch", "data": {"id": "i-12345"}},
        {"type": "security.bruteforce", "source": "guardduty", "data": {"ip": "192.168.1.50"}},
        {"type": "db.latency", "source": "prometheus", "data": {"service": "users-db"}},
        {"type": "server.down", "source": "cloudwatch", "data": {"id": "i-67890"}},
        {"type": "unknown.event", "source": "chaos", "data": {"foo": "bar"}}, # Should return 200 (Ignored) but handle gracefully
        {"type": "security.ssh_login", "source": "auth.log", "data": {"user": "root"}},
        {"type": "app.crash", "source": "sentry", "data": {"app": "frontend"}},
        {"type": "disk.full", "source": "datadog", "data": {"mount": "/var/log"}},
        {"type": "server.down", "source": "cloudwatch", "data": {"id": "i-99999"}},
        {"type": "scaling.needed", "source": "k8s", "data": {"deployment": "api-gateway"}}
    ]
    
    success_count = 0
    start_time = time.time()
    
    for i, event in enumerate(events):
        # CloudEvents Spec (simplified)
        payload = {
            "specversion": "1.0",
            "id": str(uuid.uuid4()),
            "type": event["type"],
            "source": event["source"],
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "data": event["data"]
        }
        
        try:
            print(f"[{i+1}/10] Sending {event['type']}...")
            resp = requests.post(API_URL, json=payload, timeout=0.1) # 100ms timeout!
            
            if resp.status_code == 200:
                print(f"  ✅ Accepted (Lat: {resp.elapsed.total_seconds()*1000:.1f}ms)")
                success_count += 1
            else:
                print(f"  ❌ Error: {resp.status_code}")
                
        except requests.exceptions.Timeout:
            print("  ❌ Timeout (>100ms)")
        except requests.exceptions.ConnectionError:
            print("  ❌ Connection Refused (Is Flask running?)")
            break
            
    # Summary
    duration = time.time() - start_time
    print("-" * 30)
    print(f"Results: {success_count}/10 Successful Events handled.")
    print(f"Total Time: {duration:.2f}s")
    
    if success_count >= 9:
        print("🏆 Reactor Stability: 90%+. Certified.")
    else:
        print("💀 Reactor Unstable. Optimize your handlers.")

if __name__ == "__main__":
    fire_events()
