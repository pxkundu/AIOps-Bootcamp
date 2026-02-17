# Exercise 01: The Manual Autoscaler (You vs Traffic)

## 🎯 Objective
Understand the delicate balance of **Over-provisioning** (burning money) vs **Under-provisioning** (losing customers).

---

## 🚦 The Rules

You are the Kubernetes Controller.
- **Traffic Pattern:** Waves of requests arrive randomly (Poisson distribution).
- **Your Capacity:** 1 Server = 5 Requests/Sec.
- **Your Cost:** $1 per active server per tick.
- **Your Penalty:** $2 per request waiting in queue.

**Goal:** Maximize Score (Revenue - Cost).
- If Queue > 0: You lose points rapidly.
- If Server Unused: You lose points slowly.

## 🛠️ Task 1: Play the Game

Run the provided script `manual_scaler.py`.
- Step 1: Request arrives.
- Step 2: You choose Action (`u`=Up, `d`=Down, `Enter`=Hold).
- Step 3: Simulation advances. Score updates.

Try to keep the **Queue** near 0, while keeping **Servers** low.

## 📝 Deliverable
Run for 20 steps. Note your High Score.
Can you beat a simple rule like "If Queue > 5, Scale Up"?
