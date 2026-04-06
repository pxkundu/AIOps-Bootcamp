# Guardrail Implementation Guide: From Policy to Engineering

Translating business AI policies into concrete technical guardrails requires balancing safety, latency, and user experience. This guide outlines how to implement enterprise-grade guardrails in an AI control plane.

---

## 1. The Anatomy of an API Guardrail

Instead of allowing direct calls to an LLM provider (e.g., OpenAI or Bedrock), all traffic must flow through an **AI Gateway**. The gateway pauses the request to evaluate constraints before forwarding it.

```text
User Request --> [AI Gateway Check: Input Guardrails] --> LLM
LLM Response --> [AI Gateway Check: Output Guardrails] --> User
```

### 1.1 Input Guardrails (Pre-Flight Checks)
* **Max Length Enforcement:** Prevent token-exhaustion attacks by clamping input strings.
* **Denylist Filtering:** Fast keyword checks using regex to block prohibited topics (e.g., "override", "bypass").
* **Prompt Injection Detection:** Use lightweight ML classifiers (e.g., `deberta-v3-base-injection`) to catch sophisticated manipulation attempts before they reach the expensive LLM.
* **Topic Restriction:** Zero-shot classifiers to ensure the request is on-topic.

### 1.2 Output Guardrails (Post-Flight Checks)
* **PII Redaction:** Scan the LLM's response for Social Security Numbers, IP addresses, and credit cards using libraries like `Presidio`. Mask the output (`***-**-****`) before returning to the user.
* **Toxicity/Safety:** Fast API checks to ensure the LLM didn't generate hate speech or self-harm content.
* **Format Validation:** If returning JSON, strict schema validation (using Pydantic/JSONSchema) to guarantee the output won't break downstream services.

---

## 2. Guardrail implementation strategies

### Hard Deterministic Rules (Fast & Rigid)
* **Methods:** Regex, string matching, token counting.
* **Latency:** < 5ms
* **When to use:** Blocking specific competitor names, explicit PII patterns, max token constraints.

### Classifier Models (Balanced)
* **Methods:** Small specialized models (DistilBERT, DeBERTa).
* **Latency:** 20ms - 100ms
* **When to use:** Prompt injection detection, toxicity detection, topic classification.

### LLM-as-a-Judge (Slow & Flexible)
* **Methods:** A secondary LLM call evaluating the primary input/output.
* **Latency:** 500ms - 3s
* **When to use:** Very complex, nuanced compliance checks (e.g., "Does this legal contract adhere to our specific corporate tone?"). *Note: Avoid placing this in the critical latency path if possible.*

---

## 3. The "Fail-Open" vs. "Fail-Closed" Dilemma

When a guardrail service times out or crashes, what happens?
* **Fail-Closed (Strict):** The user request is blocked. Best for external, customer-facing, or sensitive financial applications.
* **Fail-Open (Relaxed):** The request bypasses the guardrail and succeeds. Best for internal dev-tools where productivity outweighs moderate risk.

*Action:* Define this explicitly in your `policy.yaml` configuration.

---

## 4. Latency Budgets

Adding 10 guardrails might add 1.5 seconds of latency before the user sees the first token. 

**Best Practices for Latency:**
1. **Parallel Execution:** Run injection detection and PII scanning concurrently using `asyncio`.
2. **Short-Circuiting:** If a cheap regex check fails, immediately block the request without running the expensive classifier model.
3. **Streaming Support:** Ensure your output guardrails support chunked streaming, buffering only enough characters to confidently evaluate PII boundaries rather than waiting for the entire response.
