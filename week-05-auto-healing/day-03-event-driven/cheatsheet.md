# Remediation Cheat Sheet: Webhooks & FaaS

> **Libraries:** `Flask`, `requests`, `boto3` (AWS SDK)
> **Protocols:** HTTP POST, JSON

---

## 🎣 Building a Simple Webhook Receiver (Flask)

Run this locally to catch events.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_event():
    # 1. Verify JSON Payload
    if not request.is_json:
        return jsonify({"error": "Expected JSON"}), 400
        
    data = request.json
    print(f"Received Event: {data}")
    
    # 2. Extract Key Info
    event_type = data.get('event_type')
    
    # 3. Route Logic
    if event_type == 'server_crash':
        # run_recovery_script()
        return jsonify({"status": "recovering"}), 200
    
    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 🚀 Sending an Event (The Trigger)

Simulate a CloudWatch Alarm or GitHub Push.

```python
import requests
import time

payload = {
    "event_type": "server_crash",
    "server_id": "i-12345abcdef",
    "timestamp": time.time()
}

# Fire and Forget
try:
    requests.post('http://localhost:5000/webhook', json=payload, timeout=1)
    print("Event sent!")
except requests.exceptions.ConnectionError:
    print("Receiver is down!")
```

---

## ☁️ AWS Lambda Template (Python)

Standard signature for FaaS.

```python
import json

def lambda_handler(event, context):
    """
    AWS passes JSON event automatically.
    """
    print("Received event: " + json.dumps(event))
    
    # Extract
    if 'Records' in event: # S3/SQS usually wraps in 'Records'
        for record in event['Records']:
            process_record(record)
            
    # Return (API Gateway expects this format)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

---

## 🔒 Security: Verify HMAC Signature

Don't let hackers trigger your restart script. (GitHub style).

```python
import hmac
import hashlib

def verify_signature(secret, payload, signature_header):
    # Compute SHA256 of payload using secret key
    computed = hmac.new(
        key=secret.encode(), 
        msg=payload, 
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Secure Compare (prevents timing attacks)
    return hmac.compare_digest(f"sha256={computed}", signature_header)
```
