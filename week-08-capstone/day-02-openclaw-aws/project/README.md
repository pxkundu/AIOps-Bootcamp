# Project: The Autonomous AWS SRE (OpenClaw + Bedrock)

Build an end-to-end AIOps Cloud Agent using the official **AWS Lightsail OpenClaw Blueprint** and **Amazon Bedrock**.

---

## 🏗️ Step 1: Create the OpenClaw Instance

1.  **Launch**: Go to the [AWS Lightsail Console](https://lightsail.aws.amazon.com).
2.  **Config**:
    *   **Platform**: Linux/Unix.
    *   **Blueprint**: **OpenClaw**.
    *   **Plan**: 4 GB RAM (Recommended for Bedrock/Claude performance).
3.  **Deploy**: Choose a unique name and click **Create Instance**. Wait for the status to show **Running**.

---

## 💻 Step 2: Pair Your Browser

1.  **SSH**: Click **Connect using SSH** in the Lightsail instance dashboard.
2.  **URL**: Locate the **Dashboard URL** in the welcome message. Open it in a new tab.
3.  **Token**:
    *   Copy the **Access Token** from the terminal.
    *   Paste it into the **Gateway Token** field in the dashboard.
4.  **Confirm**: Type `y` in the terminal to continue pairing, then `a` to approve.

---

## 🧠 Step 3: Enable AI with Amazon Bedrock

Your agent needs permissions to "think" using AWS models.

1.  **Script**: In the **Getting Started** tab of your Lightsail instance, locate "Enable Amazon Bedrock" and click **Copy the script**.
2.  **CloudShell**: Click **Launch CloudShell** next to the script.
3.  **Execute**: Paste the script and hit Enter. Once it says `Done`, your instance has an IAM Role that can talk to Bedrock.
4.  **FTU**: Ensure you have granted model access for **Anthropic Claude 3.5 Sonnet** in the Bedrock console.

---

## 📱 Step 4: Connect Messaging Channels (Optional)

1.  **CLI**: In the SSH terminal, run: `openclaw channels add`.
2.  **Telegram**:
    *   Create a bot via `@BotFather`.
    *   Paste the bot token in the CLI.
    *   Approve the pairing via `openclaw pairing approve telegram [pairing-code]`.
3.  **WhatsApp**:
    *   Select WhatsApp in the CLI.
    *   Scan the QR code with your phone (Linked Devices).

---

## 🛡️ Step 5: Snapshots & Backup

1.  **Navigate**: Go to the **Snapshots** tab of your instance.
2.  **Create**: Take a manual snapshot of your fully configured agent.
3.  **Auto**: Enable **Automatic Snapshots** to ensure you don't lose your AIOps context during a crash.

---

## ⚡ Step 6: Configuring the AIOps Use Cases

Once your agent is paired and Bedrock is active, configure these top 3 enterprise workflows:

### 1. The Bedrock Incident Narrator (RCA)
*   **Goal**: Automatically summarize errors from `/var/log/syslog`.
*   **Step**: In the OpenClaw Dashboard, add a new **Skill** called `LogNarrator`.
*   **Link**: Point the skill to `src/aiops_tools/power_tools.py` $\to$ `summarize_incident_logs`.
*   **Test**: Type: *"Summarize the last 50 errors in syslog"* on WhatsApp.

### 2. The Cloud Secret Sentry (Security)
*   **Goal**: Prevent credential leaks in your Lightsail scripts.
*   **Step**: Add a **Cron Trigger** in OpenClaw set to `0 0 * * 0` (Weekly).
*   **Action**: Execute `secret_scan(directory="/var/www/html")`.
*   **Outcome**: The agent will scan your web files and DM you on Telegram if it finds a loose API key.

### 3. WhatsApp Ops Commander (ChatOps)
*   **Goal**: Query system vitals on the go.
*   **Step**: Ensure your WhatsApp channel is paired.
*   **Interaction**: Text your bot: *"How is the server doing?"* 
*   **Execution**: The agent will run `check_vitals`, see the 95% RAM usage from a runaway process, and reply: *"Warning: 'nginx' is consuming high memory. Should I restart it?"*

---

<p align="center">
  <a href="../../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../resources/RESOURCES.md">Next: Resources ➡️</a>
</p>
