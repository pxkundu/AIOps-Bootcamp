# Exercise 03: Log Rarity & Shannon Entropy

## 🎯 Objective
Apply Information Theory (Shannon Entropy) to a stream of logs to mathematically identify which messages are "surprising" (rare) and which are "monotonous" (common).

---

## 📋 The Dataset
Download or create a file `microservice_logs.txt` with the following distribution:
- 950 lines of `INFO: Heartbeat sent`
- 45 lines of `WARN: High disk usage`
- 5 lines of `CRITICAL: Segfault in module X`

---

## 🛠️ Step 1: Probability Mapping
1.  Count the frequency of each unique log message.
2.  Calculate the probability $P(x)$ for each message.

---

## 🧪 Step 2: Calculating Self-Information
The "Surprise" or "Information Content" of a message $x$ is:
$$I(x) = -\log_2(P(x))$$

### Task:
Calculate $I(x)$ for all three log types.
- Which one has the highest value?
- What is the unit of this value? (Hint: Bits)

---

## 📊 Step 3: Total System Entropy
Calculate the **Shannon Entropy** ($H$) of the entire log stream:
$$H = -\sum P(x) \log_2(P(x))$$

---

## ✅ Deliverable
A Python script that:
1.  Outputs the "Surprise Score" for each log level.
2.  Explains how a sudden increase in Total System Entropy ($H$) could indicate a "Log Storm" or an emerging incident.
