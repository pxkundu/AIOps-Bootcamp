# Knowledge Graph Deep Dive Guide

A comprehensive guide to the Glean Knowledge Graph for enterprise IDP builders.

---

## 🧠 What is the Knowledge Graph?

The Glean Knowledge Graph is the **intelligence backbone** that powers enterprise search. It goes beyond simple keyword matching by understanding:
- **What** content exists (Content Integration)
- **Who** created and consumes it (People Intelligence)
- **How** it's being used (Activity Tracking)
- **Why** it matters right now (Collective Intelligence)

---

## 📐 The 4 Pillars — In Depth

### Pillar 1: Content Integration

Every piece of enterprise content is indexed with rich metadata:

| Field | Description | Example |
|-------|-------------|---------|
| **Title** | Document name | "Payment API Runbook" |
| **Body** | Full text content | Step-by-step diagnosis... |
| **Comments** | Discussion threads | "Fixed in PR #1482" |
| **Creator** | Author identity | alice@corp.com |
| **Created** | Timestamp | 2026-01-15T14:30:00Z |
| **Updated** | Last modification | 2026-03-10T09:00:00Z |
| **File Type** | Content format | markdown, pdf, code |
| **Folder** | Hierarchy path | /SRE/Runbooks/Payment/ |
| **Permissions** | ACL groups | ["SRE", "DevOps"] |

**Crawl Configuration Options:**
- **Frequency**: Real-time (webhooks), hourly, daily, weekly.
- **Blackout Periods**: Pause crawling during peak hours.
- **Methodologies**: Full crawl, incremental, delta sync.

### Pillar 2: People Intelligence

The Knowledge Graph builds a **unified identity** for every person:

```
Alice Chen
├─ Email: alice@corp.com
├─ Slack: @alice.chen
├─ GitHub: @alicechen
├─ Jira: alice.chen
├─ Team: SRE → Platform (Director: Bob Kumar)
├─ Expertise: kubernetes, payment-api, incident-response
├─ Authored: 42 documents
├─ Collaborators: charlie, dave, eve
└─ Activity Score: 87/100
```

**Use Cases:**
- "Who is the expert on Kubernetes?" → Alice Chen (Staff SRE)
- "Who should review this auth change?" → Charlie Okafor (Identity team)
- "Who collaborates most across SRE and Data?" → Collaboration graph edges

### Pillar 3: Activity Tracking

Signals are collected from multiple touchpoints (with privacy controls):

| Signal Source | Data Captured | Privacy |
|--------------|---------------|---------|
| Teams/Slack | Channels joined, messages (metadata only) | No message content stored |
| Email | Subject lines (metadata only) | No body content stored |
| Browser Extension | Pages visited on internal tools | Anonymized after 30 days |
| Search | Queries, clicks, dwell time | Used for ranking, not profiling |

**Knowledge Gaps**: When users search for something that returns 0 results, it's logged as a "gap" — telling admins what content needs to be created.

### Pillar 4: Collective Intelligence

The aggregated behavior of all users improves results for everyone:

| Signal | Effect |
|--------|--------|
| 50 views on a runbook in 1 hour | Runbook is auto-boosted in search |
| 3 teams referencing the same Jira | Jira ticket surfaces across teams |
| New hire searches "onboarding guide" | Guide appears on homepage |

---

## 🏗️ Building Custom Data Sources for IDP

Based on the [Glean Custom Connectors doc](https://docs.glean.com/connectors/custom/about):

### Step 1: Register the Data Source
```bash
curl -X POST https://customer-api.glean.com/api/indexing/v1/datasources \
  -H "Authorization: Bearer $GLEAN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "service-catalog",
    "displayName": "Service Catalog",
    "datasourceCategory": "CUSTOM",
    "urlRegex": "https://catalog.internal.corp.com/.*"
  }'
```

### Step 2: Push Documents
```bash
curl -X POST https://customer-api.glean.com/api/indexing/v1/documents \
  -H "Authorization: Bearer $GLEAN_TOKEN" \
  -d '{
    "datasource": "service-catalog",
    "documents": [{
      "id": "SVC-001",
      "title": "payment-api",
      "body": { "text": "The Payment API handles all checkout transactions..." },
      "author": { "email": "alice@corp.com" },
      "permissions": { "allowedUsers": [], "allowedGroups": ["SRE", "DevOps"] }
    }]
  }'
```

### Step 3: Verify
```bash
curl https://customer-api.glean.com/api/indexing/v1/documents/SVC-001 \
  -H "Authorization: Bearer $GLEAN_TOKEN"
```

### Deployment Options
- **Glean-hosted**: Docker container in Glean's cloud. Secrets in cloud project.
- **Self-hosted (AWS)**: Container in ECS/EKS. Secrets in AWS Secrets Manager.

---

## 🔐 Security Model

All queries respect the **source system's permissions**:
1. User authenticates via SSO/SAML.
2. Knowledge Graph checks user's group memberships.
3. Only documents where user's groups match the ACL are returned.
4. No admin override — even Glean admins cannot bypass ACLs.

---

<p align="center">
  <a href="../../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../diagrams/SOLUTION_ARCHITECTURE.md">Next: Architecture ➡️</a>
</p>
