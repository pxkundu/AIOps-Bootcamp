import json
import os
import jwt
from flask import Flask, request, jsonify
from auth_manager import AuthManager
from glean_engine import GleanSecEngine

# --- 🛰️ Managed Connection Point (MCP) Simulator for OpenWeb UI ---

app = Flask(__name__)
auth = AuthManager()

# Link the AIOps discovery engine
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
engine = GleanSecEngine(DATA_DIR)
engine.load_data()
engine.run_discovery()

def redact_for_unauthorized(knowledge_item):
    """
    Simulates redaction: If the user doesn't have permissions, 
    they see the item metadata but the 'content' is hidden or masked.
    """
    redacted = knowledge_item.copy()
    redacted['content'] = "[🔐 REDACTED: Insufficient permissions to view content]"
    return redacted

@app.route('/mcp/v1/discovery', methods=['POST'])
def mcp_discovery_tool():
    """
    Managed Connection Point (MCP) API for OpenWeb UI Integration.
    Forces authentication, extracts identity, and performs ACL-aware search.
    """
    # 1. JWT / Bearer Token Validation
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"status": "error", "message": "Missing or invalid Authorization header"}), 401
    
    token_str = token.split(" ")[1]
    identity = auth.validate_and_get_identity(token_str)
    
    if not identity['valid']:
        return jsonify({"status": "error", "message": "Authentication failed", "details": identity.get("error")}), 403
    
    # 2. Extract Query Params
    payload = request.get_json()
    query = payload.get("query", "").lower()
    
    results = []
    
    # 3. ACL-Aware Search Results
    # We iterate over knowledge objects and check if identity['groups'] can see them.
    # For this simulation, we define some hard-coded target ACLs for specific objects.
    
    acl_mapping = {
        "DOC-101": "SRE",  # Critical production key doc
        "GH-enterprise/analytics-pipeline": "Admins", # Internal code repo
        "SL-2026-03-03T09:15:00Z": "SRE"  # Serious security leak message
    }
    
    for obj in engine.knowledge_base:
        # If query matches or it's a security-related search
        if query in obj['content'].lower() or query in obj['title'].lower():
            target_acl = acl_mapping.get(obj['id'], "Public")
            
            # Use AuthManager to check if the user's groups are allowed
            if auth.check_permission(identity['groups'], target_acl):
                results.append(obj)
            else:
                # Still show in discovery but REDACT content
                results.append(redact_for_unauthorized(obj))
    
    return jsonify({
        "status": "success",
        "user": identity['username'],
        "groups": identity['groups'],
        "results_found": len(results),
        "results": results[:5] # Limit result count for Chat UI performance
    })

@app.route('/mcp/v1/auth', methods=['POST'])
def mock_login():
    """Testing endpoint to get a token for simulation."""
    username = request.get_json().get("username", "alice")
    token = auth.generate_token(username)
    return jsonify({"token": f"Bearer {token}"})

if __name__ == "__main__":
    print("🛰️ MCP Sentry Service (OpenWeb UI Connector) active at http://localhost:5001")
    app.run(debug=True, port=5001)
