#!/usr/bin/env python3
"""
Simple log generator to produce sample application logs for analysis.
"""

import json
import random
import time
from datetime import datetime

LOG_LEVELS = ["INFO", "INFO", "INFO", "WARN", "ERROR", "DEBUG"]
ENDPOINTS = ["/login", "/api/v1/orders", "/api/v1/products", "/health", "/api/v1/payment"]
SERVICES = ["auth-service", "order-manager", "payment-gateway", "frontend-api"]

def generate_log():
    level = random.choice(LOG_LEVELS)
    service = random.choice(SERVICES)
    endpoint = random.choice(ENDPOINTS)
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "service": service,
        "request_id": f"req-{random.getrandbits(32)}",
        "message": f"Handled request to {endpoint}",
        "metadata": {
            "duration_ms": random.randint(10, 500) if level != "ERROR" else random.randint(500, 5000),
            "status_code": 200 if level != "ERROR" else random.choice([400, 401, 500, 503])
        }
    }
    
    if level == "ERROR":
        log_entry["message"] = f"Failed to process request to {endpoint}"
        log_entry["exception"] = "ServiceTimeoutException" if log_entry["metadata"]["status_code"] == 503 else "ValidationFailed"
        
    return log_entry

def main(count=10):
    print(f"--- Generating {count} Sample Logs ---\n")
    for _ in range(count):
        print(json.dumps(generate_log()))
        time.sleep(0.1)

if __name__ == "__main__":
    main()
