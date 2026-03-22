# Exercise 01: The Safety Audit

## 🎯 Objective
Analyze the behavior of **Project Aegis** under pressure and identify "unsafe" or inefficient remediation decisions.

---

## 🛠️ Step 1: Run the Siege
1.  Start the Aegis Gateway: `python src/app.py`
2.  Start the Chaos Monkey: `python simulation/chaos_monkey.py`
3.  Let it run for 5 minutes.

## 🛠️ Step 2: The Audit
Extract the logs from your `AegisEngine.history` (or the console output).

**Analyze the following:**
1.  **Duplicate Actions:** Did Aegis try to restart the same service multiple times within 10 seconds? If so, why didn't the first one fix it?
2.  **Backup Integrity:** Check the logs for `cpu_spike` on `database`. Did Aegis correctly ignore it if the computer clock was between 02:00 and 04:00?
3.  **The Unkown:** How many times did Aegis return `ESCALATED`? Are there patterns in those unhandled events that could be turned into a new runbook?

## 🛠️ Step 3: Hardening
Modify `src/engine.py` to add a **Rate Limit** to the restart healer. 
*Requirement:* A service should not be restarted more than once every 60 seconds.

## 📝 Deliverable
An updated `engine.py` with the "Restart Rate-Limit" implemented.
