# Solution Architecture: Knowledge Graph IDP on AWS

---

## 🏗️ 1. Full AWS Infrastructure Topology

```mermaid
graph TD
    subgraph "Users"
        ENG["Engineers"]
        MGR["Managers"]
        SRE["SRE/DevOps"]
    end

    subgraph "AWS Cloud (VPC)"
        subgraph "Public Subnet"
            ALB["Application Load Balancer"]
        end

        subgraph "Private Subnet A"
            ECS["ECS Fargate Cluster"]
            PORTAL["IDP Portal Container"]
            KG_SVC["Knowledge Graph Service"]
            CONN["Custom Connector Workers"]
        end

        subgraph "Private Subnet B"
            RDS["RDS PostgreSQL 16"]
        end

        S3["S3 Bucket<br/>(Document Store)"]
        SM["Secrets Manager"]
        CW["CloudWatch"]
    end

    subgraph "Glean Platform"
        GLEAN_API["Glean Indexing API"]
        GLEAN_SEARCH["Glean Search API"]
        GLEAN_KG["Glean Knowledge Graph"]
    end

    subgraph "Enterprise Data Sources"
        GITHUB["GitHub"]
        SLACK["Slack"]
        JIRA["Jira"]
        CONFL["Confluence"]
        WIKI["Internal Wiki"]
    end

    ENG & MGR & SRE --> ALB --> PORTAL
    PORTAL --> KG_SVC --> RDS
    KG_SVC --> S3
    CONN --> GLEAN_API
    PORTAL --> GLEAN_SEARCH
    GLEAN_API --> GLEAN_KG
    GITHUB & SLACK & JIRA & CONFL & WIKI --> CONN
    SM -. "Secrets" .-> CONN
    ECS --> CW
```

---

## ⚡ 2. Knowledge Graph Data Flow

```mermaid
sequenceDiagram
    participant DS as Data Source (GitHub/Jira/Wiki)
    participant CC as Custom Connector (ECS)
    participant IDX as Glean Indexing API
    participant KG as Knowledge Graph
    participant PI as People Intelligence
    participant IDP as IDP Portal
    participant User as Engineer

    DS->>CC: Raw data (API pull)
    CC->>CC: Extract content + metadata + ACLs
    CC->>IDX: POST /indexing/v1/documents
    IDX->>KG: Index Knowledge Objects
    KG->>PI: Map authors → People profiles
    
    User->>IDP: Search: "payment-api runbook"
    IDP->>KG: Query with user context
    KG->>KG: Apply ACLs + Activity boost
    KG-->>IDP: Ranked results
    IDP-->>User: Runbook + Code Owner + Related PRs
```

---

## 🧠 3. Knowledge Graph Pillar Architecture

```mermaid
graph TD
    subgraph "Pillar 1: Content Integration"
        C1["Full Content Analysis"]
        C2["Metadata Extraction"]
        C3["Permission Sync"]
        C4["Faceted Search"]
    end

    subgraph "Pillar 2: People Intelligence"
        P1["Unified Identity"]
        P2["Org Chart Mapping"]
        P3["Expertise Tagging"]
        P4["Collaboration Graph"]
    end

    subgraph "Pillar 3: Activity Tracking"
        A1["View History"]
        A2["Search Patterns"]
        A3["Click Signals"]
        A4["Knowledge Gaps"]
    end

    subgraph "Pillar 4: Collective Intelligence"
        I1["Trending Content"]
        I2["Popular Resources"]
        I3["Team Recommendations"]
        I4["Organic Boosting"]
    end

    KG["Knowledge Graph Core"]
    KG --> C1 & C2 & C3 & C4
    KG --> P1 & P2 & P3 & P4
    KG --> A1 & A2 & A3 & A4
    KG --> I1 & I2 & I3 & I4
```

---

## 🐳 4. ECS Fargate Service Architecture

```mermaid
graph LR
    subgraph "ECS Cluster: idp-cluster"
        subgraph "Service: portal"
            T1["Task: Flask IDP Portal<br/>Port 5000"]
        end
        subgraph "Service: kg-engine"
            T2["Task: Knowledge Graph API<br/>Port 5001"]
        end
        subgraph "Service: connectors"
            T3["Task: Connector Workers<br/>Scheduled"]
        end
    end

    ALB["ALB :443"] --> T1
    T1 --> T2
    T2 --> RDS["RDS PostgreSQL"]
    T2 --> S3["S3 Docs"]
    T3 --> GLEAN["Glean Indexing API"]
```

---

## 🔐 5. Security & Governance

| Layer | AWS Service | Purpose |
|-------|------------|---------|
| **Network** | VPC + Private Subnets | Portal and DB in isolated network |
| **Compute** | ECS Fargate | Serverless containers, no EC2 to patch |
| **Identity** | IAM Roles | Task-level scoped permissions |
| **Secrets** | Secrets Manager | API keys, DB passwords |
| **Data** | RDS Encryption + S3 SSE | Encryption at rest (KMS) |
| **Transport** | ALB + ACM | TLS termination with AWS Certificate Manager |
| **Access** | Knowledge Graph ACLs | Source-inherited permissions on every query |
| **Audit** | CloudWatch + CloudTrail | Full request and access audit trail |

---

## 📊 6. IDP Value Metrics

```mermaid
graph TD
    subgraph "Inputs (Knowledge Graph)"
        D1["100+ Data Sources"]
        D2["50k+ Documents Indexed"]
        D3["500+ People Profiles"]
    end

    subgraph "IDP Portal Metrics"
        M1["Avg Search Time: < 3s"]
        M2["Knowledge Gap Reduction: 40%"]
        M3["Onboarding Time: -60%"]
        M4["Incident RCA: -45% MTTR"]
    end

    D1 & D2 & D3 --> M1 & M2 & M3 & M4
```

---

<p align="center">
  <a href="../../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../../project/README.md">Next: Project Guide ➡️</a>
</p>
