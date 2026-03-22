# Solution: Circuit Breaker Implementation
# Week 5 Day 5 Exercise 02

class CircuitBreakerEngine:
    def __init__(self, limit=3):
        self.remediation_counts = {}
        self.limit = limit
        self.last_action_time = {}

    def diagnose_and_heal(self, service, issue):
        # 1. Check Circuit Status
        current_count = self.remediation_counts.get(service, 0)
        
        if current_count >= self.limit:
            print(f"🛑 [CIRCUIT BREAKER] {service} tripped! Retry count: {current_count}. Stopping automation.")
            return "CIRCUIT_BROKEN_HUMAN_REQUIRED"
        
        # 2. Logic to choose healing action
        print(f"🔧 Attempting to fix {service} (Attempt {current_count + 1})")
        
        # Simulate healing execution...
        success = self._run_healer(service, issue)
        
        if success:
            # In a real environment, we might increment only on failure, 
            # or increment every time until we verify a sustained fix.
            self.remediation_counts[service] = current_count + 1
            return "HEALING_EXECUTED"
        
        return "HEALING_FAILED"

    def _run_healer(self, service, issue):
        # Mocking healer
        return True

    def reset_circuit(self, service):
        print(f"✅ Resetting circuit for {service}.")
        self.remediation_counts[service] = 0

# --- Test ---
engine = CircuitBreakerEngine(limit=3)

# Simulate 4 incidents in quick succession
for i in range(4):
    result = engine.diagnose_and_heal("webapp", "out_of_memory")
    print(f"Result: {result}")
