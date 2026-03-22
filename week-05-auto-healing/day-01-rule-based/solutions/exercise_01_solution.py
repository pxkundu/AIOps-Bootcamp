# Solution for Exercise 01: The Memory Leak (Python Remediation)
# Week 5 Day 1

import psutil
import time
import os

# ---------------------------------------------------------
# 1. LEAK STOPPER
# ---------------------------------------------------------
def kill_leaker(threshold_mb=50):
    """
    Finds and kills processes matching 'leaker_process' consuming excessive RAM.
    """
    leaker_found = False
    
    # Iterate all processes
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            # Get info safely (Process might terminate)
            info = proc.info
            name = info['name']
            pid = info['pid']
            rss = info['memory_info'].rss / (1024 * 1024) # MB
            
            # Identify target (modify name as needed)
            if 'leaker' in name.lower() or 'python' in name.lower():
                # Checking cmdline is safer for python scripts
                try:
                    cmdline = proc.cmdline()
                    if any('leak_simulator.py' in arg for arg in cmdline):
                        print(f"[FOUND] {name} ({pid}) using {rss:.1f} MB")
                        
                        if rss > threshold_mb:
                            print(f"[KILL] Terminating PID {pid} (Limit: {threshold_mb} MB)")
                            proc.kill()
                            leaker_found = True
                            return True # Killed one
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    pass
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    if not leaker_found:
        print("[INFO] No active leakers detected.")
    return False

# ---------------------------------------------------------
# 2. WATCHDOG LOOP
# ---------------------------------------------------------
if __name__ == "__main__":
    print("Starting Memory Leak Watchdog...")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            kill_leaker(threshold_mb=20) # Low threshold for demo
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping Watchdog.")
