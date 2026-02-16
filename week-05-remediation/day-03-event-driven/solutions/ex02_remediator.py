# Solution for Exercise 02: Self-Healing Flask API
# Week 5 Day 3

from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# --- Mock Remediation Functions ---
def restart_nginx():
    print("[ACTION] Stopping Nginx...")
    time.sleep(1)
    print("[ACTION] Starting Nginx...")
    return True

def clear_redis():
    print("[ACTION] Executing FLUSHALL on Redis...")
    return True

# --- The Webhook Handler ---
@app.route('/incident', methods=['POST'])
def handle_incident():
    data = request.json
    service = data.get('service')
    issue = data.get('issue')
    
    print(f"\n[ALERT] Received: {service} is {issue}")

    if service == 'nginx' and issue == 'down':
        restart_nginx()
        return jsonify({"status": "restarted", "severity": "high"}), 200
        
    elif service == 'redis' and issue == 'full':
        clear_redis()
        return jsonify({"status": "cleared", "severity": "medium"}), 200
    
    return jsonify({"status": "unknown_service", "message": "No playbook found"}), 400

if __name__ == '__main__':
    print("Starting Remediator on port 5000...")
    app.run(port=5000)
