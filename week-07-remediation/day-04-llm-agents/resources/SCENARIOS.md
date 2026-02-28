# Workshop Scenario Cards: The Agent Challenge

Use these cards during the Day 4 Workshop to test your agent's reasoning.

---

## 🏗️ Card 1: The "Silent Killer" (Ghost Latency)
**Alert:** `api-gateway` latency is > 2s, but error rate is 0%.
**System State:** 
- Database CPU is 5%.
- External payment provider is healthy.
- A new feature flag was enabled 10 minutes ago.
**Challenge:** Can your agent find the feature flag change after seeing no infrastructure issues?

---

## 🏗️ Card 2: The "Heisenbug" (OOM Killer)
**Alert:** `worker-node-04` has been restarted 5 times in 1 hour.
**System State:**
- Memory usage is flat at 40%.
- No error logs in the application.
- Kernel logs show `Out of memory: Kill process 12345 (python)`.
**Challenge:** Can your agent decide to call `check_kernel_logs` when application logs are clean?

---

## 🏗️ Card 3: The "Domino Effect" (DNS Failure)
**Alert:** 50 services reporting "Connection Refused".
**System State:**
- Network is up.
- CoreDNS pods are in `CrashLoopBackOff`.
**Challenge:** Will your agent identify the single point of failure (DNS) or get stuck trying to fix 50 individual services?

---

## 🛠️ Discussion Questions
1. How does the agent prioritize which service to investigate first?
2. What is the "Stop Condition" if the agent can't find the root cause?
3. How do we ensure the agent doesn't leak customer data found in the logs during the "Action" phase?
