# Day 1 Project: The Entropy Engine (Rare Event Detector)

> **Goal:** Build a Python tool that uses Information Theory (Entropy) to automatically find rare and potentially critical log messages in a sea of millions of normal logs.

---

## 🎯 Project Overview

Modern systems generate massive log volumes. Most logs are boring ("Heartbeat", "User login", "Cache hit"). Finding the one "Niche" log that indicates a rare race condition is like finding a needle in a haystack.

Conventional tools use "Grepping" for keywords. An AIOps approach uses **Statistical Rarity**.

## 🏗️ Requirements

### 1. Log Simulator (`log_emitter.py`)
Generate 100,000 logs.
- 99% should be common messages (e.g., `[INFO] Connection accepted`).
- 0.5% should be moderately rare (`[WARN] Retrying connection`).
- 0.1% should be "Incredible Surprises" (`[CRITICAL] Kernel Panic: Stack overflow at 0x4f`).

### 2. The Entropy Calculator (`engine.py`)
Your script must:
1.  Read the log file.
2.  Calculate the frequency of each unique log message template.
3.  Calculate the **Shannon Entropy** (Self-Information) for each message.
    *   Formula: `I(x) = -log2(P(x))` where `P(x)` is the probability of the message.
4.  Rank the logs from "Most Boring" to "Most Surprising".

---

## 🚀 Starter Code Snippet

```python
import math
from collections import Counter

logs = [
    "INFO: User login",
    "INFO: User login",
    "ERROR: DB connection failed",
    "INFO: User login"
]

def calculate_surprise(logs):
    counts = Counter(logs)
    total = len(logs)
    surprise_scores = {}
    
    for log, count in counts.items():
        prob = count / total
        # High probability = Low surprise
        # Low probability = High surprise
        surprise_scores[log] = -math.log2(prob)
        
    return surprise_scores

# TODO: Enhance this to ignore timestamps and dynamic IDs 
# (e.g., "User login [ID: 123]" should be treated as "User login")
```

---

## ✅ Evaluation Rubric

| Criteria | Points |
|----------|--------|
| **Functional:** Successfully identifies the "Kernel Panic" as the highest surprise. | 40 |
| **Technique:** Correct implementation of Shannon Entropy formula. | 30 |
| **Abstraction:** The engine can collapse variable IDs (e.g., `User 1` and `User 2` are the same template). | 20 |
| **Performance:** Script handles 100k logs in < 5 seconds. | 10 |

---

## 📤 Submission
Submit your `log_emitter.py` and `engine.py`. In your README, explain why a log message that appears only once in 1,000,000 logs has a higher entropy than one that appears every 10 seconds.
