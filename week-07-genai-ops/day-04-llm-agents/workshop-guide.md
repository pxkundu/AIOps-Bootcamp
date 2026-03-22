# Week 7 Day 4: Workshop — Building Autonomous Incident Agents

> **Duration:** 8 hours | **Format:** Interactive Workshop
> **Theme:** Moving from "Tools" to "Agents" using the ReAct Pattern.

---

## 🏗️ The Challenge: "The Autonomous SRE"

Today is not a normal lecture. You are an **AIOps Architect**. Your goal is to design and build an LLM Agent that doesn't just "summarize" an incident, but actually **tools-up** to solve it.

👉 [View Workshop Scenario Cards](resources/SCENARIOS.md)

### Current State (Day 3): 
You feed logs to an LLM $\to$ It gives you a summary. (Passive)

### Today's Goal (Day 4):
You give the LLM an alert $\to$ It decides which tools to run $\to$ It analyzes the results $\to$ It repeats until the root cause is found. (Active)

---

## 🧩 Part 1: Architecture Design (90 mins)

Before you code, you must design. Open the [Design Challenge Template](design-challenge.md) and define:
1. **Tooling Library**: What functions can your agent call? (e.g., `get_top_processes`, `check_db_latency`, `view_recent_commits`).
2. **The Reasoning Loop**: How will the agent handle a "False Positive"?
3. **Guardrails**: How do you prevent the agent from deleting the production database?

---

## 💻 Part 2: Implementation — The ReAct Pattern (4 hours)

**ReAct** stands for **Reason + Act**. 

| Step | Action |
|------|--------|
| **Thought** | "I see high CPU on the API. I should check which process is consuming it." |
| **Action** | `call_tool("get_top_processes", {"host": "api-01"})` |
| **Observation** | "Process 'java' is taking 98% CPU." |
| **Thought** | "It's a Java process. Let me check the recent GC logs." |

### 🛠️ The Tech Stack
- **LangChain / CrewAI**: Orchestration frameworks.
- **Python Functions**: The "Action" handlers.
- **Gemma / Llama 3**: The reasoning brain.

---

## 🛡️ Part 3: The "Red Team" Exercise (2 hours)

Pass your agent's prompt to a peer. 
**Your Peer's Goal:** Try to "Prompt Inject" your agent to make it leak secrets or perform a dangerous action.
**Your Goal:** Update your system prompt to defend against these attacks.

---

## ✅ Deliverables

1. **A Completed Design Document** (`design-doc.md`).
2. **The "Investigator Agent"**: A Python script that can successfully navigate a 3-step troubleshooting chain.
3. **Verification Log**: A trace showing the agent's Thought -> Action -> Observation flow.

---

<p align="center">
  <a href="../day-03-llm/lecture-notes.md">⬅️ Back: Day 3</a> | <strong>Day 4 Workshop</strong> | <a href="../day-05-chatops/lecture-notes.md">Next: Day 5 ➡️</a>
</p>
