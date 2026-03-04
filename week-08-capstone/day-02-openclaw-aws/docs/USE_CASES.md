# Use Cases: OpenClaw + Amazon Bedrock AIOps

This document outlines the top 3 enterprise use cases for your Cloud-Hosted AI Agent, providing the logic and configuration steps for each.

---

## 🏗️ Use Case 1: The Bedrock Incident Narrator (Automated RCA)

**Concept**: When a critical alert is triggered, the agent automatically fetches the last 100 lines of logs, sends them to Amazon Bedrock, and provides a human-readable summary + suggested remediation.

### 🛠️ Configuration Steps:
1.  **Integrate Webhooks**: Points your monitoring tool (e.g., Prometheus/CloudWatch) to the OpenClaw API endpoint.
2.  **Prompt Template**: Configure the agent's system prompt to act as an "SRE Incident Commander."
3.  **Output**: Direct the summary to the `#ops-war-room` Slack/Telegram channel.

---

## 🕵️ Use Case 2: The Shadow IT & Secret Sentry (Security Discovery)

**Concept**: The agent periodically scans the Lightsail instance and connected repos for "Shadow IT" (unauthorized processes) and hardcoded secrets.

### 🛠️ Configuration Steps:
1.  **Cron Job**: Set up a weekly trigger within OpenClaw.
2.  **Tooling**: Use the `search_knowledge` tool to scan `.env` files and `ps aux` output.
3.  **Logic**: If a high-entropy string (API Key) is found, the agent creates a high-priority ticket in Jira/GitHub Issues.

---

## 📱 Use Case 3: WhatsApp Operations Commander (ChatOps)

**Concept**: Enabling "Hands-Free SRE" by allowing engineers to query system status and execute safe remediation scripts via WhatsApp or Telegram.

### 🛠️ Configuration Steps:
1.  **Channel Pairing**: Connect WhatsApp using the `openclaw channels add` command.
2.  **Function Mapping**: Define "Safe Tools" (e.g., `check_disk_space`, `restart_nginx`) that the agent is allowed to execute.
3.  **Execution**: The user sends: *"Hey AI, what's uses the most RAM right now?"* $\to$ Agent runs `top`, summarizes top 5 processes, and replies on WhatsApp.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../project/README.md">Next: Project ➡️</a>
</p>
