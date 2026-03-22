# Week 7 Day 6: The AIOps Survival Game 🎮

> **Duration:** 8 hours | **Format:** Game-Based Simulation
> **Theme:** High-Stakes Incident Response Strategy

---

## 🕹️ Game Objective: "Save Cyber Monday"

Welcome, Incident Commander! It's the biggest shopping day of the year. Your infrastructure is melting, your users are angry, and your budget is shrinking. 

You have **7 days of AIOps training** behind you. Today, you won't write a lecture—you will **survive the surge**.

---

## 📜 How to Play

The game is a **Decision-Tree Simulation**. Every action you take has a cost in **Budget**, **User Trust**, and **Latency**.

### Your Inventory:
1. **The Ansible Runbook**: Fixed cost, high speed, risk of breaking things if state is wrong.
2. **The LLM Agent**: High cost (API tokens), slow (reasoning time), but highly accurate RCA.
3. **The Circuit Breaker**: Passive tool. Prevents catastrophic loops but might leave services down.
4. **Manual Intervention**: Zero dollar cost, but HUGE loss in User Trust (long wait times).

### Your Stats:
- **User Trust**: 100% $\to$ If hits 0%, you are fired.
- **Budget**: $5,000 $\to$ Every LLM call costs $50. Every outage minute costs $500.
- **System Health**: Green $\to$ Yellow $\to$ Red $\to$ 🔥

---

## 🗺️ Levels of the Game

### Level 1: The "Log Storm"
A minor latency spike triggers 5,000 logs/second.
- **Option A**: Send all logs to LLM for RCA. ($$$)
- **Option B**: Run the "Disk Cleanup" Ansible script blindly. (Risk of data loss)
- **Option C**: Do nothing and wait for more data. (Latency increases)

### Level 2: The "Heisenbug"
A service is crashing repeatedly. Your simple restarter is in an infinite loop.
- **Strategy**: Do you have a **Circuit Breaker** enabled? 
- If YES: The loop breaks, you lose 10% Trust, but save $2,000 in CPU costs.
- If NO: The system crashes your entire node. **GAME OVER**.

### Level 3: The "ChatOps War Room"
Multiple stakeholders are asking for updates in Slack.
- **Action**: Use your **Incident Summarizer** (Day 3) to keep them calm.
- **Impact**: Increases User Trust by 20%, costs $100 in tokens.

---

## ✅ Deliverables

1. **A Game Log**: Run the `aiops_survival.py` simulator and reach the end of the "Cyber Monday" shift with > 50% User Trust.
2. **Strategy Reflection**: Write a one-page report on why you chose "Automation" over "Manual" at minute 30.
3. **The Fix**: Identify one bug in the simulator's "Circuit Breaker" logic and patch it.

---

<p align="center">
  <a href="../day-05-chatops/lecture-notes.md">⬅️ Back: Day 5</a> | <strong>Day 6: AIOps Game</strong> | <a href="../day-07-capstone/README.md">Next: Final Capstone ➡️</a>
</p>
