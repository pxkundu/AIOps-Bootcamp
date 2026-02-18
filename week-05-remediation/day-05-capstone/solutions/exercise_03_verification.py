# Solution: Post-Remediation Verification
# Week 5 Day 5 Exercise 03

import time
import random

def mock_remediation():
    print("  [HEALER] Restarting service...")
    return True

def verify_health():
    """
    Checks if the service is actually healthy.
    Simulates a 70% chance of a successful fix.
    """
    time.sleep(1) # Grace period
    is_up = random.random() > 0.3
    return is_up

def closed_loop_healing():
    print("Received Alert: Webapp is Down.")
    
    # Step 1: Execute Fix
    mock_remediation()
    
    # Step 2: Verify Fix
    print("  [VERIFY] Checking health after fix...")
    if verify_health():
        print("  ✅ [SUCCESS] Service is stable.")
        return "STABLE"
    else:
        print("  ❌ [FAILED] Service is still down after restart.")
        # Step 3: Secondary Remediation (e.g. Rollback)
        print("  [HEALER-2] Triggering Rollback as last resort...")
        time.sleep(1)
        return "ROLLED_BACK"

if __name__ == "__main__":
    for i in range(3):
        print(f"\n--- Simulation {i+1} ---")
        status = closed_loop_healing()
        print(f"Final Outcome: {status}")
