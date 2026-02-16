# Solution for Project App: The Reactor Router
# Week 5 Day 3

from flask import Flask, request, jsonify
import project_handlers as handlers
import hmac
import hashlib

app = Flask(__name__)
SECRET_KEY = "super_secret_key"

def verify_signature(payload, signature):
    """
    Optional: Verifies HMAC SHA256 signature for security.
    """
    computed = hmac.new(
        key=SECRET_KEY.encode(), 
        msg=payload, 
        digestmod=hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={computed}", signature)

@app.route('/events', methods=['POST'])
def receive_event():
    # 1. Validate Content Type
    if not request.is_json:
        return jsonify({"error": "Expected JSON payload"}), 400
        
    # 2. Check Security (Optional Twist)
    signature = request.headers.get('X-Hub-Signature-256')
    if signature:
        if not verify_signature(request.data, signature):
            return jsonify({"error": "Invalid Signature"}), 403
            
    # 3. Parse CloudEvents Structure
    event = request.json
    specversion = event.get('specversion')
    if specversion != "1.0":
        return jsonify({"error": "Unsupported CloudEvents Version"}), 400
        
    event_type = event.get('type')
    data = event.get('data', {})
    
    print(f"\n[RECEIVED] {event_type} from {event.get('source')}")
    
    # 4. Route to Handler (The "Switch" Statement)
    try:
        if event_type == "server.down":
            handlers.restart_server(data.get('id'))
            
        elif event_type == "security.bruteforce":
            handlers.block_ip(data.get('ip'))
            
        elif event_type == "scaling.needed":
            handlers.scale_deployment(data.get('deployment'))
            
        else:
            # Unknown event -> Log it but return 200 (Don't crash the sender)
            handlers.log_audit(event_type, event.get('source'))
            
        return jsonify({"status": "processed"}), 200
        
    except Exception as e:
        print(f"[ERROR] Handler crashed: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    print(f"Reactor Online. Routing events...")
    app.run(port=5000)
