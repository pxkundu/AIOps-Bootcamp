# Solution for Capstone: The War Room Simulation
# Week 4 Day 5

import pandas as pd
import numpy as np
import time
from generator import MetricGenerator # Assumes generator.py is in PYTHONPATH or same folder
from panopticon_solution import Panopticon

def run_simulation():
    print("Welcome to THE WAR ROOM.")
    print("-------------------------")
    
    # 1. SETUP
    gen = MetricGenerator()
    print("Generating training history (30 days)...")
    history_df = gen.generate_history()
    
    # 2. DEPLOY SYSTEM
    system = Panopticon()
    system.train(history_df)
    
    # 3. BATTLE
    print("\nINITIATING LIVE ATTACK STREAM...")
    score = 0
    attacks_launched = 0
    
    # Stream 100 events
    # We yield dicts: {'timestamp', 'cpu', 'fan_speed', 'label'}
    for i, event in enumerate(gen.stream_live(n_events=100)):
        
        # Ground Truth
        is_attack = event['label'] != 'normal'
        if is_attack:
            attacks_launched += 1
            print(f"\n[ATTACK LAUNCHED] Type: {event['label']} | CPU: {event['cpu']:.1f}")
        
        # Detector
        # In reality, this would be an API call
        # Here we just call the method
        detection = system.detect(event)
        
        # Scoring
        if is_attack and detection:
            print(f"  ✅ BLOCKED! System detected: {detection}")
            score += 1
        elif is_attack and not detection:
            print(f"  ❌ MISSED! Attack slipped through.")
        elif not is_attack and detection:
            print(f"  ⚠️ FALSE POSITIVE! Normal marked as: {detection}")
            score -= 0.5 # Penalty
            
    # 4. DEBRIEF
    print("\n-------------------------")
    print(f"FINAL SCORE: {score}/{attacks_launched}")
    
    if score >= 4:
        print("🏆 MISSION ACCOMPLISHED. SYSTEM SECURE.")
        print("You have mastered Anomaly Detection. Welcome to Week 5.")
    else:
        print("💀 SYSTEM COMPROMISED. RETRAIN AND TRY AGAIN.")

if __name__ == "__main__":
    run_simulation()
