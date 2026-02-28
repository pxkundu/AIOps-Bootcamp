import json

# --- 🛠️ Simulation Tools ---

def get_server_metrics(host):
    print(f"  [Tool] Fetching metrics for {host}...")
    # Simulated metrics
    return {"cpu": "95%", "mem": "40%", "status": "overloaded"}

def get_deployment_history(service):
    print(f"  [Tool] Fetching deployment history for {service}...")
    return [
        {"version": "v1.2.0", "time": "2 hours ago", "status": "success"},
        {"version": "v1.1.9", "time": "2 days ago", "status": "success"}
    ]

def check_error_logs(service):
    print(f"  [Tool] Scanning logs for {service}...")
    return "ERROR: NullPointerException in PaymentService.java:45"

# --- 🧠 The ReAct Engine (Simplified) ---

class AgentSentinel:
    def __init__(self, goal):
        self.goal = goal
        self.memory = []
        
    def reason(self, step):
        # In a real agent, this would be an LLM call.
        # Here we simulate the LLM's logic based on the step.
        if step == 0:
            return "THOUGHT: I see the goal is to investigate the CPU spike. I should check host metrics first.", "action:get_server_metrics"
        elif step == 1:
            return "THOUGHT: The CPU is indeed at 95%. This matches the alert. I need to see if a recent deployment caused this.", "action:get_deployment_history"
        elif step == 2:
            return "THOUGHT: A new version v1.2.0 was deployed 2 hours ago. Let me check the logs for that service to see if it's throwing errors.", "action:check_error_logs"
        else:
            return "THOUGHT: I have enough evidence. The incident was caused by a NullPointerException introduced in the v1.2.0 deployment.", "final_answer"

    def execute(self):
        print(f"🚀 Mission: {self.goal}\n")
        
        for i in range(5): # Limit to 5 reasoning loops
            thought, decision = self.reason(i)
            print(f"Step {i+1}:")
            print(f"  {thought}")
            
            if decision == "final_answer":
                print(f"\n✅ FINAL DIAGNOSIS: {thought.replace('THOUGHT: ', '')}")
                break
            
            # Simulated Tool Dispatcher
            if "get_server_metrics" in decision:
                obs = get_server_metrics("api-prod-01")
            elif "get_deployment_history" in decision:
                obs = get_deployment_history("payment-service")
            elif "check_error_logs" in decision:
                obs = check_error_logs("payment-service")
                
            print(f"  OBSERVATION: {obs}\n")
            self.memory.append({"thought": thought, "observation": obs})

if __name__ == "__main__":
    agent = AgentSentinel("Investigate the high CPU alert on api-prod-01")
    agent.execute()
