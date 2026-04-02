# AI Governance Framework (Enterprise Reference)

> Use this as a **template** for documentation in your org. Adapt roles, tools, and cadence to your environment.

---

## 1. Purpose

Establish **accountable, auditable, and safe** use of AI systems—including LLMs, retrieval, embeddings, and agentic workflows—across build and run phases.

---

## 2. Scope

| In scope | Out of scope (example) |
|----------|-------------------------|
| AI-powered products and internal tools | Generic IT security policy (reference separately) |
| Data used for model input/output | Non-AI ML models (unless governed by same board) |
| Third-party models and APIs | Pure research without production data |

---

## 3. Risk tiers (example)

| Tier | Description | Controls |
|------|-------------|----------|
| **T0** | Public, non-sensitive content generation | Standard logging |
| **T1** | Internal business data; low harm if wrong | Access control + retention + evaluation |
| **T2** | PII/regulated data; material business impact | Strong guardrails + audit + approvals |
| **T3** | High-risk (health, safety, financial advice) | Human-in-the-loop + legal review + monitoring |

---

## 4. Roles (RACI-style)

| Activity | Engineering | Security | Legal/Privacy | Product | Executive sponsor |
|----------|-------------|----------|----------------|---------|-------------------|
| Use case intake | R | C | C | A | I |
| Risk tiering | R | A | C | C | I |
| Policy approval | C | C | A | R | C |
| Model allowlist | R | A | I | C | I |
| Incident response | A | A | C | C | I |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

---

## 5. Policy topics (minimum)

1. **Acceptable use** (what is prohibited; e.g., surveillance, deception).
2. **Data handling** (classification, retention, cross-border transfer).
3. **Human oversight** (when required; escalation paths).
4. **Third-party models** (vendor review, DPAs, subprocessors).
5. **Audit & evidence** (logs, retention, access to logs).

---

## 6. Evidence pack (for audits)

- Architecture diagram (data flows, trust boundaries).
- Policy version history and approval records.
- Evaluation results (quality, safety, fairness) per release.
- Guardrail configuration (what is blocked, how tuned).
- Incident runbooks and postmortems.

---

## 7. Continuous improvement

| Signal | Action |
|--------|--------|
| Rising block rate | Tune rules; check for false positives |
| User complaints | Review prompts and guardrail UX |
| New regulations | Update policy + technical controls |
| New model version | Re-run evaluation suite + regression tests |

---

<p align="center">
  <a href="../lecture-notes.md">← Lecture notes</a> | <a href="diagrams/SOLUTION_ARCHITECTURE.md">Solution architecture →</a>
</p>
