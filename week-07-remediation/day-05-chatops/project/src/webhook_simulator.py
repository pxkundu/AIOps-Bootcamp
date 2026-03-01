import time

# Simulation helper for project demo
import slack_bot_sim

if __name__ == "__main__":
    slack_bot_sim.send_simulated_alert("order-service", "Latency Spike ( > 2000ms)")
    print("Simulated webhook received at /api/v1/alerts")
