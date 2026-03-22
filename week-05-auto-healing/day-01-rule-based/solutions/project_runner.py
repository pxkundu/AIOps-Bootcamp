# Solution for Capstone Project Runner: The Auto-Restarter
# Week 5 Day 1

import subprocess
import time
import os
import signal
import sys

# ---------------------------------------------------------
# 1. GENERATE DUMMY SERVICES
# ---------------------------------------------------------
print("Creating dummy services...")

# Ensure 'services' dir exists
if not os.path.exists("services"):
    os.makedirs("services")

# Build 'api.py' (Crasher)
with open("services/api.py", "w") as f:
    f.write("""
import time
import random
import sys
import os

print(f"[API] Starting PID {os.getpid()}...")
time.sleep(random.randint(1, 3))

# Crash 50% of the time immediately
if random.random() < 0.5:
    print(f"[API] CRASH: Database Gone! (PID {os.getpid()})")
    sys.exit(1)

# Else run for 5 more seconds then exit normally
time.sleep(5)
print(f"[API] Service Shutdown Ordered (PID {os.getpid()})")
sys.exit(0)
""")

# Build 'worker.py' (Zombie / Slow Death)
with open("services/worker.py", "w") as f:
    f.write("""
import time
import os
import sys

print(f"[WORKER] Starting PID {os.getpid()}...")
# Run forever
try:
    while True:
        time.sleep(1)
except:
    sys.exit(0)
""")

# ---------------------------------------------------------
# 2. THE SUPERVISOR (Main Logic)
# ---------------------------------------------------------
print("Starting Supervisor...")

SERVICES = {
    "api": ["python", "services/api.py"],
    "worker": ["python", "services/worker.py"]
}

# State Tracking
processes = {} # name -> Popen object
restart_counts = {} # name -> int
last_restart_time = {} # name -> float

def start_service(name):
    print(f"[SUPERVISOR] Starting {name}...")
    proc = subprocess.Popen(SERVICES[name])
    processes[name] = proc
    return proc

def monitor_loop():
    try:
        # Initial Start
        for name in SERVICES:
            start_service(name)
            restart_counts[name] = 0
            last_restart_time[name] = time.time()
            
        while True:
            for name, proc in list(processes.items()):
                # Check status
                ret = proc.poll()
                
                if ret is not None:
                    # Process Dead
                    print(f"[SUPERVISOR] Alert: {name} died with code {ret}")
                    
                    # Backoff Logic
                    now = time.time()
                    if now - last_restart_time[name] < 10:
                        restart_counts[name] += 1
                        print(f"  -> Rapid failure count: {restart_counts[name]}")
                    else:
                        restart_counts[name] = 0 # Reset if stable for >10s
                        
                    last_restart_time[name] = now
                    
                    if restart_counts[name] > 3:
                        print(f"  -> Too many restarts. Cooling down for 5s...")
                        time.sleep(5)
                        restart_counts[name] = 0
                        
                    # Restart
                    print(f"  -> Restarting {name}...")
                    start_service(name)
                    
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping Supervisor...")
        for name, proc in processes.items():
            if proc.poll() is None:
                proc.terminate()

if __name__ == "__main__":
    monitor_loop()
