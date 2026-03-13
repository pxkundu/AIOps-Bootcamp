"""
Custom Connectors for the IDP Knowledge Graph.
Simulates pushing enterprise data sources into the Glean Indexing API.
Based on: https://docs.glean.com/connectors/custom/about
"""

import json
from datetime import datetime, timedelta
from knowledge_graph.kg_engine import KnowledgeObject, PersonProfile


def load_service_catalog():
    """Custom Connector: Internal Service Catalog (CMDB)."""
    return [
        KnowledgeObject(
            "SVC-001", "Service Catalog", "payment-api",
            "The Payment API handles all checkout transactions. Tech: Python, FastAPI, PostgreSQL. "
            "SLA: 99.95%. On-call: #sre-payment. Runbook: RB-001. Dependencies: auth-service, db-primary.",
            "alice", "service", {"team": "Payments", "tier": "Tier-1", "language": "Python"},
            ["SRE", "DevOps", "Developer"]
        ),
        KnowledgeObject(
            "SVC-002", "Service Catalog", "auth-service",
            "Central authentication and authorization service. Handles OAuth2, SAML, MFA. "
            "Tech: Go, Redis. SLA: 99.99%. On-call: #sre-identity.",
            "charlie", "service", {"team": "Identity", "tier": "Tier-0", "language": "Go"},
            ["SRE", "DevOps", "Developer"]
        ),
        KnowledgeObject(
            "SVC-003", "Service Catalog", "data-pipeline",
            "ETL pipeline for analytics. Processes 2TB/day from Kafka to Snowflake. "
            "Tech: Spark, Airflow. On-call: #data-eng.",
            "dave", "service", {"team": "Data", "tier": "Tier-2", "language": "Python"},
            ["Data", "SRE"]
        ),
    ]


def load_okrs():
    """Custom Connector: Engineering OKRs."""
    return [
        KnowledgeObject(
            "OKR-Q1-001", "OKR Tool", "Q1 Platform Reliability OKR",
            "Objective: Achieve 99.95% uptime across all Tier-1 services.\n"
            "KR1: Reduce MTTR to under 15 minutes (current: 28 min).\n"
            "KR2: Deploy automated rollback for 100% of Tier-1 services.\n"
            "KR3: Zero P1 incidents lasting > 30 minutes.",
            "bob", "okr", {"quarter": "Q1-2026", "team": "Platform", "status": "On Track"},
            ["Platform", "Executives", "SRE"]
        ),
        KnowledgeObject(
            "OKR-Q1-002", "OKR Tool", "Q1 Developer Productivity OKR",
            "Objective: Reduce developer friction by 40%.\n"
            "KR1: Internal search satisfaction score > 4.5/5.\n"
            "KR2: Onboarding time for new engineers < 2 weeks.\n"
            "KR3: 90% of APIs have up-to-date documentation.",
            "eve", "okr", {"quarter": "Q1-2026", "team": "DevEx", "status": "At Risk"},
            ["DevEx", "Executives", "Developer"]
        ),
    ]


def load_runbooks():
    """Custom Connector: Incident Runbooks from Internal Wiki."""
    return [
        KnowledgeObject(
            "RB-001", "Internal Wiki", "Payment API Runbook",
            "# Payment API Incident Response\n"
            "## Symptoms\n- 5xx errors on /checkout endpoint\n- Latency > 500ms\n"
            "## Diagnosis\n1. Check DB connection pool: `SELECT count(*) FROM pg_stat_activity;`\n"
            "2. Check recent deployments: `kubectl rollout history deploy/payment-api`\n"
            "## Remediation\n- If DB: `kubectl exec -it db-primary -- pg_reload_conf`\n"
            "- If deploy: `kubectl rollout undo deploy/payment-api`",
            "alice", "runbook", {"service": "payment-api", "severity": "P1"},
            ["SRE", "DevOps"]
        ),
        KnowledgeObject(
            "RB-002", "Internal Wiki", "Auth Service Runbook",
            "# Auth Service Incident Response\n"
            "## Symptoms\n- 401/403 errors across multiple services\n- Redis connection timeouts\n"
            "## Diagnosis\n1. Check Redis: `redis-cli ping`\n"
            "2. Verify certs: `openssl s_client -connect auth:443`\n"
            "## Remediation\n- Restart Redis: `kubectl rollout restart statefulset/redis`",
            "charlie", "runbook", {"service": "auth-service", "severity": "P0"},
            ["SRE", "DevOps"]
        ),
    ]


def load_api_docs():
    """Custom Connector: API Documentation from Developer Portal."""
    return [
        KnowledgeObject(
            "API-001", "Developer Portal", "Payment API Reference",
            "POST /api/v2/checkout - Process a payment.\n"
            "Headers: Authorization: Bearer <token>\n"
            "Body: {amount: number, currency: string, customer_id: string}\n"
            "Response: {transaction_id: string, status: 'completed'|'pending'|'failed'}",
            "alice", "api-doc", {"service": "payment-api", "version": "v2"},
            ["Developer", "SRE"]
        ),
        KnowledgeObject(
            "API-002", "Developer Portal", "Auth Service API Reference",
            "POST /auth/token - Generate an access token.\n"
            "Body: {client_id: string, client_secret: string, grant_type: 'client_credentials'}\n"
            "Response: {access_token: string, expires_in: 3600, token_type: 'Bearer'}",
            "charlie", "api-doc", {"service": "auth-service", "version": "v1"},
            ["Developer"]
        ),
    ]


def load_people():
    """Custom Connector: People profiles from HR system."""
    return [
        PersonProfile("alice", "Alice Chen", "alice@corp.com", "SRE", "Staff SRE", "bob"),
        PersonProfile("bob", "Bob Kumar", "bob@corp.com", "Platform", "Director of Platform", None),
        PersonProfile("charlie", "Charlie Okafor", "charlie@corp.com", "Identity", "Senior Engineer", "bob"),
        PersonProfile("dave", "Dave Park", "dave@corp.com", "Data", "Data Engineer", "bob"),
        PersonProfile("eve", "Eve Santos", "eve@corp.com", "DevEx", "DevEx Lead", "bob"),
    ]


def set_expertise(people_map):
    """Tag expertise based on authored content and metadata."""
    expertise_map = {
        "alice": ["kubernetes", "incident-response", "payment-api", "postgresql"],
        "bob": ["platform-strategy", "okrs", "architecture"],
        "charlie": ["authentication", "oauth2", "redis", "go"],
        "dave": ["spark", "airflow", "data-pipeline", "kafka"],
        "eve": ["developer-experience", "documentation", "onboarding"],
    }
    for pid, topics in expertise_map.items():
        if pid in people_map:
            people_map[pid].expertise = topics
            people_map[pid].activity_score = len(topics) * 10


if __name__ == "__main__":
    print("Service Catalog:", len(load_service_catalog()), "items")
    print("OKRs:", len(load_okrs()), "items")
    print("Runbooks:", len(load_runbooks()), "items")
    print("API Docs:", len(load_api_docs()), "items")
    print("People:", len(load_people()), "profiles")
