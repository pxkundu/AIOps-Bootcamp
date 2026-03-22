# 🏥 The Trauma Center: Week 5 Day 1

> **System Alert:** You have mastered Detection (Week 4). But detecting a fire doesn't put it out. The alarms are screaming, and the servers are dying. You must become **The First Responder**.

---

## 🎮 Phase 1: The Pre-Game (Runbook Hell)

**Scenario:**
You are the On-Call Engineer.
- **02:00 AM:** Pager goes off. "Database Unresponsive".
- **Action:** You wake up, SSH in, type `systemctl restart postgresql`.
- **02:15 AM:** Pager goes off again. Same error.
- **Action:** You restart it again.
- **02:30 AM:** Pager goes off...

This is **Toil**. Manual, repetitive work that scales linearly with system size.
You need **Automation**.

**Your Inventory (Unlocked for Day 1):**
- 📜 **The Bash Scroll:** Simple shell scripts for quick fixes.
- 🐍 **The Python Syringe:** Advanced logic (API calls, complex checks) to heal the system.
- 🤖 **The Ansible Droid:** Agentless config management to fix 100 servers at once.

---

## 🎮 Phase 2: The Verification Game ("The Auto-Restarter")

**Objective:**
We will launch 3 broken processes on your machine (simulated). You must write a script that:
1.  **Detects** if they are dead.
2.  **Restarts** them automatically.
3.  **Logs** the incident.

| Level | Due Date | The Injury | The Treatment (Day 1 Skill) |
|---|---|---|---|
| **1. The Zombie** | A process that hangs (State: 'Z'). | **Bash Script (kill -9)** |
| **2. The Leaker** | A process consuming > 500MB RAM. | **Python (psutil + kill)** |
| **3. The Flapper** | A service that restarts but crashes immediately. | **Backoff Logic (Wait before restart)** |

**Win Condition:**
Run `python project/trauma_center.py`.
The simulation will break services. Your `healer.py` must bring uptime to 99%.

**Reward:**
Unlocks **Day 2: Context-Aware Remediation** (Decision Trees).

---

## 🚀 How to Start

1.  **Study:** Read [Lecture Notes: Runbooks as Code](lecture-notes.md).
2.  **Equip:** Copy the snippets from [Cheat Sheet](cheatsheet.md).
3.  **Practice:** Fix a memory leak in [Exercise 01](exercises/exercise-01-scripting.md).
4.  **Save Lives:** Build the `Auto-Restarter` in the [Project](project/README.md).
