# Exercise 02: Implementing a Circuit Breaker

## 🎯 Objective
Prevent your self-healing system from making a situation worse. If a service continues to fail after multiple remediation attempts, the system should "Trip" the circuit breaker and stop trying.

---

## 🛠️ The Scenario
Your `webapp` is crashing. Aegis restarts it. It crashes again. Aegis restarts it.
Without a circuit breaker, this will loop forever, pinning CPU and making logs unreadable.

## 🛠️ Task 1: Tracking Attempts
Modify `src/engine.py` (or create a new script) to maintain a counter for each type of remediation per service.

```python
# State store
remediation_counts = {
    'webapp': 0,
    'database': 0
}
RETRY_LIMIT = 3
```

## 🛠️ Task 2: Trip the Circuit
Before executing a healing action:
1.  Check the current count for that service.
2.  If `count >= RETRY_LIMIT`:
    - Refuse to run the healer.
    - Return `STATUS: CIRCUIT_BROKEN_ESCALATING_TO_HUMAN`.
3.  If `count < RETRY_LIMIT`:
    - Increment count and proceed with healing.

## 🛠️ Task 3: The Reset
Implement a "Reset" mechanism (e.g., if no failure is detected for 5 minutes, reset the count to 0).

## 📝 Deliverable
A Python script demonstrating the Circuit Breaker logic blocking a 4th consecutive restart request.
