# Week 7 Day 2: Self-Healing Loops & Circuit Breakers

> **Duration:** 8 hours | **Difficulty:** Intermediate+
> **Focus:** Building robust, stateful automation that knows when to stop.

---

## 🎯 Learning Objectives

By the end of this session, you will:
1. Implement a **Stateful Remediator** that tracks fix attempts across restarts.
2. Build a **Circuit Breaker** to prevent "Infinite Remediation Loops".
3. Implement **Post-Remediation Verification** (The "Trust but Verify" pattern).
4. Understand **Remediation Flapping** and how to suppress it.

---

## 📖 Lecture Content

### 1. The Statefulness Problem
In Day 1, our remediator was "Stateless". If an alert stayed active, it would keep running the fix every 5 seconds.
**Problem:** If the fix is failed (e.g., disk is full of un-deletable files), the script will loop forever, wasting CPU and potentially hiding a deeper issue.

### 2. The Remediation Circuit Breaker
Just like a fuse in your house, a **Remediation Circuit Breaker** "trips" (stops) when it detects a failure pattern.

**States of a Circuit Breaker:**
- **Closed (Healthy)**: Remediation runs normally.
- **Open (Tripped)**: Too many failures/attempts. Remediation is DISABLED. Alerts are escalated to humans.
- **Half-Open (Testing)**: Attempt a fix one more time after a timeout.

### 3. Verification: The Final Step
Executing a command (e.g., `systemctl restart nginx`) is not a success. Success is when the **Metrics** return to normal.

**The Verification Loop:**
1. Run Fix.
2. Wait 30 seconds (Cooldown).
3. Check Metric (e.g., Latency < 200ms).
4. If Metric is bad $\implies$ Fix Failed $\implies$ Increment Failure Counter.

---

## 🛠️ Design: The Smart Remediator

We represent our remediation logic as a Class that maintains state in-memory or in a small database (SQLite/Redis).

```python
class SmartRemediator:
    def __init__(self):
        self.attempts = {} # {alert_id: count}
        self.MAX_ATTEMPTS = 3
        
    def should_act(self, alert_id):
        count = self.attempts.get(alert_id, 0)
        return count < self.MAX_ATTEMPTS

    def mark_failure(self, alert_id):
        self.attempts[alert_id] = self.attempts.get(alert_id, 0) + 1
        if self.attempts[alert_id] >= self.MAX_ATTEMPTS:
            print(f"🚨 CIRCUIT BREAKER TRIPPED for alert {alert_id}")
```

---

## ✅ Deliverables for Today

- [ ] A Python script `smart_controller.py` that implements a failure-counting circuit breaker.
- [ ] A simulated "Service Crash" scenario where the fix (restart) fails to solve the problem.
- [ ] Log output showing the Circuit Breaker moving from "Closed" to "Open".

---

## 📚 Additional Resources

- [Deep Dive: Resilience Patterns](resources/RESOURCES.md)
- [Circuit Breaker in Distributed Systems](https://martinfowler.com/bliki/CircuitBreaker.html)

---

<p align="center">
  <a href="../day-01-runbooks/lecture-notes.md">⬅️ Back: Day 1</a> | <strong>Day 2: Self-Healing Loops</strong> | <a href="../day-03-llm/lecture-notes.md">Next: Day 3 ➡️</a>
</p>
