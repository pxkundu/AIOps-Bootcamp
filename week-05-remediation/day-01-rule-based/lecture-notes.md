# Week 5 Day 1: Rule-Based Remediation (Self-Healing)

> **Duration:** 8 hours | **Difficulty:** Intermediate  
> **Focus:** Replacing Human Runbooks with Code (Bash, Python).

---

## 🏗️ Part 1: Eliminating Toil

**Toil** is manual, repetitive, automatable work that lacks enduring value.
- Restarting a server.
- Cleaning up log files.
- Resizing disk partitions.

**The Goal:** Every incident should lead to an automation that prevents *human* intervention next time.

---

## 📜 Part 2: Runbooks as Code

A **Runbook** is a document telling you "Steps to Restart DB".
A **Remediation Script** is that document, executed by a machine.

### Level 1: Bash (The Hammer)
Good for simple, single commands.
```bash
#!/bin/bash
if systemctl is-active --quiet nginx; then
    echo "Nginx is running"
else
    systemctl restart nginx
    echo "Restarted Nginx"
fi
```

### Level 2: Python (The Scalpel)
Good for logic, API calls, and complex checks.
```python
import psutil
import requests

# Check if process exists AND is responding 200 OK
def check_health():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'nginx':
            try:
                r = requests.get('http://localhost')
                return r.status_code == 200
            except:
                return False
    return False
```

---

## ⚡ Part 3: Safety Mechanisms (Crucial!)

Automated remediation is dangerous. If you restart a database every second, you destroy the data.

### 1. Idempotency
Running a script 100 times should have the same effect as running it once.
- **Bad:** `echo "line" >> config.txt` (Appends 100 times).
- **Good:** Check if `line` exists before appending.

### 2. Exponential Backoff
Don't restart immediately. Wait.
- Attempt 1: Wait 1s.
- Attempt 2: Wait 2s.
- Attempt 3: Wait 4s.
- Attempt 4: Wait 8s.

### 3. Circuit Breakers
If remediation fails N times, **Stop** and page a human.
Do not enter an infinite loop of death.

---

## 🛠️ Part 4: Tools of the Trade

1.  **psutil (Python):** Inspect CPU, RAM, Disk, Processes.
2.  **subprocess (Python):** Run shell commands from Python.
3.  **Ansible:** Configuration Management (Fix drift).
    - `ansible-playbook fix_webserver.yml`
4.  **StackStorm:** Event-driven automation platform (IF trigger THEN action).

---

## 🔗 Next Steps

1.  Open the [Cheat Sheet](cheatsheet.md) for remediation snippets.
2.  Practice process killing in [Exercise 01](exercises/exercise-01-scripting.md).
3.  Build "The Auto-Restarter" in the [Project](project/README.md).
