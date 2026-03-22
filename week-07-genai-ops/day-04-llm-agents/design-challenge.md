# Agent Architect Design Challenge

**Name:** ____________________
**Agent Name:** ____________________
**Mission:** ____________________

---

### 🏛️ System Architecture

#### 1. Tool Definitions
List at least 3 tools your agent will have access to. Define their inputs and what they return.

| Tool Name | Input Parameters | Return Value |
|-----------|------------------|--------------|
| Example: `check_k8s_logs` | `pod_name` | `string (last 100 lines)` |
| | | |
| | | |

#### 2. The Persona (System Prompt)
Draft the character of your agent. How should it behave during a "Critical P0" vs a "Minor Flake"?
> *Tip: "You are a senior SRE who is concise, skeptical of noisy alerts, and prioritizes data evidence over guesses."*

#### 3. Handling Uncertainty
What should the agent do if Tool A returns an error (e.g., "Connection Timeout")?

---

### 🛡️ Guardrails & Safety

#### 1. Execution Policy
- [ ] Read-only tools only.
- [ ] Approval required for "Write" actions.
- [ ] Time-limited execution (Max 5 loops).

#### 2. Cost Control
How will you prevent the agent from entering an infinite loop and draining your API budget?

---

### 🧪 Test Scenarios

Define one "Happy Path" and one "Edge Case" for your agent.

**Happy Path:** 
Alert: "High Memory" -> Agent calls `get_top_mem_procs` -> Identifies leak -> Suggests restart.

**Edge Case:**
Alert: "Latancy Spike" -> Agent sees external dependency failure -> Realizes internal fixes won't work.
