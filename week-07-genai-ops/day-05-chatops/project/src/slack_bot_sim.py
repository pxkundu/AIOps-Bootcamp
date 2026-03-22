import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# --- 🚀 SIMULATION MODE ---
# Set these in your env if you have a real Slack App
# SLACK_BOT_TOKEN = "xoxb-..."
# SLACK_APP_TOKEN = "xapp-..."

def send_simulated_alert(service, reason):
    """
    Simulates sending an interactive card to a Slack channel.
    In a real app, you would use app.client.chat_postMessage(...)
    """
    print("\n--- 📟 INTERACTIVE SLACK NOTIFICATION ---")
    print(f"*Service:* {service}")
    print(f"*Alert:* {reason}")
    print("*AIOps Suggestion:* Detected memory leak. Recommend service restart.")
    print("---------------------------------------")
    print("[ Button: ACKNOWLEDGE ]  [ Button: RESTART SERVICE ]")
    print("---------------------------------------\n")

def handle_remediate_click(service):
    print(f"🛠️  BOT ACTION: Executing remediation for {service}...")
    print("📋 [LOG] Calling Ansible Playbook: restart_service.yml")
    print("✅ [SUCCESS] Service restarted and verified.")

if __name__ == "__main__":
    print("🤖 ChatOps Sentry Starting (Simulation Mode)...")
    
    # 🚨 Simulator sequence
    time_delay = 2
    
    print(f"Waiting for alerts...")
    time.sleep(time_delay)
    
    send_simulated_alert("payment-api", "High Memory Usage (> 90%)")
    
    user_input = input("Click a button? (1: Acknowledge, 2: Restart Service, 3: Skip): ")
    
    if user_input == "2":
        handle_remediate_click("payment-api")
    elif user_input == "1":
        print("👤 USER ACTION: Incident Acknowledged. Bot will stand down.")
    else:
        print("⌛ No action taken. Alert will persist in dashboard.")
