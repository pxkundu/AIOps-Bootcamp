import time
import random
import sys

class AIOpsGame:
    def __init__(self):
        self.trust = 100
        self.budget = 5000
        self.time_left = 8 # 8 hour shift
        self.active_incident = False
        
    def print_status(self):
        print(f"\n--- 🕒 Hour {9 - self.time_left}:00 | Trust: {self.trust}% | Budget: ${self.budget} ---")

    def log_storm_event(self):
        print("\n🚨 EVENT: LOG STORM! A latency spike has triggered 10,000 logs/second.")
        print("1. [AI] Run LLM RCA Aggregator (-$200, +Accuracy)")
        print("2. [Ansible] Run Blind Disk Cleanup (Free, 20% risk of crashing DB)")
        print("3. [SRE] Manual Log Grep (-10% Trust due to slowness)")
        
        choice = input("Your choice (1/2/3): ")
        if choice == '1':
            self.budget -= 200
            print("🧠 AI suggests: Root cause is a rogue crawler from IP 192.x.x.x. Blocks IP.")
            self.trust += 5
        elif choice == '2':
            if random.random() < 0.2:
                print("💥 DISASTER! Ansible deleted the active DB lock file. System CRASHED.")
                self.trust -= 40
            else:
                print("🧹 Cleanup successful. Disk pressure released.")
        else:
            self.trust -= 10
            print("🐢 Manual grep took too long. Customers are complaining about slowness.")

    def heisenbug_event(self):
        print("\n🚨 EVENT: THE HEISENBUG! Payment-API is oscillating (Up/Down).")
        print("Current Remediation Mode: AUTO-RESTART")
        time.sleep(1)
        print("...Restarting...")
        time.sleep(1)
        print("...Restarting...")
        
        print("\nLoop detected! Do you engage the CIRCUIT BREAKER?")
        print("1. [YES] Trip the breaker and escalate to human.")
        print("2. [NO] Let it keep trying. It might fix itself.")
        
        choice = input("Your choice (1/2): ")
        if choice == '1':
            print("🛡️ Circuit Breaker TRIPPED. System isolated. Trust -5%, but Budget saved.")
            self.trust -= 5
        else:
            print("💸 Infinite loop engaged. Your AWS Bill is skyrocketing!")
            self.budget -= 1000
            self.trust -= 20

    def run(self):
        print("🎮 WELCOME TO THE AIOPS SURVIVAL GAME: CYBER MONDAY EDITION")
        print("----------------------------------------------------------")
        
        while self.time_left > 0 and self.trust > 0 and self.budget > 0:
            self.print_status()
            
            # Random event selector
            event = random.choice(['logs', 'bug', 'quiet'])
            
            if event == 'logs':
                self.log_storm_event()
            elif event == 'bug':
                self.heisenbug_event()
            else:
                print("\n🟢 Monitoring... All systems quiet for now.")
                time.sleep(1)
            
            self.time_left -= 1
            if self.trust <= 0:
                print("\n💀 GAME OVER: You lost the trust of your users. You are FIRED.")
                return
            if self.budget <= 0:
                print("\n💸 GAME OVER: You went bankrupt paying for AI tokens and AWS bills.")
                return

        print(f"\n🏆 VICTORY! You survived the shift. Final Trust: {self.trust}%")

if __name__ == "__main__":
    game = AIOpsGame()
    game.run()
