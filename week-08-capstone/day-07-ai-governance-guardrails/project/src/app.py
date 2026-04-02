"""
AI Governance Control Plane — Flask API
All LLM-bound traffic should pass through this layer for policy + audit.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, request

from audit_logger import append_event, read_recent_events
from guardrails import evaluate_input, evaluate_output
from llm_stub import generate
from policy_engine import load_policies, resolve_tenant_policy

app = Flask(__name__)

_POLICIES = None


def get_policies():
    global _POLICIES
    if _POLICIES is None:
        _POLICIES = load_policies()
    return _POLICIES


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "ai-governance-control-plane"})


@app.route("/v1/chat", methods=["POST"])
def chat():
    body = request.get_json(force=True, silent=True) or {}
    messages = body.get("messages")
    if not messages or not isinstance(messages, list):
        return jsonify({"error": "messages[] required"}), 400

    tenant_id = body.get("tenant_id") or request.headers.get("X-Tenant-ID") or "default"
    user_id = body.get("user_id") or request.headers.get("X-User-ID") or "anonymous"

    policies = get_policies()
    policy = resolve_tenant_policy(policies, tenant_id)

    ok, violations = evaluate_input(messages, policy)
    if not ok:
        v = violations[0]
        append_event(
            "request_blocked",
            tenant_id,
            {"user_id": user_id, "code": v.code, "message": v.message, "detail": v.detail},
        )
        return (
            jsonify(
                {
                    "blocked": True,
                    "violation": {"code": v.code, "message": v.message, "detail": v.detail},
                    "tenant_id": tenant_id,
                }
            ),
            403,
        )

    if policy.get("require_approval_for_actions") and body.get("requires_approval"):
        append_event(
            "approval_required",
            tenant_id,
            {"user_id": user_id, "note": "Flagged for human approval (demo)."},
        )
        return jsonify({"blocked": True, "approval_required": True, "tenant_id": tenant_id}), 202

    result = generate(messages, tenant_id)
    out_text, out_violations = evaluate_output(result["content"], policy)

    append_event(
        "response_ok",
        tenant_id,
        {
            "user_id": user_id,
            "model": result.get("model"),
            "latency_ms": result.get("latency_ms"),
            "output_flags": [v.code for v in out_violations],
        },
    )

    return jsonify(
        {
            "blocked": False,
            "tenant_id": tenant_id,
            "risk_tier": policy.get("_risk_tier"),
            "response": {
                "content": out_text,
                "model": result.get("model"),
                "usage": result.get("usage"),
            },
            "governance": {
                "output_warnings": [
                    {"code": v.code, "message": v.message, "detail": v.detail}
                    for v in out_violations
                ]
            },
        }
    )


@app.route("/admin/audit", methods=["GET"])
def audit():
    limit = int(request.args.get("limit", 50))
    return jsonify({"events": read_recent_events(limit=limit)})


@app.route("/admin/policy", methods=["GET"])
def policy_snapshot():
    tenant_id = request.args.get("tenant_id", "default")
    policies = get_policies()
    policy = resolve_tenant_policy(policies, tenant_id)
    # Do not leak regex patterns in production — here for learning
    safe = {k: v for k, v in policy.items() if not k.startswith("_")}
    safe["_tenant_id"] = policy.get("_tenant_id")
    safe["_risk_tier"] = policy.get("_risk_tier")
    return jsonify(safe)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5010"))
    app.run(host="0.0.0.0", port=port, debug=False)
