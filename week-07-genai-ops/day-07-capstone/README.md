# Week 7 Day 7: Master Project — The Autonomous SOC

> **Duration:** 8 hours | **Format:** Final Build
> **Goal:** Link all Week 7 modules into one cohesive "Self-Healing Brain."

---

## 🏗️ The Challenge

You must build **The Autonomous SOC (Security Operations Center)**. This isn't just a script; it's a platform that:
1. **Detects anomalies** (Simulated alerts).
2. **Triages via LLM** (Generates an RCA & Narrative).
3. **Notifies via ChatOps** (Slack Card with buttons).
4. **Remediates via Ansible** (Executes the fix when a button is clicked).

---

## 🛠️ Requirements

Your final project must demonstrate these 4 "Levels of Intelligence":

### Level 1: Clean Data (Redaction)
The system must automatically strip PII from incoming logs before they hit your database or LLM.

### Level 2: Explanability (LLM Narrator)
When an incident happens, the system must generate a 3-bullet point summary explaining the "Why" and the "How".

### Level 3: Human-in-the-Loop (Interactive)
Remediation should NOT be 100% blind. It should present an "Approval Button" to a human in Slack.

### Level 4: Self-Verification
After a fix is applied, the system must check the "World State" again to confirm the alert has cleared.

---

## 📂 Project Structure

- `/src/ingestor.py` -> Receives raw telemetry.
- `/src/narrator.py` -> The LLM-powered logic.
- `/src/slack_interface.py` -> The UI.
- `/src/playbooks/` -> Your Ansible logic.

---

## ✅ Graduation Criteria

- [ ] Successful demo: "Alert Injected" $\to$ "Slack Card Appears" $\to$ "Button Clicked" $\to$ "System Fixed."
- [ ] A 10-minute video or interactive walkthrough showing the OODA loop in action.
- [ ] Code properly documented and pushed to your personal AIOps portfolio.

---

<p align="center">
  <a href="../day-06-game/game-guide.md">⬅️ Back: Day 6</a> | <strong>Week 7 Complete</strong> | <a href="../../week-08-capstone/README.md">Go to Week 8 ➡️</a>
</p>
