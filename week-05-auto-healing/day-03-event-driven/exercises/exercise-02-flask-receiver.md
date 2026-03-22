# Exercise 02: Building a Self-Healing API (Function-as-a-Service)

## 🎯 Objective
Create a localized "FaaS" runner using Flask. Instead of running Python scripts manually, we will trigger them via HTTP requests. This mimics AWS Lambda (Event -> Function).

---

## 🛠️ Step 1: The Receiver (`remediator.py`)

Create a Flask app that listens for incidents.

```python
from flask import Flask, request
import time

app = Flask(__name__)

# Mock Remediation Functions
def restart_nginx():
    print("Stopping Nginx...")
    time.sleep(1)
    print("Starting Nginx...")
    return True

def clear_cache():
    print("Clearing Redis cache...")
    return True

@app.route('/incident', methods=['POST'])
def handle_incident():
    # 1. Parse JSON
    data = request.json
    service = data.get('service')
    issue = data.get('issue')
    
    # 2. Route Logic
    print(f"Received Alert: {service} is {issue}")

    if service == 'nginx' and issue == 'down':
        restart_nginx()
        return {"status": "restarted"}, 200
    elif service == 'redis' and issue == 'full':
        clear_cache()
        return {"status": "cleared"}, 200
    
    return {"status": "unknown_service"}, 400

if __name__ == '__main__':
    app.run(port=5000)
```

## 🛠️ Step 2: The Fire Drill (`fire_drill.py`)

Create a script that triggers the remediator.
1.  Send `POST /incident` with `{"service": "nginx", "issue": "down"}`.
2.  Send `POST /incident` with `{"service": "redis", "issue": "full"}`.

## 📝 Deliverable
Run both. Screenshot the `remediator.py` output showing the "restarting" logs appearing instantly when you run the fire drill.
