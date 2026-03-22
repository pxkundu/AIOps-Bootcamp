# Solution: The Trauma Healer (Remediation Logic)
# Week 5 Day 1

import psutil
import subprocess
import time
import os

SERVICES = {
    'zombie.py': 'kill_relaunch', # If found (it hangs), kill and restart
    'leaker.py': 'kill_relaunch', # If uses > 50MB, kill and restart
    'flapper.py': 'ensure_running' # If not running, start it
}

def check_memory(pid, limit=10):
    try:
        proc = psutil.Process(pid)
        rss = proc.memory_info().rss / (1024 * 1024)
        return rss > limit
    except psutil.NoSuchProcess:
        return False

def heal():
    print("[HEALER] Starting rounds...")
    
    found_services = set()
    
    # 1. Scan active processes
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = proc.info['cmdline']
            if cmd and len(cmd) > 1 and 'python' in cmd[0]:
                script_name = os.path.basename(cmd[1]) # zombie.py
                
                if script_name in SERVICES:
                    found_services.add(script_name)
                    pid = proc.info['pid']
                    action = SERVICES[script_name]
                    
                    if script_name == 'leaker.py':
                        if check_memory(pid, limit=50):
                            print(f"[REMEDIATION] Leaker detected (PID {pid}). Killing...")
                            proc.kill()
                            # Restart
                            print(f"[REMEDIATION] Restarting leaker.py...")
                            subprocess.Popen(["python", "leaker.py"])
                            
                    elif script_name == 'zombie.py':
                        # Simplification: Assume all zombies must die
                        # In reality, check if unresponsive via HTTP/socket
                        print(f"[REMEDIATION] Zombie detected (PID {pid}). Killing...")
                        proc.kill()
                        print(f"[REMEDIATION] Restarting zombie.py...")
                        subprocess.Popen(["python", "zombie.py"])
                        
        except (psutil.NoSuchProcess, IndexError):
            pass
            
    # 2. Check for missing services (Flapper)
    for svc in SERVICES:
        if svc not in found_services:
            print(f"[REMEDIATION] Service {svc} is MISSING! Starting...")
            try:
                subprocess.Popen(["python", svc])
            except FileNotFoundError:
                print(f"[ERROR] Script {svc} not found. Did you run simulator?")

if __name__ == "__main__":
    while True:
        heal()
        time.sleep(5)
