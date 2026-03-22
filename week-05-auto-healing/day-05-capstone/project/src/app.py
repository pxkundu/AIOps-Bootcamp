# Aegis Webhook Gateway
from flask import Flask, request, jsonify
from project.src.engine import AegisEngine
import os

app = Flask(__name__)
engine = AegisEngine()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Aegis is online"}), 200

@app.route('/webhook', methods=['POST'])
def handle_event():
    """
    Interface for Prometheus Alerts / Custom Metrics.
    """
    if not request.is_json:
        return jsonify({"error": "Invalid payload"}), 400
    
    event = request.json
    
    # 1. Triage & Heal
    result = engine.triage_and_heal(event)
    
    # 2. Audit
    engine.audit(result)
    
    return jsonify({
        "status": "event_processed",
        "action_taken": result
    }), 200

if __name__ == '__main__':
    print("🛡️  Aegis Gateway listening on port 5005...")
    app.run(port=5005)
