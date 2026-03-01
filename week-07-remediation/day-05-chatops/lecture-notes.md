# Week 7 Day 5: ChatOps — Slack & Microsoft Teams Integration

> **Duration:** 8 hours | **Difficulty:** Intermediate
> **Focus:** Bringing AIOps intelligence to where the engineers already are: The Chat Window.

---

## 🎯 Learning Objectives

By the end of this session, you will:
1. Understand the philosophy of **ChatOps** (Conversational Infrastructure).
2. Learn how to bridge the gap between **Monitoring Tool Alerts** and **Interactive Chat Messages**.
3. Use the **Slack SDK** to build an alert triage bot.
4. Implement **Interactive Components** (Buttons/Modals) for 1-click remediation.

---

## 📖 Lecture Content

### 1. What is ChatOps?
ChatOps is a collaboration model that connects people, tools, process, and automation into a transparent workflow. 
Instead of logging into a CLI or a dashboard, you talk to a Bot in Slack/Teams to perform operations.

**Key Benefits:**
- **Shared Context:** Everyone in the channel sees the bot's analysis and the engineer's response.
- **Onboarding:** Senior engineers "show" juniors how to debug by typing commands in the common channel.
- **Audit Trail:** The chat history becomes the post-mortem timeline.

### 2. The Alert Pipeline: "Noise to Signal"
A good ChatOps bot doesn't just dump raw JSON into a channel. It follows the **Triage Rule**:
1. **Receive Webhook:** From Prometheus/Datadog.
2. **Enrich:** Add links to the specific dashboard and the RCA summary from Day 3.
3. **Notify:** Post a formatted card to Slack.
4. **Interact:** Provide a "Silence" and "Restart Service" button on the card.

### 3. Slack Building Blocks
Slack uses **Block Kit** to build rich interfaces.
- **Section:** For text and descriptions.
- **Context:** For small metadata (e.g., "Triggered by engine-01").
- **Actions:** For buttons, menus, and date pickers.

### 4. Security: The Bot's Identity
**CRITICAL:** ChatOps bots have "Write" access. 
- Use **RBAC** (Role Based Access Control): Only certain users should be able to click the "Restart Production" button.
- Use **Signed Secrets**: Verify that the button click actually came from Slack, not a malicious script.

---

## 🛠️ Implementation: The "AIOps Sentinel" Bot

We will use the **Slack Bolt framework** for Python. It handles the threading and event listening for us.

---

## ✅ Deliverables for Today

- [ ] A conceptual flow of an interactive alert triage process.
- [ ] A Python script `slack_bot.py` that listens for a simulated webhook and posts a "Remediation Card".
- [ ] A set of button handlers that "simulate" running the Ansible playbooks from Day 1.

---

<p align="center">
  <a href="../day-04-llm-agents/workshop-guide.md">⬅️ Back: Day 4</a> | <strong>Day 5: ChatOps</strong> | <a href="../day-06-remediation-bots/lecture-notes.md">Next: Day 6 ➡️</a>
</p>
