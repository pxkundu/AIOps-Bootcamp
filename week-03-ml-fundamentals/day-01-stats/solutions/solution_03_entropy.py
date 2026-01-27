import math
from collections import Counter

# Sample log data
logs = (
    ["INFO: Heartbeat sent"] * 950 + 
    ["WARN: High disk usage"] * 45 + 
    ["CRITICAL: Segfault in module X"] * 5
)

def calculate_stats(data):
    counts = Counter(data)
    total = len(data)
    
    print(f"{'Log Message':<30} | {'Probability':<12} | {'Surprise (Bits)':<15}")
    print("-" * 65)
    
    system_entropy = 0
    for message, count in counts.items():
        prob = count / total
        
        # 1. Self-Information (Individual surprise)
        surprise = -math.log2(prob)
        
        # 2. Add to Shannon Entropy
        system_entropy += prob * surprise
        
        print(f"{message:<30} | {prob:<12.4f} | {surprise:<15.4f}")
        
    return system_entropy

print("--- Log Rarity Analysis ---")
total_entropy = calculate_stats(logs)

print(f"\nTotal System Entropy (H): {total_entropy:.4f} bits")

print("\n--- AIOps Interpretation ---")
print("1. Which is most surprising? The CRITICAL log. It contains ~7.6 bits of 'new' info.")
print("2. Total Entropy indicates the 'Uncertainty' of the stream.")
print("   - If H increases: New types of errors are appearing. Signal of a 'Log Storm'.")
print("   - If H is near 0: Every log is the same. Monotonous system.")
print("3. Application: Use Entropy as a feature to trigger alerts on 'Novel' log messages.")
