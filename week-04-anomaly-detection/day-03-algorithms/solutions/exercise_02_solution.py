# Solution for Exercise 02: Contextual Trap
# Week 4 Day 3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ---------------------------------------------------------
# 1. GENERATE CONTEXTUAL DATA
# ---------------------------------------------------------
print("Generating 7 days of CPU metrics...")
hours = np.tile(np.arange(24), 7)
day_mask = (hours >= 9) & (hours <= 17)

# Normal Traffic
# Day: Mean 80% (High Load)
# Night: Mean 10% (Low Load)
cpu = np.where(day_mask, 
               np.random.normal(80, 5, len(hours)), 
               np.random.normal(10, 5, len(hours)))

# Inject Attack (The Sleeper)
# At index 3 (3 AM), inject 85% CPU.
# Normally 3 AM should be ~10%. So 85% is HUGE.
# But 85% is "Normal" for Daytime.
ATTACK_INDEX = 3
cpu[ATTACK_INDEX] = 85 

df = pd.DataFrame({'hour': hours, 'cpu': cpu})

# ---------------------------------------------------------
# 2. FAIL ATTEMPT: RAW FEATURES
# ---------------------------------------------------------
print("\n--- Attempt 1: Raw CPU Only ---")
# Only looking at CPU values, ignoring time.
# The model sees 85 and thinks "This is just like the 80s I see all day long".
clf_raw = IsolationForest(contamination=0.01, random_state=42)
df['pred_raw'] = clf_raw.fit_predict(df[['cpu']])

caught_raw = df.loc[ATTACK_INDEX, 'pred_raw'] == -1
print(f"Did Raw model catch the attack? {'YES' if caught_raw else 'NO'}")

# ---------------------------------------------------------
# 3. SUCCESS ATTEMPT: CONTEXTUAL FEATURES
# ---------------------------------------------------------
print("\n--- Attempt 2: CPU + Hour ---")
# The model sees [CPU=85, Hour=3]. It knows [CPU=80, Hour=12] is common.
# It knows [CPU=10, Hour=3] is common.
# It rarely sees [CPU=85, Hour=3], so it flags it.
clf_context = IsolationForest(contamination=0.01, random_state=42)
df['pred_context'] = clf_context.fit_predict(df[['cpu', 'hour']])

caught_context = df.loc[ATTACK_INDEX, 'pred_context'] == -1
print(f"Did Contextual model catch the attack? {'YES' if caught_context else 'NO'}")

# ---------------------------------------------------------
# 4. VISUALIZATION
# ---------------------------------------------------------
plt.figure(figsize=(12, 6))
plt.plot(df['cpu'], label='CPU Usage', color='gray', alpha=0.5)

# Highlight Attack
plt.scatter(ATTACK_INDEX, df.loc[ATTACK_INDEX, 'cpu'], c='red', s=200, label='Actual Attack', marker='x')

# Highlight Detections (Raw)
raw_anoms = df[df['pred_raw'] == -1]
plt.scatter(raw_anoms.index, raw_anoms['cpu'], c='blue', s=50, label='Raw Detection', marker='o', alpha=0.5)

# Highlight Detections (Context)
ctx_anoms = df[df['pred_context'] == -1]
plt.scatter(ctx_anoms.index, ctx_anoms['cpu'], c='green', s=100, label='Context Detection', marker='*', alpha=0.7)

plt.title("Contextual Detection: 3 AM Spike")
plt.xlabel("Hour Index")
plt.ylabel("CPU %")
plt.legend()
plt.show()

# Insight Check
# Usually raw detects excessive spikes (>100%), but misses context (85% at night).
# Context model should catch the 85% at night.
