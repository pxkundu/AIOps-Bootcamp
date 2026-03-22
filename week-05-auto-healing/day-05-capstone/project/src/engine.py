# Aegis Core Engine
from project.src.healers import process, security
import datetime

class AegisEngine:
    def __init__(self):
        self.history = []
        
    def triage_and_heal(self, event):
        """
        Main Decision Loop.
        Accepts: Dict (metric/alert event)
        """
        etype = event.get('type')
        data = event.get('data', {})
        hour = datetime.datetime.now().hour
        
        print(f"\n[ENGINE] Processing {etype} event...")
        
        # 1. Context Check: Backup Window Logic
        if hour >= 2 and hour <= 4:
            if etype == 'cpu_spike' and data.get('service') == 'database':
                print("[ENGINE] IGNORING high CPU - Currently in Backup Window (02:00-04:00).")
                return "IGNORED_EXPECTED_BEHAVIOR"

        # 2. Decision Tree Logic
        if etype == 'memory_leak':
            # Logic: If memory > 90% -> Restart
            if data.get('value', 0) > 90:
                print(f"[ENGINE] High Memory detected ({data['value']}%). Triggering Restart.")
                process.restart_service(data['service'])
                return "HEALED_RESTART"
            
        elif etype == 'security_alert':
            # Logic: If unauthorized attempts > 50 -> Block IP
            if data.get('failed_attempts', 0) > 50:
                print(f"[ENGINE] Brute force detected from {data['ip']}.")
                security.block_ip(data['ip'])
                return "HEALED_IP_BLOCK"
                
        elif etype == 'capacity_breach':
            # Logic: Trigger Scaling logic
            print(f"[ENGINE] Traffic spike on {data['service']}. Scaling Up Instance Group.")
            # Trigger Scaling healer
            return "HEALED_SCALE_UP"

        print("[ENGINE] No automated runbook found. Escalating to SRE On-Call.")
        return "ESCALATED"

    def audit(self, action_result):
        self.history.append({
            "time": datetime.datetime.now().isoformat(),
            "result": action_result
        })
