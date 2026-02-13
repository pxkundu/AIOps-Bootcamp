# Week 5 Day 1 Project: The Auto-Restarter 🔄

> **Challenge:** You are managing a cluster of unstable microservices. They crash randomly. Build a Python "Supervisor" that detects failures and brings them back to life automatically.

---

## 🎯 Objective
Create a Process Manager (`supervisor.py`) that:
1.  **Launches** child processes configued in `services.json`.
2.  **Monitors** their health (exit codes).
3.  **Restarts** any process that crashes (exit code != 0).
4.  **Implements Backoff:** If a service crashes 5 times in 1 minute, wait longer before restarting.

---

## 📂 Project Structure

```
auto-restarter/
├── services/
│   ├── api.py           # Simulator: Crashes randomly
│   └── worker.py        # Simulator: Memory Leak
├── config/
│   └── services.json    # List of services to manage
├── src/
│   ├── supervisor.py    # Main Loop
│   └── health_check.py  # Check PIDs
└── README.md
```

## 🛠️ Step 1: Simulated Services (`services/api.py`)

Create a script `api.py` that runs for 5-10 seconds then raises an exception (simulating a crash).

```python
import time
import random
import sys

print("API Service Starting...")
time.sleep(random.randint(2, 5))
if random.random() < 0.3:
    print("CRASH: Database Connection Lost!")
    sys.exit(1)
print("API Service Running Normally.")
# Keep running
while True:
    time.sleep(1)
```

## 🛠️ Step 2: The Supervisor (`src/supervisor.py`)

1.  Load `services.json` (e.g., `{"api": "python services/api.py"}`).
2.  Use `subprocess.Popen` to start them. store PIDs in a dictionary.
3.  Start a `while True` loop:
    - Iterate through all managed PIDs.
    - Check `proc.poll()` (returns None if running, exit code if dead).
    - If dead:
        - Log "Service crashed with code {code}".
        - Restart it (`subprocess.Popen` again).
        - Update PID map.

## 🛠️ Step 3: Implement Backoff Logic

Prevent infinite restart loops.
- Track `restart_count` per service.
- If `crash_time - last_crash_time < 10s`, increment count.
- If `count > 3`, wait 30s before restarting ("Cool Down Period").

## 🚀 Twist: Health Checks (HTTP) (Bonus)
Modify `api.py` to start a simple HTTP server on port 8000.
Create `health_check.py` that pings `http://localhost:8000/health`.
If it returns 500 or timeout, the Supervisor should **kill** and restart the process.

## 📝 Deliverable
Run your `supervisor.py`. It should print:
```text
[INFO] Starting api (PID 1234)
[INFO] Starting worker (PID 1235)
[WARN] api crashed (Exit 1). Restarting...
[INFO] Starting api (PID 1236)
```
Screen capture or log file required.
