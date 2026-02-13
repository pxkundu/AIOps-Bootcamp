# Week 5 Day 1: Trauma Simulator (Problem Generator)
# Run this to break your system (safely).

import subprocess
import time
import os
import sys

def create_broken_scripts():
    # 1. Zombie (Hangs)
    with open("zombie.py", "w") as f:
        f.write("import time; time.sleep(1000)")
        
    # 2. Leaker (Eats RAM)
    with open("leaker.py", "w") as f:
        f.write("import time; x=[]; \nwhile True: x.append(' '*1024*1024); time.sleep(0.1)")
        
    # 3. Flapper (Crashes instantly)
    with open("flapper.py", "w") as f:
        f.write("import sys; sys.exit(1)")

def launch_problems():
    print("[SIMULATOR] Launching broken services...")
    
    # Launch Zombie
    p1 = subprocess.Popen(["python", "zombie.py"])
    print(f"[SIMULATOR] Zombie PID: {p1.pid}")
    
    # Launch Leaker
    p2 = subprocess.Popen(["python", "leaker.py"])
    print(f"[SIMULATOR] Leaker PID: {p2.pid}")
    
    # Launch Flapper (It will die immediately, simulating a dead service)
    # We don't keep track because it's already dead. The healer needs to START it.
    print("[SIMULATOR] Flapper launched (and died). Expecting restart.")
    
    return [p1, p2]

if __name__ == "__main__":
    create_broken_scripts()
    procs = launch_problems()
    try:
        print("[SIMULATOR] Problems active. Run healer.py now!")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Simulator...")
        for p in procs:
            p.terminate()
