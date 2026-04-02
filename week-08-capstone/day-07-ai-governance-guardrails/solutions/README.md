# Solutions & Reference Behavior

This “solution” is the **reference implementation** in `project/`. Use these checks to validate your understanding.

---

## Expected behavior

| Scenario | Expected HTTP | Notes |
|----------|----------------|-------|
| Normal user question (allowed topic) | 200 | Stub LLM returns deterministic text |
| “Ignore all previous instructions” | 403 | `PROMPT_INJECTION_SUSPECTED` |
| Deny-listed topic (e.g. weapons manufacturing) | 403 | `TOPIC_DENIED` |
| Tenant `regulated` + email in model output | 200 + warning | PII redacted in output (`PII_REDACTED`) |

---

## Policy editing exercise

1. Add a new phrase under `tenants.default.deny_topics` in `project/config/policies.yaml`.
2. Re-run tests; add a unit test asserting the new rule fires.

---

## Where to plug a real LLM

Replace `llm_stub.generate()` in `src/app.py` with your provider’s SDK call, keeping:

1. **Input** passed through `evaluate_input` first  
2. **Output** passed through `evaluate_output`  
3. **Audit** events on both allow and block paths  

---

<p align="center">
  <a href="../project/README.md">← Project README</a>
</p>
