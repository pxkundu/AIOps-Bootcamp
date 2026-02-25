# Week 7: Auto-Remediation & Incident Intelligence

> **Theme:** Closing the loop with automated response

---

## 🎯 Learning Objectives

By the end of this week, you will:

1. Build automated remediation runbooks with Ansible/Python
2. Integrate LLMs for incident analysis and summarization
3. Create ChatOps bots for operations
4. Implement Kubernetes self-healing patterns

---

## 📅 Daily Schedule

| Day | Topic | Duration |
|-----|-------|----------|
| 1 | [Runbook Automation & Ansible](day-01-runbooks/) | 8 hours |
| 2 | [Self-Healing Loops & Circuit Breakers](day-01-runbooks/) | 8 hours |
| 3 | [LLM-powered RCA & Summarization](day-02-llm/) | 8 hours |
| 4 | [Building LLM Incident Agents](day-02-llm/) | 8 hours |
| 5 | [ChatOps: Slack & Microsoft Teams](day-03-chatops/) | 8 hours |
| 6 | [Interactive Remediation Bots](day-03-chatops/) | 8 hours |
| 7 | [Kubernetes Self-Healing (KEDA)](day-04-k8s/) | 4 hours |

---

## 🛠️ Technologies Covered

- **Ansible** - Automation framework
- **OpenAI/Claude APIs** - LLM integration
- **LangChain** - LLM orchestration
- **Slack SDK** - ChatOps
- **Kubernetes** - HPA, KEDA, custom controllers

---

## ✅ Deliverables

- [ ] Automated remediation runbooks
- [ ] LLM-powered incident summarizer
- [ ] ChatOps bot for operations
- [ ] Week 7 quiz completed

---

## 🔑 Key Concepts

### Remediation Levels
```
Level 0: Manual → Human does everything
Level 1: Assisted → Bot suggests actions
Level 2: Semi-Auto → Bot executes with approval
Level 3: Auto → Bot executes autonomously (safe ops)
```

### LLM for AIOps Use Cases
| Use Case | Implementation |
|----------|---------------|
| Incident summarization | Summarize logs/alerts |
| RCA suggestions | Analyze patterns |
| Runbook generation | Convert docs to code |
| Natural language queries | "What caused the outage?" |

---

---

<p align="center">
  <a href="../week-06-alerting/master-project/README.md">⬅️ Back: Week 6</a> | <strong>Week 7 Overview</strong> | <a href="../week-08-capstone/README.md">Begin Week 8 ➡️</a>
</p>
