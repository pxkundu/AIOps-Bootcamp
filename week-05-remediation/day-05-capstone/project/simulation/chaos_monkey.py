# Aegis Chaos Monkey Simulator
import requests
import time
import random

AEGIS_URL = "http://localhost:5005/webhook"

def simulate_chaos():
    print("🚀 Starting Chaos Simulation...")
    print("Make sure Aegis app.py is running on port 5005!")
    
    events = [
        {"type": "memory_leak", "data": {"service": "webapp", "value": 95}},
        {"type": "security_alert", "data": {"ip": "10.0.0.45", "failed_attempts": 150}},
        {"type": "cpu_spike", "data": {"service": "database", "value": 99}}, # Will be ignored if hour is 2-4
        {"type": "capacity_breach", "data": {"service": "api_gateway", "rps": 5000}},
        {"type": "strange_log", "data": {"message": "Something weird happened"}} # Escalation test
    ]
    
    while True:
        # Choose a random failure
        event = random.choice(events)
        
        print(f"\n[CHAOS] Injecting fault: {event['type']}")
        
        try:
            resp = requests.post(AEGIS_URL, json=event, timeout=2)
            print(f"[CHAOS] Aegis Response: {resp.json().get('action_taken')}")
        except Exception as e:
            print(f"[CHAOS] Error connecting to Aegis: {e}")
            break
            
        # Wait for the next disaster
        wait_time = random.randint(3, 7)
        print(f"[CHAOS] Next fault in {wait_time} seconds...")
        time.sleep(wait_time)

if __name__ == "__main__":
    simulate_chaos()
