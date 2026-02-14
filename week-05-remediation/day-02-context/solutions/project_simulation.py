# Solution for Capstone Project Simulation: The Smart Doctor
# Week 5 Day 2

import joblib
import pandas as pd
import numpy as np

# Load Model (Ensure you ran exercise_02_trainer.py first!)
try:
    clf = joblib.load('doctor_model.pkl')
    print("[INFO] Model loaded successfully.")
except:
    print("[ERROR] Model not found. Please run exercise_02_trainer.py first.")
    exit(1)

# Action Map
ACTION_MAP = {
    0: "IGNORE (Backup)",
    1: "SCALE_UP (High CPU)",
    2: "ROLLBACK (Deploy Fail)",
    3: "RESTART (Mem Leak)",
    4: "ESCALATE"
}

def simulate_incidents():
    print("\n--- Starting Live Simulation ---\n")
    
    # Test Cases (Context, Symptom -> Expected Action)
    test_cases = [
        # 1. The Backup Incident
        {'cpu': 95, 'mem': 20, 'is_backup': 1, 'is_deploy': 0, 'desc': "Backup Window (High CPU)"},
        
        # 2. The Deployment Failure
        {'cpu': 20, 'mem': 95, 'is_backup': 0, 'is_deploy': 1, 'desc': "Deploy Window (High Mem)"},
        
        # 3. The Runaway Process
        {'cpu': 95, 'mem': 20, 'is_backup': 0, 'is_deploy': 0, 'desc': "Normal Time (High CPU)"},
        
        # 4. The Memory Leak
        {'cpu': 20, 'mem': 95, 'is_backup': 0, 'is_deploy': 0, 'desc': "Normal Time (High Mem)"},
    ]

    score = 0
    
    for case in test_cases:
        # Prepare Features (Matches Training Columns: cpu, mem, is_backup, is_deploy)
        features = [[case['cpu'], case['mem'], case['is_backup'], case['is_deploy']]]
        
        # Predict
        action_code = clf.predict(features)[0]
        action_str = ACTION_MAP.get(action_code, "UNKNOWN")
        
        print(f"Incident: {case['desc']}")
        print(f"  Context: CPU={case['cpu']}%, Backup={case['is_backup']}")
        print(f"  Diagnosis: {action_str}")
        
        # Validation Logic (Simplified)
        if "Backup" in case['desc'] and action_code == 0:
            print("  ✅ CORRECT")
            score += 1
        elif "Deploy" in case['desc'] and action_code == 2:
            print("  ✅ CORRECT")
            score += 1
        elif "Normal Time (High CPU)" in case['desc'] and action_code == 1:
            print("  ✅ CORRECT")
            score += 1
        elif "Normal Time (High Mem)" in case['desc'] and action_code == 3:
            print("  ✅ CORRECT")
            score += 1
        else:
            print("  ❌ WRONG DIAGNOSIS")
            
        print("-" * 30)

    print(f"Final Score: {score}/{len(test_cases)}")
    if score == len(test_cases):
        print("🏆 The Doctor is In. System Certified Safe.")
    else:
        print("💀 Malpractice Suit Incoming. Retrain Model.")

if __name__ == "__main__":
    simulate_incidents()
