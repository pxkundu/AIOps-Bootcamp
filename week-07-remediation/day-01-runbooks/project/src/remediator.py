import os
import json
import time

# Note: In a real scenario, we would use ansible_runner. 
# For this lab, we will use a direct subprocess call to make it easier to debug.
import subprocess

ALERTS_FILE = "alerts.json"

def check_for_alerts():
    if not os.path.exists(ALERTS_FILE):
        return None
    
    with open(ALERTS_FILE, "r") as f:
        try:
            alerts = json.load(f)
            return alerts
        except:
            return None

def trigger_remediation():
    print("🚀 Triggering Auto-Remediation: Running cleanup.yml...")
    try:
        # Run ansible-playbook locally
        result = subprocess.run(["ansible-playbook", "cleanup.yml"], capture_output=True, text=True)
        print(result.stdout)
        return True
    except Exception as e:
        print(f"❌ Remediation failed: {e}")
        return False

if __name__ == "__main__":
    print("🩺 Disk Doctor Controller starting...")
    
    # Simple loop simulation
    while True:
        alerts = check_for_alerts()
        
        if alerts and any(a.get("type") == "disk_full" for a in alerts):
            print("⚠️ DISK_FULL Alert detected!")
            success = trigger_remediation()
            
            if success:
                print("✅ System healed. Clearing alerts...")
                # Clear the alerts file after healing
                with open(ALERTS_FILE, "w") as f:
                    json.dump([], f)
            break
        else:
            print("🟢 System healthy (no active disk alerts)...")
        
        time.sleep(5)
