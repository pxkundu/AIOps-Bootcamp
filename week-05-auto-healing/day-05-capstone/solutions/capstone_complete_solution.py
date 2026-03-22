# COMPLETE CAPSTONE SOLUTION: SYSTEM AEGIS
# Includes Gateway, Integrated Triage, Circuit Breakers, and Verification.

from flask import Flask, request, jsonify
import time
import datetime
import threading

app = Flask(__name__)

class UnifiedAegis:
    def __init__(self):
        self.stats = {"healed": 0, "failed": 0, "broken": 0}
        self.circuit_counts = {}
        self.RETRY_LIMIT = 2

    def process_incident(self, event):
        etype = event.get('type')
        service = event.get('data', {}).get('service', 'unknown')
        
        # 1. Circuit Breaker Check
        count = self.circuit_counts.get(service, 0)
        if count >= self.RETRY_LIMIT:
            self.stats["broken"] += 1
            return "CIRCUIT_BROKEN"

        # 2. Context Triage (Simple Decision Tree)
        print(f"\n[AEGIS] Incident: {etype} on {service}")
        
        # 3. Execution & Verification
        if etype == "memory_leak":
            success = self.healer_and_verify(service, "restart")
            if success:
                self.circuit_counts[service] = 0 # Reset on success
                self.stats["healed"] += 1
                return "HEALED"
            else:
                self.circuit_counts[service] = count + 1
                self.stats["failed"] += 1
                return "FAIL_VERIFICATION"

        return "UNHANDLED"

    def healer_and_verify(self, service, action):
        print(f"  [EXEC] Running {action} on {service}...")
        time.sleep(0.5)
        
        # Post-action verification
        print(f"  [VERIFY] Checking {service} status...")
        # Simulate a 80% success rate
        import random
        return random.random() > 0.2

aegis = UnifiedAegis()

@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.json
    outcome = aegis.process_incident(event)
    return jsonify({"outcome": outcome, "stats": aegis.stats})

if __name__ == '__main__':
    print("🛡️ Aegis Master Solution running on port 5005...")
    app.run(port=5005)
