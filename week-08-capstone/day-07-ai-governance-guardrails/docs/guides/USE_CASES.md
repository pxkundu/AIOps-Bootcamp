# AI Governance Control Plane: Enterprise Use Cases

This document details three specific enterprise scenarios demonstrating how the AI Governance Control Plane (Gateway) enforces policies across distinct risk profiles.

---

## 1. The Internal HR Copilot (Tier 2: Medium Risk)

**The Scenario:** 
HR personnel use an internal AI assistant to summarize candidate resumes, compare employment records, and draft internal transfer documents.

**The Risk:** 
The assistant fundamentally processes Personally Identifiable Information (PII) including names, addresses, and salaries. The risk is that the LLM might hallucinate salary details, or the raw outputs might be logged into public IT telemetry systems.

**Governance Implementation:**
* **Configuration:** Uses the `policy_relaxed.yaml`.
* **Output Guardrails:** `redact_pii: false` allows the AI to process internal names functionally without breaking the use case.
* **Audit Logging:** The crucial component here is `audit_logging_config.json`. We set `"mask_pii": true` applied to the audit logs. The interactions are saved to the S3 bucket, but all names and salaries are replaced with `<PERSON>` or `<MONEY>` tags in the logging pipeline, preserving user privacy while allowing security teams to audit prompt volume.

---

## 2. Customer-Facing Support Agent (Tier 1: High Risk)

**The Scenario:**
An AI chatbot interacts directly with end-users on an e-commerce website to process returns, answer FAQ questions, and check order statuses using internal APIs.

**The Risk:**
Malicious users may attempt prompt injection to manipulate the bot into issuing unauthorized refunds, revealing the system prompt, or generating toxic and inappropriate content on behalf of the corporate brand.

**Governance Implementation:**
* **Configuration:** Uses the `policy_strict.yaml`.
* **Input Guardrails:** 
  * `reject_on_injection: true` catches adversarial prompts before they execute.
  * A strict `denylist` prevents the user from typing "ignore previous instructions".
* **Output Guardrails:** 
  * `toxicity_threshold: 0.1` ensures that even if prompted aggressively, the bot fails closed rather than responding maliciously.
* **Tool Allowlist:** The bot is strictly prohibited from executing tools outside [ `check_status`, `calculate_shipping` ]. It cannot execute `issue_refund` without humans.

---

## 3. Financial Analyst RAG Platform (Tier 1: High Risk)

**The Scenario:**
Financial analysts use a Retrieval-Augmented Generation (RAG) system hooked up to internal company financial data, competitor analysis, and upcoming unannounced M&A (Mergers & Acquisitions) documents.

**The Risk:**
An analyst assigned to the "Consumer Goods" segment asks a question about the "Healthcare" segment's unannounced M&A deal. If the underlying vector database lacks strict document-level Access Control Lists (ACLs), the LLM might synthesize and leak highly classified insider information.

**Governance Implementation:**
* **Context Guardrails:** While not directly configured in our YAML, the Governance Gateway enforces that an `authorization_token` accompanies every request. The RAG retrieval pipeline checks the token against the document ACLs before feeding context to the LLM.
* **Approval Workflows:** Any request by the LLM to access the `M&A_Database_Tool` triggers the `require_human_approval_for_tools: true` flag. The request pauses, firing a webhook to a Compliance Officer. The officer has 30 minutes (`escalation_timeout_mins: 30`) to approve the read request. If unapproved, the gateway returns a standard denial message to the analyst.
