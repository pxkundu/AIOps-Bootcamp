"""
MCP Action Server — Managed Connection Point for Glean-powered observability.
Implements read/write/execute actions against PagerDuty and Jira (simulated).
Based on: https://docs.glean.com/connectors/configure-actions-in-datasource/config-actions-mcp-from-datasource
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# --- Simulated External State ---
pagerduty_incidents = {
    "INC-001": {"title": "DB Latency > 500ms", "status": "triggered", "severity": "P1"},
    "INC-002": {"title": "Memory pressure on worker-node-03", "status": "acknowledged", "severity": "P2"},
}

jira_tickets = {}
action_audit_log = []


def log_action(user, action, target, result):
    """Log every MCP action for compliance and audit."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "action": action,
        "target": target,
        "result": result,
    }
    action_audit_log.append(entry)
    print(f"📋 AUDIT: {json.dumps(entry)}")


# ============================================================
# MCP TOOLS (Native Action Pack + Custom)
# ============================================================

@app.route("/mcp/v1/tools", methods=["GET"])
def list_tools():
    """List all available MCP tools (per Glean actions catalog)."""
    tools = [
        {
            "name": "list_incidents",
            "description": "List all PagerDuty incidents with current status.",
            "type": "read",
            "source": "PagerDuty",
        },
        {
            "name": "acknowledge_incident",
            "description": "Acknowledge a PagerDuty incident by ID.",
            "type": "write",
            "source": "PagerDuty",
            "parameters": {"incident_id": "string"},
            "requires_confirmation": True,
        },
        {
            "name": "resolve_incident",
            "description": "Resolve a PagerDuty incident by ID.",
            "type": "write",
            "source": "PagerDuty",
            "parameters": {"incident_id": "string"},
            "requires_confirmation": True,
        },
        {
            "name": "create_jira_ticket",
            "description": "Create a Jira issue for RCA tracking.",
            "type": "write",
            "source": "Jira",
            "parameters": {"summary": "string", "description": "string", "priority": "string"},
            "requires_confirmation": True,
        },
        {
            "name": "get_audit_log",
            "description": "Retrieve the full MCP action audit trail.",
            "type": "read",
            "source": "System",
        },
    ]
    return jsonify({"tools": tools, "count": len(tools)})


@app.route("/mcp/v1/execute", methods=["POST"])
def execute_tool():
    """Execute an MCP tool action."""
    payload = request.get_json()
    tool = payload.get("tool")
    params = payload.get("parameters", {})
    user = payload.get("user", "anonymous")
    confirmed = payload.get("confirmed", False)

    # --- READ ACTIONS ---
    if tool == "list_incidents":
        log_action(user, "list_incidents", "PagerDuty", "success")
        return jsonify({"status": "success", "incidents": pagerduty_incidents})

    if tool == "get_audit_log":
        return jsonify({"status": "success", "audit_log": action_audit_log})

    # --- WRITE ACTIONS (Human-in-the-loop) ---
    if tool == "acknowledge_incident":
        inc_id = params.get("incident_id")
        if inc_id not in pagerduty_incidents:
            return jsonify({"status": "error", "message": f"Incident {inc_id} not found"}), 404

        if not confirmed:
            return jsonify({
                "status": "confirmation_required",
                "message": f"⚠️ Please confirm: Acknowledge incident '{pagerduty_incidents[inc_id]['title']}'?",
                "action": "acknowledge_incident",
                "target": inc_id,
            })

        pagerduty_incidents[inc_id]["status"] = "acknowledged"
        log_action(user, "acknowledge_incident", inc_id, "success")
        return jsonify({"status": "success", "message": f"Incident {inc_id} acknowledged."})

    if tool == "resolve_incident":
        inc_id = params.get("incident_id")
        if inc_id not in pagerduty_incidents:
            return jsonify({"status": "error", "message": f"Incident {inc_id} not found"}), 404

        if not confirmed:
            return jsonify({
                "status": "confirmation_required",
                "message": f"⚠️ Please confirm: Resolve incident '{pagerduty_incidents[inc_id]['title']}'?",
            })

        pagerduty_incidents[inc_id]["status"] = "resolved"
        log_action(user, "resolve_incident", inc_id, "success")
        return jsonify({"status": "success", "message": f"Incident {inc_id} resolved."})

    if tool == "create_jira_ticket":
        if not confirmed:
            return jsonify({
                "status": "confirmation_required",
                "message": f"⚠️ Confirm: Create Jira ticket '{params.get('summary')}'?",
            })

        ticket_id = f"JIRA-{4521 + len(jira_tickets)}"
        jira_tickets[ticket_id] = {
            "summary": params.get("summary"),
            "description": params.get("description"),
            "priority": params.get("priority", "High"),
            "status": "Open",
            "created_by": user,
        }
        log_action(user, "create_jira_ticket", ticket_id, "success")
        return jsonify({"status": "success", "ticket_id": ticket_id, "message": f"Jira ticket {ticket_id} created."})

    return jsonify({"status": "error", "message": f"Unknown tool: {tool}"}), 400


if __name__ == "__main__":
    print("🛰️ MCP Action Server running at http://localhost:5002")
    print("📋 Available tools: GET /mcp/v1/tools")
    print("⚡ Execute actions: POST /mcp/v1/execute")
    app.run(debug=True, port=5002)
