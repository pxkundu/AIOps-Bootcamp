# Solution Architecture: Glean-SEC Enterprise Hub

Visualizing the multi-layer architecture of the Glean-SEC platform for enterprise security discovery and analytics.

---

## 🏗️ 1. High-Level System Architecture

This diagram shows the relationship between the external enterprise silos, the Glean Intelligence Core, and the final AIOps outcome (Alerting/Monitoring).

```mermaid
graph TD
    subgraph "Enterprise Data Silos (Connectors)"
        GH["GitHub Repos"]
        SL["Slack History"]
        CF["Confluence Wiki"]
        DB["Internal SQL DB"]
    end

    subgraph "Glean-SEC Intelligence Core"
        IC["Ingestion Controller"]
        IN["Indexing Pipeline"]
        KG["Knowledge Graph Engine"]
        SA["Security Analytics (Regex/LLM)"]
        PM["Permission Mapper"]
    end

    subgraph "AIOps Outcome (Alerting & UI)"
        AL["Slack/PagerDuty Alerts"]
        DS["Flask Security Dashboard"]
        REP["Audit Reports (JSON)"]
    end

    GH & SL & CF & DB --> IC
    IC --> IN
    IN --> KG
    KG --> SA
    SA --> PM
    PM --> AL & DS & REP
```

---

## ⚡ 2. Data Flow & Processing Pipeline

The following sequence details how a single "Knowledge Object" (e.g., a Slack message about a leak) is processed through the system.

```mermaid
sequenceDiagram
    participant Source as Data Source (Slack/Jira)
    participant Ingest as Ingestor API
    participant Index as Indexing Service
    participant Scan as Security Scanner
    participant Notify as Notification Engine

    Source->>Ingest: Send raw data/metadata
    Ingest->>Index: Transform to Knowledge Object
    Index->>Scan: Trigger Security Scan
    
    par Pattern Match (Regex)
        Scan-->>Scan: Look for secrets (KEY/TOKEN)
    and Semantic Discovery (LLM)
        Scan-->>Scan: Analyze context for policy drift
    end
    
    Scan->>Notify: Create High-Risk Alert (if found)
    Notify->>Notify: Route to Security Channel
```

---

## 🛠️ 3. Security Discovery Logic (Branching)

This flowchart represents the logic used within the `glean_engine.py` to classify and prioritize risks.

```mermaid
graph TD
    Start([New Knowledge Object Indexed]) --> P1{Has Secret Patterns?}
    P1 -- Yes --> S1[Critical: Credential Leak]
    P1 -- No --> P2{Mentioned 'Credentials' or 'Leak'?}
    P2 -- Yes --> S2[High: Policy Violation Mentioned]
    P2 -- No --> P3{Old/Unmaintained Project?}
    P3 -- Yes --> S3[Low: Surface Area Risk]
    P3 -- No --> End([No Risk Identified])
    
    S1 & S2 & S3 --> Agg[Aggregate Risk Score]
    Agg --> Dash[Update Dashboard]
```

---

## 📋 Architectural Documentation

### **Ingestion Controller**
- **Job**: Collects data from Slack, GitHub, and Confluence.
- **Protocol**: Uses a mix of Webhooks (Real-time) and REST APIs (Crawl).
- **Redaction**: First-stage PII masking happens at this layer.

### **Indexing Service**
- **Job**: Normalizes disparate JSON formats into a standard **Knowledge Metadata Schema**.
- **Storage**: In a production environment, this would feed into a Vector Database (like Pinecone) or a Search Index (like Elasticsearch).

### **Security Analytics Engine**
- **Job**: The "Brain" of the project. It uses hard-coded rules (Day 1-2 skills) and LLM-assisted discovery (Day 3-4 skills) to find risks that traditional logs miss.

---

<p align="center">
  <a href="../../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../GLEAN_GUIDE.md">Glean Guide</a>
</p>
