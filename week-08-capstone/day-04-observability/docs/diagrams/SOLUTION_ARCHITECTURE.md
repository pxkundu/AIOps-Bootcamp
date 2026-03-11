# Solution Architecture: Enterprise Observability Hub

Comprehensive diagrams for the Glean-powered observability, monitoring, logging, and alerting solution.

---

## 🏗️ 1. Full Observability Topology

```mermaid
graph TD
    subgraph "Tier 1: Enterprise Systems"
        PD["PagerDuty<br/>(Incident Stream)"]
        SL["Slack<br/>(War Room + Channels)"]
        JR["Jira<br/>(Issue Tracker)"]
        GH["GitHub<br/>(Commits + PRs)"]
        CW["CloudWatch<br/>(Metrics + Logs)"]
        SN["ServiceNow<br/>(Change Mgmt)"]
    end

    subgraph "Tier 2: Glean Connector Framework"
        NC1["Native Connector:<br/>PagerDuty"]
        NC2["Native Connector:<br/>Slack"]
        NC3["Native Connector:<br/>Jira"]
        NC4["Native Connector:<br/>GitHub"]
        CC1["Custom Connector:<br/>CloudWatch SDK"]
        CC2["Custom Connector:<br/>ServiceNow SDK"]
    end

    subgraph "Tier 3: Intelligence Core"
        CRAWL["Crawl Engine"]
        INDEX["Indexing Pipeline"]
        KG["Knowledge Graph"]
        PERM["Permission Mapper"]
        AI["AI Agent<br/>(Claude / GPT)"]
    end

    subgraph "Tier 4: Observability Output"
        MON["Health Monitor<br/>(Sync Status)"]
        CORR["Alert Correlator"]
        DASH["Flask Dashboard"]
        MCP["MCP Action Server"]
    end

    PD --> NC1
    SL --> NC2
    JR --> NC3
    GH --> NC4
    CW --> CC1
    SN --> CC2

    NC1 & NC2 & NC3 & NC4 & CC1 & CC2 --> CRAWL
    CRAWL --> INDEX --> KG
    KG --> PERM --> AI
    AI --> CORR & MCP
    CRAWL --> MON
    CORR --> DASH
    MCP --> PD & JR
```

---

## ⚡ 2. Connector Sync & Monitoring Pipeline

```mermaid
sequenceDiagram
    participant Admin as Glean Admin
    participant Conn as Connector
    participant Source as Data Source (PagerDuty)
    participant Index as Indexing Engine
    participant Monitor as Health Monitor

    Admin->>Conn: Configure + Start Crawl
    Conn->>Source: Fetch data (API call)
    Source-->>Conn: Return incidents + ACLs
    Conn->>Index: Push Knowledge Objects
    Index->>Monitor: Report sync metrics
    
    loop Every Hour
        Monitor->>Monitor: Check items_synced delta
        alt Delta > 0
            Monitor-->>Admin: Status: HEALTHY
        else Delta = 0 for 24h+
            Monitor-->>Admin: Status: STALLED ⚠️
        end
    end
```

---

## 🔐 3. MCP Action Flow (Read → Write → Execute)

```mermaid
sequenceDiagram
    participant User as SRE Engineer
    participant Agent as Glean AI Agent
    participant MCP as MCP Action Server
    participant PD as PagerDuty API
    participant JR as Jira API

    User->>Agent: "Acknowledge all P1 incidents and create a Jira ticket"
    Agent->>Agent: Parse intent + check permissions
    
    Agent->>MCP: Action: acknowledge_incident(INC-001)
    MCP->>PD: PUT /incidents/INC-001/acknowledge
    PD-->>MCP: 200 OK
    MCP-->>Agent: Acknowledged

    Agent->>MCP: Action: create_jira_ticket(summary, description)
    Agent-->>User: [Human-in-the-Loop] "Confirm: Create ticket 'P1 RCA: DB Outage'?"
    User-->>Agent: ✅ Approved
    MCP->>JR: POST /rest/api/3/issue
    JR-->>MCP: JIRA-4521 Created
    MCP-->>Agent: Ticket Created

    Agent-->>User: "Done. INC-001 acknowledged. JIRA-4521 created for RCA."
```

---

## 📊 4. Alert Correlation Logic

```mermaid
graph TD
    A[PagerDuty: DB Latency > 500ms] --> CORR
    B[Slack: User reports slow queries] --> CORR
    C[GitHub: DB migration merged 2h ago] --> CORR
    D[CloudWatch: CPU spike on db-primary] --> CORR

    CORR["Alert Correlator<br/>(Time Window: 4h)"]

    CORR --> ROOT["ROOT CAUSE:<br/>DB migration caused index rebuild"]
    ROOT --> ACT1["Action: Roll back migration"]
    ROOT --> ACT2["Action: Notify #sre-oncall"]
    ROOT --> ACT3["Action: Create RCA Jira ticket"]
```

---

## 🔄 5. Data Source Visibility Rollout

```mermaid
graph LR
    A["1. Configure Connector"] --> B["2. Set: Test Group Only"]
    B --> C["3. Test Group Verifies"]
    C --> D{"Results Accurate?"}
    D -- Yes --> E["4. Set: Visible to Everyone"]
    D -- No --> F["5. Adjust Data Rules"]
    F --> B
```

---

## 📋 6. Security & Governance Matrix

| Layer | Control | Detail |
|-------|---------|--------|
| **Connector Auth** | OAuth 2.0 / API Token | Per-source authentication |
| **Permission Sync** | ACL Inheritance | Respect source permissions in search results |
| **Visibility** | Test Group → All | Staged rollout of new data sources |
| **MCP Actions** | Human-in-the-Loop | All write/execute actions require user confirmation |
| **Data Rules** | Include/Exclude | Filter channels, repos, ticket types |
| **Audit** | Action Logging | All MCP actions logged with user ID and timestamp |

---

<p align="center">
  <a href="../../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../../project/README.md">Next: Project Guide ➡️</a>
</p>
