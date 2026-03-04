import os
import subprocess
import json
import re

# --- 🚀 UC-3: System Health Tool (Ops Commander) ---
def check_system_vitals():
    """
    Returns the top 5 memory hogs and disk usage for the Lightsail instance.
    For use in ChatOps (WhatsApp/Telegram).
    """
    try:
        # Get memory-intensive processes
        mem_output = subprocess.check_output("ps -eo pmem,pcpu,comm --sort=-pmem | head -n 6", shell=True).decode()
        
        # Get disk usage
        disk_output = subprocess.check_output("df -h / | tail -n 1", shell=True).decode()
        
        return {
            "memory_hogs": mem_output,
            "root_disk_usage": disk_output.strip(),
            "status": "HEALTHY"
        }
    except Exception as e:
        return {"error": str(e), "status": "DEGRADED"}

# --- 🛰️ UC-2: Shadow IT & Secret Sentry ---
def scan_for_secrets(directory="/var/www/html"):
    """
    Scans the provided directory for high-entropy strings (leaked API keys).
    """
    # Simple regex for generic tokens: 32+ char hex or alphanumeric
    secret_pattern = re.compile(r"(['\"])([A-Za-z0-9_-]{32,64})\1")
    leaks = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".env", ".py", ".js", ".json", ".yaml")):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                        matches = secret_pattern.findall(content)
                        if matches:
                            leaks.append({
                                "file": path,
                                "count": len(matches),
                                "risk": "CRITICAL"
                            })
                except:
                    continue
    return leaks if leaks else "✅ No leaks found."

# --- 🌪️ UC-1: Incident Summarizer (RCA) ---
def summarize_incident_logs(log_file="/var/log/syslog", lines=50):
    """
    Parses the tail of a log file and extracts 5xx or Error patterns for Bedrock analysis.
    """
    try:
        # Fetch the tail of the log
        log_snippet = subprocess.check_output(f"tail -n {lines} {log_file}", shell=True).decode()
        
        # Look for the word "error", "fail", or "500"
        alerts = re.findall(r"(?i)(error|failed|exception|5[0-9]{2})", log_snippet)
        
        return {
            "snippet": log_snippet,
            "alert_keywords_found": list(set(alerts)),
            "log_source": log_file
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test Simulation
    print("--- System Vitals ---")
    print(check_system_vitals())
    
    print("\n--- Secret Sentry Scan ---")
    print(scan_for_secrets(os.path.dirname(__file__)))
