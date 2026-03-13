# Project Guide: AWS Cloud IDP with Glean Knowledge Graph

Build a complete Internal Developer Portal on AWS powered by the Glean Knowledge Graph.

---

## 📋 Prerequisites

| Requirement | Installation |
|-------------|-------------|
| **Python 3.10+** | `brew install python` |
| **Flask** | `pip install flask` |
| **Terraform** (for AWS) | `brew install terraform` |
| **AWS CLI** (for AWS) | `brew install awscli` |
| **Docker** (optional) | `brew install --cask docker` |

---

## 🏗️ Phase 1: Understand the Knowledge Graph

Before building, review the 4 pillars:

| Pillar | What it Does | IDP Value |
|--------|-------------|-----------|
| **Content Integration** | Indexes all enterprise content with metadata | Unified search across wikis, APIs, tickets |
| **People Intelligence** | Builds unified identities with expertise tags | "Who owns this service?" answered instantly |
| **Activity Tracking** | Tracks search patterns and knowledge gaps | Surfaces trending content, identifies missing docs |
| **Collective Intelligence** | Aggregated user behavior boosts relevant content | Popular runbooks auto-surface during incidents |

👉 Deep dive: [Knowledge Graph Guide](../docs/guides/KNOWLEDGE_GRAPH_GUIDE.md)

---

## 🧪 Phase 2: Run the Knowledge Graph Engine

### Step 2.1: Test the core engine

```bash
cd project/src
python knowledge_graph/kg_engine.py
```

**Expected Output:**
```json
[
  {
    "document": {
      "id": "RB-001",
      "title": "Payment API Runbook",
      "source": "Internal Wiki",
      ...
    },
    "score": 6.0
  }
]
```

### Step 2.2: Test custom connectors

```bash
python knowledge_graph/custom_connectors.py
```

This loads: 3 services, 2 OKRs, 2 runbooks, 2 API docs, and 5 people profiles.

---

## 🚀 Phase 3: Launch the IDP Portal (Local)

### Step 3.1: Run preflight checks

```bash
bash scripts/deploy.sh
```

### Step 3.2: Start the portal

```bash
cd project/src
python portal/app.py
```

### Step 3.3: Open in browser

Navigate to `http://localhost:5005`

You will see:
- **Stats bar**: Knowledge objects, people, searches, facets, knowledge gaps.
- **Live Search**: Type "payment runbook" → returns scored results.
- **Service Catalog**: Cards for payment-api, auth-service, data-pipeline.
- **People Directory**: Profiles with expertise tags and collaboration links.
- **OKR Dashboard**: Current quarter objectives with status indicators.

---

## 📡 Phase 4: Explore the APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search?q=runbook` | GET | Permission-aware knowledge search |
| `/api/stats` | GET | Knowledge Graph statistics |
| `/api/people` | GET | All people profiles |
| `/api/expert/kubernetes` | GET | Find experts on a topic |
| `/api/gaps` | GET | Queries with 0 results (knowledge gaps) |
| `/api/trending` | GET | Most viewed/searched documents |
| `/api/facets` | GET | Available facet dimensions and values |

### Example: Search for payment experts

```bash
curl "http://localhost:5005/api/expert/payment-api" | python -m json.tool
```

### Example: Find knowledge gaps

```bash
curl "http://localhost:5005/api/gaps" | python -m json.tool
```

---

## ☁️ Phase 5: Deploy to AWS (ECS Fargate)

### Step 5.1: Configure Terraform variables

```bash
cd project/src/terraform
cp terraform.tfvars.sample terraform.tfvars
# Edit terraform.tfvars with your AWS credentials
```

### Step 5.2: Initialize and plan

```bash
terraform init
terraform plan
```

### Step 5.3: Deploy

```bash
terraform apply -auto-approve
```

### Step 5.4: Get the portal URL

```bash
terraform output alb_url
# → http://kg-idp-alb-123456.us-east-1.elb.amazonaws.com
```

**Architecture deployed:**
- ECS Fargate (serverless containers)
- Application Load Balancer (public endpoint)
- RDS PostgreSQL 16 (private subnet)
- CloudWatch (logging)

---

## 📂 File Map

| File | Purpose |
|------|---------|
| `knowledge_graph/kg_engine.py` | Core KG engine with all 4 pillars |
| `knowledge_graph/custom_connectors.py` | Service catalog, OKR, runbook, API doc connectors |
| `portal/app.py` | Flask IDP portal with search and dashboards |
| `terraform/main.tf` | Full AWS infrastructure (ECS, ALB, RDS, VPC) |
| `scripts/deploy.sh` | Preflight check and deployment script |
| `config/idp_config.json` | Knowledge Graph and portal configuration |

---

## 🔧 Extending the IDP

### Add a New Data Source

1. Create a new function in `custom_connectors.py`:
```python
def load_incident_history():
    return [
        KnowledgeObject(
            "INC-001", "PagerDuty", "DB Latency Spike",
            "Root cause: index rebuild after migration...",
            "alice", "incident", {"severity": "P1"}, ["SRE"]
        ),
    ]
```

2. Import and index in `portal/app.py`:
```python
from knowledge_graph.custom_connectors import load_incident_history
for doc in load_incident_history():
    kg.index_document(doc)
```

### Add a New Person

Add to `load_people()` in `custom_connectors.py` and tag expertise in `set_expertise()`.

### Push to Glean Indexing API (Production)

```bash
curl -X POST https://customer-api.glean.com/api/indexing/v1/documents \
  -H "Authorization: Bearer $GLEAN_API_TOKEN" \
  -d @document_payload.json
```

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../resources/RESOURCES.md">Next: Resources ➡️</a>
</p>
