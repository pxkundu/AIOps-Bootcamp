# Week 8 Day 7: AI Implementation, Guardrails & Governance

> **Duration:** 8 hours | **Difficulty:** Advanced

---

## Learning objectives

By the end of this day you will be able to:

1. Describe an end-to-end **AI implementation lifecycle** (discover → design → build → deploy → monitor → improve).
2. Define **guardrails** across prompts, tools, data, and outputs—and map them to **technical controls**.
3. Stand up a **governance** model: policies, risk classification, approvals, audit, and continuous review.
4. Explain how the capstone **Governance Control Plane** fits into a larger enterprise architecture.

---

## 1. AI implementation: what “done” actually means

### 1.1 Lifecycle (high level)

| Phase | Focus | Common failure mode |
|-------|--------|---------------------|
| **Discover** | Problem fit, data availability, success metrics | “AI for AI’s sake” |
| **Design** | Architecture, model choice, evaluation plan, risk | No offline evaluation |
| **Build** | Pipelines, RAG, tools, guardrails | Training-serving skew |
| **Deploy** | Routing, capacity, fallbacks, observability | No rollback |
| **Operate** | Drift, incidents, cost, abuse | No owner after launch |
| **Improve** | Feedback loops, policy updates, retraining | Static prompts forever |

### 1.2 Implementation pillars

1. **Data:** lineage, consent, retention, minimization, PII handling.
2. **Model:** versioning, evaluation sets, bias/safety checks where applicable.
3. **System:** idempotency, timeouts, rate limits, circuit breakers.
4. **Human:** escalation paths, override rules, training for operators.

---

## 2. Guardrails: technical controls

Guardrails are **enforceable rules** applied before, during, or after model inference.

### 2.1 Categories

| Layer | Examples |
|-------|----------|
| **Input** | Prompt injection detection, max length, allow/deny topics, schema validation |
| **Context** | Retrieval boundaries, document ACLs, source pinning |
| **Tool** | Tool allowlists, argument validation, rate limits, “high-risk” gates |
| **Output** | Toxicity filters, PII redaction, citation requirements, structured output validation |
| **Process** | Human-in-the-loop for sensitive actions, dual control, change management |

### 2.2 Principle: defense in depth

No single guardrail is sufficient. Combine **policy rules** + **classifiers** (where appropriate) + **human approval** for irreversible operations.

---

## 3. Governance: organizational controls

Governance answers **who decides**, **what is allowed**, **how we prove**, and **how we recover**.

### 3.1 Core artifacts

| Artifact | Purpose |
|----------|---------|
| **AI policy** | Acceptable use, data classes, prohibited use cases |
| **Risk tiers** | Map use cases to approval, logging, and monitoring |
| **Model registry** | Approved models, versions, owners, evaluation status |
| **Audit trail** | Who requested what, when, with what outcome |
| **Incident playbooks** | Model misuse, data leak, prompt injection campaigns |

### 3.2 Operating cadence

- **Quarterly:** policy review, risk tier updates, vendor/model review.
- **Monthly:** guardrail effectiveness review (blocked vs false positives).
- **Continuous:** drift monitoring, cost anomalies, abuse detection.

---

## 4. Mapping to the capstone project

The **AI Governance Control Plane** (in `project/`) demonstrates:

- **Policy-as-code** (`config/policies.yaml`)
- **Guardrail pipeline** (injection checks, deny lists, optional PII handling)
- **Audit logging** (structured events for compliance)
- **API boundary** where all “LLM traffic” should pass in production

See [docs/diagrams/SOLUTION_ARCHITECTURE.md](docs/diagrams/SOLUTION_ARCHITECTURE.md) for diagrams.

---

## 5. Deliverables checklist

- [ ] Read [docs/GOVERNANCE_FRAMEWORK.md](docs/GOVERNANCE_FRAMEWORK.md)
- [ ] Read [docs/guides/GUARDRAIL_IMPLEMENTATION_GUIDE.md](docs/guides/GUARDRAIL_IMPLEMENTATION_GUIDE.md)
- [ ] Read [docs/guides/AUDIT_AND_COMPLIANCE_GUIDE.md](docs/guides/AUDIT_AND_COMPLIANCE_GUIDE.md)
- [ ] Review Real-world Scenarios in [docs/guides/USE_CASES.md](docs/guides/USE_CASES.md)
- [ ] Run the capstone project and execute the tests
- [ ] Extend **one** policy: add a new deny-list term or a new risk tier rule
- [ ] Run the traffic simulation script `project/scripts/simulate_traffic.py`
- [ ] Document your architecture choice in 1 page (for your portfolio)

---

<p align="center">
  <a href="../README.md">← Week 8</a> | <a href="project/README.md">Capstone project →</a>
</p>
