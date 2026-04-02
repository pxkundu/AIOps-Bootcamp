# Capstone: AI Governance Control Plane — Solution Architecture

> Reference architecture for the Day 7 project: a **policy-enforcing gateway** in front of LLM calls, with **audit** and **guardrails**.

---

## 1. Context diagram

```mermaid
flowchart TB
    subgraph Clients["Clients"]
        APP[Web app / agent]
        CLI[Internal tools]
    end

    subgraph GCP["AI Governance Control Plane"]
        API[Policy API<br/>Flask]
        PE[Policy engine]
        GR[Guardrails]
        AUD[Audit logger]
        LLM[LLM stub / adapter]
    end

    subgraph External["External systems"]
        MODEL[Real LLM provider<br/>optional in production]
        SIEM[SIEM / log archive<br/>optional]
    end

    APP --> API
    CLI --> API
    API --> PE
    PE --> GR
    GR -->|allow| LLM
    GR -->|deny| AUD
    LLM --> AUD
    AUD --> SIEM
    LLM -.->|production| MODEL

    style GR fill:#2d3436,color:#fff
    style AUD fill:#0984e3,color:#fff
```

---

## 2. Request flow (sequence)

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Control Plane API
    participant P as Policy engine
    participant G as Guardrails
    participant L as LLM adapter
    participant U as Audit Log

    C->>A: POST /v1/chat (messages, user, tenant)
    A->>P: Resolve tenant policy + risk tier
    P->>G: Evaluate input + context
    alt Blocked
        G-->>A: violation + code
        A->>U: log blocked + reason
        A-->>C: 403 + policy detail
    else Allowed
        G-->>L: sanitized / unchanged payload
        L->>L: generate (stub or provider)
        L->>U: log success + latency
        A-->>C: 200 + response
    end
```

---

## 3. Governance operating model (people + process)

```mermaid
flowchart LR
    subgraph Gov["Governance"]
        POL[Policies]
        RISK[Risk tiers]
        REG[Model registry]
    end

    subgraph Tech["Technical controls"]
        GW[Guardrails]
        AUD[Audit]
        MON[Monitoring]
    end

    POL --> GW
    RISK --> GW
    REG --> GW
    GW --> AUD
    GW --> MON

    style Gov fill:#1a1a2e,color:#fff
    style Tech fill:#16213e,color:#fff
```

---

## 4. Deployment options

| Pattern | When to use |
|---------|-------------|
| **Sidecar / gateway** | Single entry for all LLM traffic (recommended for enforcement) |
| **SDK wrapper** | Fast adoption; weaker guarantee if bypassed |
| **Proxy** | Centralized routing + rate limits + policy |

The capstone implements a **gateway-style** API so enforcement is explicit and testable.

---

## 5. Extension points (for your portfolio)

- **OIDC / JWT** for user identity and tenant claims.
- **OPA** or **Open Policy Agent** for complex policy rules.
- **Async queue** for human approval on T3 actions.
- **Export audit logs** to SIEM (Splunk, Datadog, CloudWatch).

---

<p align="center">
  <a href="../GOVERNANCE_FRAMEWORK.md">← Governance framework</a> | <a href="../../project/README.md">Run the project →</a>
</p>
