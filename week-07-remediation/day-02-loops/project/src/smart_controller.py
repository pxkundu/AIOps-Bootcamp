import json
import time
import os

class SmartRemediator:
    def __init__(self, simulator_path):
        self.simulator_path = simulator_path
        self.state = {} # {service_name: attempt_count}
        self.MAX_ATTEMPTS = 3
        
    def load_world(self):
        with open(self.simulator_path, 'r') as f:
            return json.load(f)

    def run_fix(self, service_name):
        print(f"🔧 Attempting fix for {service_name} (Attempt {self.state.get(service_name, 0) + 1}/{self.MAX_ATTEMPTS})...")
        # In a real system, this would call Ansible or a shell command.
        # Here we just log the action.
        time.sleep(1)
        
        # Increment attempt count
        self.state[service_name] = self.state.get(service_name, 0) + 1

    def verify(self, service_name, world_data):
        # In this simulation, auth-api is 'stubborn' and can_be_fixed is False
        service = world_data['services'].get(service_name)
        if service and service['status'] == "UP":
            return True
        return False

    def monitor_and_heal(self):
        print("🕵️ Smart Remediator active. Monitoring services...\n")
        
        while True:
            world = self.load_world()
            all_healthy = True
            
            for name, details in world['services'].items():
                if details['status'] == "DOWN":
                    all_healthy = False
                    
                    # 1. Check Circuit Breaker
                    if self.state.get(name, 0) >= self.MAX_ATTEMPTS:
                        print(f"🛑 [CIRCUIT BREAKER OPEN] for {name}. Manual intervention required!")
                        continue
                    
                    # 2. Act
                    self.run_fix(name)
                    
                    # 3. Verify
                    if self.verify(name, world):
                        print(f"✅ {name} successfully healed!")
                        self.state[name] = 0 # Reset state on success
                    else:
                        print(f"❌ {name} is still DOWN after fix.")
            
            if all_healthy:
                print("🟢 All systems nominal.")
                break # Exit loop for this demo once healthy or all breakers open
            
            # Check if all service breakers are open to prevent infinite loop in this demo
            breakers_open = all(self.state.get(n, 0) >= self.MAX_ATTEMPTS for n, d in world['services'].items() if d['status'] == "DOWN")
            if breakers_open:
                print("\n⚠️ No further automation possible. All circuit breakers are OPEN.")
                break
                
            time.sleep(2)

if __name__ == "__main__":
    remediator = SmartRemediator("service_simulator.json")
    remediator.monitor_and_heal()
