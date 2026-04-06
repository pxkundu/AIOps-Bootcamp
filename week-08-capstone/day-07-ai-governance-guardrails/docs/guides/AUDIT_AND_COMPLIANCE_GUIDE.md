# Audit & Compliance Guide for Enterprise AI

When deploying Generative AI models into production, adhering to regulatory standards (SOC2, HIPAA, GDPR, ISO 27001) shifts from a legal requirement to an engineering architecture challenge. This guide explains how to construct an auditable AI perimeter.

---

## 1. Defining the AI Audit Trail

Every interaction with an LLM in an enterprise environment must be recorded. However, simply logging "Input X yielded Output Y" is insufficient and often dangerous (as it copies PII into log files).

### Essential Audit Data Points (The AI Event Log)
* **Metadata Check:** Timestamp, Session ID, User ID, and IP Address.
* **Traceability:** Model Name, Model Version, and Temperature used.
* **Safety Evaluation:** Was a guardrail triggered? Which policy was evaluated (e.g., `policy_strict.yaml` v1.2)? Is the request blocked?
* **Tool Execution Details:** If the LLM requested database access, which query was executed and under whose permissions?

### Masking the Payload
Do not log raw PII into your SIEM tools (Splunk, Datadog, CloudWatch).
1. Configure your logging to drop sensitive payloads.
2. If compliance requires raw logs for investigation, store raw inputs/outputs in an encrypted, tightly restricted S3 bucket with strict TTL (Time to Live) retention policies (e.g., delete after 30 days), separated from operational logging.

---

## 2. Risk Tiers and Compliance Controls

Not all AI apps share the same risk. Engineering teams should classify applications into tiers to avoid over-engineering.

* **Tier 1: High Risk (Customer Facing / Financial)**
  * **Controls:** Strict input/output guardrails, mandatory data masking, synchronous dual-control approvals for model updates, permanent audit logs.
  * *Example:* An AI bot advising on mortgage applications.
* **Tier 2: Medium Risk (Internal PII Processing)**
  * **Controls:** PII redaction output guardrails, authenticated RBAC (Role-Based Access Control).
  * *Example:* HR assistant reviewing internal employment records.
* **Tier 3: Low Risk (Utility)**
  * **Controls:** Standard length constraints, rate limiting, no PII checking required.
  * *Example:* Internal code-generation assistant without customer data access.

---

## 3. Designing for Audits

When external auditors arrive (e.g., for a SOC2 Type II audit), they will ask for "Proof of Control."

### 3.1 Prove that policies are enforced
**The Answer:** Architect the network so that it is impossible to call the LLM directly. All API keys for OpenAI/AWS Bedrock must be isolated inside the Governance Gateway. If a developer attempts to bypass the gateway, the key will not be exposed to them.

### 3.2 Prove that models do not leak data
**The Answer:** Demonstrate the output sanitization pipeline (like Presidio). Provide the configuration file (`audit_logging_config.json`) proving that raw inputs are obfuscated and model retention policies are set to zero/opt-out.

### 3.3 Incident Response integration
**The Answer:** Show automated alerts tied to the Gateway. E.g., "If we detect 10 prompt injection attempts from a specific User ID in 1 minute, their token is revoked automatically via Okta, and a PagerDuty alert fires."

---

## 4. Automating Compliance Reviews

Use the provided `run_audit_report.py` script as a baseline to parse your exported JSONL logs. Run these reports weekly to review blocked requests. Often, a high block rate indicates a need for better user training, rather than a malicious insider.
