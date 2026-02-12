import sys
import os

# Add src and data to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))
sys.path.append(os.path.join(PROJECT_ROOT, 'data'))

# Import system
from panopticon import Panopticon
from generator import MetricGenerator

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
    for i, event in enumerate(gen.stream_live(n_events=100)):
        
        # Ground Truth
        is_attack = event['label'] != 'normal'
        if is_attack:
            attacks_launched += 1
            print(f"\n[ATTACK LAUNCHED] Type: {event['label']} | CPU: {event['cpu']:.1f}")
        
        # Detector
        detection = system.detect(event)
        
        # Scoring
        if is_attack and detection:
            print(f"  ✅ BLOCKED! System detected: {detection}")
            score += 1
        elif is_attack and not detection:
            print(f"  ❌ MISSED! Attack slipped through.")
        elif not is_attack and detection:
            print(f"  ⚠️ FALSE POSITIVE! Normal marked as: {detection}")
            score -= 0.5 
            
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
