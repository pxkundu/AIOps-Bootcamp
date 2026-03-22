# Solution for Exercise 01: The Manual Triage
# Week 5 Day 2

def diagnose(incident):
    """
    Manually checks incident context.
    Input: dict
    Output: str (Action)
    """
    cpu = incident.get('cpu_usage', 0)
    mem = incident.get('memory_usage', 0)
    hour = incident.get('hour', 0)
    backup = incident.get('backup_running', False)
    deploy = incident.get('deploy_running', False)
    
    # 1. Backup Window Override
    if cpu > 90 and backup:
        return "IGNORE"
    
    # 2. Normal CPU Spike
    if cpu > 90 and not backup:
        return "SCALE_UP"
        
    # 3. Deploy Failure (Mem Leak)
    if mem > 90 and deploy:
        return "ROLLBACK"
        
    # 4. Normal Mem Leak
    if mem > 90 and not deploy:
        return "RESTART_SERVICE"
        
    return "ESCALATE"

# Test Cases
test_cases = [
    ({'cpu_usage': 95, 'hour': 3, 'backup_running': True}, "IGNORE"),
    ({'cpu_usage': 95, 'hour': 10, 'backup_running': False}, "SCALE_UP"),
    ({'memory_usage': 95, 'deploy_running': True}, "ROLLBACK"),
    ({'memory_usage': 95, 'deploy_running': False}, "RESTART_SERVICE"),
    ({'cpu_usage': 50, 'memory_usage': 50}, "ESCALATE")
]

print("Running Manual Triage Tests...")
for inc, expected in test_cases:
    result = diagnose(inc)
    status = "PASS" if result == expected else "FAIL"
    print(f"[{status}] Incident: {inc} -> {result} (Expected: {expected})")
