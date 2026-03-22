# ⚡ The Relay Race: Week 5 Day 3

> **System Alert:** Your Triage Bot (Day 2) is smart, but it's slow. It runs every minute. In high-frequency trading or security, a minute is an eternity. You need **Instant Reflexes**.

---

## 🎮 Phase 1: The Pre-Game (The Polling Trap)

**Scenario:**
You monitor a payment gateway.
- **12:00:01 PM:** Transaction fails.
- **Your Script:** `while True: check_logs(); time.sleep(60)`
- **12:01:00 PM:** Script wakes up, checks logs, and restarts service.
- **Result:** 59 seconds of downtime. Customers lost.

**The Lesson:**
**Polling** (asking "Are we there yet?") scales poorly and introduces latency.
**Event-Driven** (shouting "ERROR!") is instant and scalable.

**Your Inventory (Unlocked for Day 3):**
- 🎣 **The Webhook:** A digital doorbell.
- ⚡ **The Lambda:** Code that sleeps until woken (Serverless).
- 🚌 **The Event Bus:** A router that sends "Fire" alerts to the Fire Dept, and "Flood" alerts to the Plumber.

---

## 🎮 Phase 2: The Verification Game ("The Reactor")

**Objective:**
We will fire high-speed alerts at your system. You must catch and remediation them within **50 milliseconds**.

| Level | Method | Latency | Result |
|---|---|---|---|
| **1. The Snail** | File Polling (sleep 1s) | ~500ms | ❌ FAIL |
| **2. The Reflex** | Flask API (Webhook) | ~10ms | ✅ PASS |
| **3. The Filter** | Ignore INFO events | ~1ms | ✅ PASS |

**Win Condition:**
Run `python project/reactor_simulation.py`.
It sends a POST request with payload `{"event": "db_crash"}`.
Your `receiver.py` must restart the mock-db and return `{"status": "fixed"}` instantly.

**Reward:**
Unlocks **Day 4: Reinforcement Learning** (The Self-Driving System).

---

## 🚀 How to Start

1.  **Study:** Read [Lecture Notes: Event Driven Architecture](lecture-notes.md).
2.  **Equip:** Copy the Flask template from [Cheat Sheet](cheatsheet.md).
3.  **Practice:** See the huge delay difference in [Exercise 01](exercises/exercise-01-polling-vs-webhook.md).
4.  **Wiring:** Build the `Reactor` in the [Project](project/README.md).
