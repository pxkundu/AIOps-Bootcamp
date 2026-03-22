# Solution for Project Handlers: The Reactor Logic
# Week 5 Day 3

import time

def restart_server(server_id):
    """
    Simulates AWS RebootInstance API call.
    """
    print(f"[ACTION] Rebooting server instance {server_id}...")
    # Simulate API Latency (fast)
    time.sleep(0.02) 
    return True

def block_ip(ip_address):
    """
    Simulates WAF Rule Update.
    """
    print(f"[ACTION] Adding firewall rule: BLOCK {ip_address}")
    time.sleep(0.01)
    return True

def scale_deployment(deployment):
    """
    Simulates Kubernetes Scale Out.
    """
    print(f"[ACTION] Scaling deployment {deployment} from 2 -> 4 replicas.")
    return True

def log_audit(event_type, source):
    """
    Logs unknown events for future analysis.
    """
    print(f"[AUDIT] Unhandled event: {event_type} from {source}")
    return True
