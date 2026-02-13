# Exercise 01: The Memory Leak (Python Remediation)

## 🎯 Objective
Use Python (`psutil`) to proactively monitor and kill processes that are consuming excessive memory (Memory Leaks) before they crash the server (OOM Kill).

---

## 📊 The Simulation
First, create a script that simulates a bad application. It will slowly consume RAM until it crashes your machine (don't worry, we'll stop it before that).

Create `leak_simulator.py`:
```python
import time
import os

def create_leak():
    data = []
    print(f"Process {os.getpid()} starting memory leak...")
    while True:
        # Allocate 10MB strings
        data.append(' ' * 10 * 1024 * 1024)
        print(f"Allocated {len(data) * 10} MB")
        time.sleep(1)

if __name__ == "__main__":
    # Name the process so we can find it
    # On Linux/Mac:
    import setproctitle
    setproctitle.setproctitle("leaker_process")
    create_leak()
```
*(Note: You might need `pip install setproctitle`. If not available, just search by PID or filename.)*

## 🛠️ Task 1: Find the Leaker
Write a script `leak_stopper.py` that:
1.  Iterates through all running processes using `psutil`.
2.  Checks memory usage (`rss`).
3.  Finds any process named `leaker_process` (or just check PID if easier).
4.  Prints its memory usage in MB.

## 🛠️ Task 2: Kill the Leaker
Modify `leak_stopper.py` to:
1.  Check if memory usage > 50 MB.
2.  If Yes -> Kill the process (`proc.kill()`).
3.  Log "Killed process {pid} consuming {mem} MB".

## 🛠️ Task 3: The Watchdog
Wrap your logic in a `while True` loop that runs every 5 seconds.
Now run `leak_simulator.py` in one terminal, and `leak_stopper.py` in another.
Watch your script detect and kill the leaker automatically!

## 📝 Deliverable
A Python script `leak_stopper.py` that successfully terminates the simulator when it crosses the threshold.
