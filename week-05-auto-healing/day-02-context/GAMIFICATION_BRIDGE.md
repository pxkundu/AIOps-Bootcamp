# 🏥 The Triage Tent: Week 5 Day 2

> **System Alert:** Yesterday you learned to restart servers blindly (Rule-Based). Today, that blindness will cost you. A backup server is running hot. If you restart it, you lose the data. You must learn **Context**.

---

## 🎮 Phase 1: The Pre-Game (The Malpractice Suit)

**Scenario:**
You deployed your Auto-Restarter (Day 1) to production.
- **Tuesday 02:00 AM:** The Database CPU spiked to 95% (as expected during backup).
- **Your Script:** "CPU > 90%! RESTARTING!"
- **Result:** Backup corrupted. Data lost. CIO is furious.

**The Lesson:**
A symptom (High CPU) is not a diagnosis. To cure correctly, you need **Context** (Time of day, recent deployments, disk I/O).

**Your Inventory (Unlocked for Day 2):**
- 🌳 **The Decision Tree:** A logic map that asks questions before acting.
- 🕵️ **The Feature Extractor:** Tools to check "Is it Backup Window?", "Was there a deploy?", "Is disk full?".
- 🤖 **The Scikit-Learn Brain:** Training a model on past incidents to learn the correct response automatically.

---

## 🎮 Phase 2: The Verification Game ("The Smart Doctor")

**Objective:**
Patients (Incidents) are arriving. You must write a script (`doctor.py`) that diagnoses them and prescribes the correct cure.

| Patient | Symptoms | Context | Correct Cure |
|---|---|---|---|
| **1. The Runner** | CPU 99% | User Process | **Kill Process** |
| **2. The Archivist** | CPU 99% | Process = 'backup_job' | **Ignore (Do Nothing)** |
| **3. The Leaker** | RAM 95% | Uptime > 24h | **Restart Service** |
| **4. The Victim** | RAM 95% | Uptime < 5m | **Rollback Deploy** |

**Win Condition:**
Run `python project/triage_simulation.py`.
It will send 10 random incidents. You satisfy the Hippocratic Oath ("First, do no harm") by achieving **100% Accuracy**.

**Reward:**
Unlocks **Day 3: Event-Driven Automation** (Webhooks & FaaS).

---

## 🚀 How to Start

1.  **Study:** Read [Lecture Notes: Smart Triage](lecture-notes.md).
2.  **Equip:** Check [Cheat Sheet](cheatsheet.md) for Decision Tree logic.
3.  **Practice:** Build a manual tree in [Exercise 01](exercises/exercise-01-manual-tree.md).
4.  **Automate:** Train an ML tree in [Exercise 02](exercises/exercise-02-sklearn-tree.md).
5.  **Save Lives:** Build the `Smart Doctor` in the [Project](project/README.md).
