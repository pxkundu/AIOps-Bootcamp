# Solution for Exercise 01: The Manual Autoscaler
# Week 5 Day 4

import random
import time

def manual_control():
    print("Welcome to the Manual Autoscaler!")
    print("Controls: 'u'=Scale Up, 'd'=Scale Down, Enter=Hold")
    print("Goal: Keep Queue < 10, Servers Low.")
    print("-" * 30)
    
    servers = 1
    queue = 0
    total_score = 0
    
    for t in range(1, 21):
        # 1. Traffic Arrives
        arrival = random.randint(0, 10)
        
        # 2. Serve Requests
        capacity = servers * 5
        served = min(queue + arrival, capacity)
        new_queue = max(0, queue + arrival - served)
        
        # 3. Calculate Score (Before Action)
        cost = servers * 1
        penalty = queue * 2 # Waiting hurts
        revenue = served * 1
        step_score = revenue - cost - penalty
        total_score += step_score
        
        # Display State
        print(f"\nStep {t}/20 | Score: {total_score}")
        print(f"Queue: {queue} (+{arrival} -{served}) | Servers: {servers}")
        
        # 4. User Action
        action = input("Action? > ").strip().lower()
        if action == 'u':
            servers = min(10, servers + 1)
            print("  -> Scaling UP (+1 Server)")
        elif action == 'd':
            servers = max(1, servers - 1)
            print("  -> Scaling DOWN (-1 Server)")
        else:
            print("  -> Holding Capacity")
            
        queue = new_queue
        
    print("\nGame Over!")
    print(f"Final Score: {total_score}")

if __name__ == "__main__":
    manual_control()
