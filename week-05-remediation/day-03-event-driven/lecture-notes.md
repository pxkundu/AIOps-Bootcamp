# Week 5 Day 3: Event-Driven Automation

> **Duration:** 8 hours | **Difficulty:** Intermediate  
> **Focus:** Webhooks, FaaS (Function-as-a-Service), and Real-Time Reactions.

---

## ⚡ Part 1: Polling is (Often) Bad

All week we wrote scripts like:
```python
while True:
    if check_error():
        fix_it()
    time.sleep(60)
```

**The Cost of Polling:**
1.  **Latency:** If an error happens at `t=1s`, we wait 59s to notice.
2.  **Resources:** 99% of checks return "No Error". Wasted CPU.
3.  **Scalability:** If you monitor 10,000 servers, your loop is too slow.

---

## 🎣 Part 2: The Webhook Revolution

Instead of asking "Are you okay?", tell the server:
**"Call me when you break."**

A **Webhook** is just an HTTP POST request sent to a URL you define.
- **Source (GitHub/Prometheus):** "Commit Pushed" or "Alert Firing".
- **Destination (Your Script):** `http://my-server.com/hooks/restart-db`
- **Payload:** JSON data about the event.

---

## ☁️ Part 3: Serverless Functions (FaaS)

In the cloud (AWS/GCP), you don't even need a server listening.
You create a **Latent Function** (Lambda).
- Ideally: It costs $0/month.
- Event Happens: The Cloud provider spins up a container, runs your function, and destroys it.
- You pay for 100ms of compute.

**The "Glue" of AIOps:**
- Database Alarm -> EventBridge -> Lambda (Resize DB).
- GitHub Push -> Webhook -> Lambda (Deploy).

---

## 🚌 Part 4: The Event Bus Pattern

Don't hardcode `Alert -> Restart`.
Use a Bus (Router): `Alert -> Bus`.
The Bus decides who cares.
- `Severity: Critical` -> PagerDuty.
- `Type: DB_OOM` -> Remediation Script.
- `Type: Login_Success` -> Analytics DB.

**CloudEvents Standard:**
Standard JSON structure:
```json
{
  "specversion": "1.0",
  "type": "com.github.pull_request.opened",
  "source": "https://github.com/my-repo",
  "id": "A234-1234-1234",
  "time": "2023-01-01T12:00:00Z",
  "data": { ... }
}
```

---

<p align="center">
  <a href="../day-02-context/lecture-notes.md">⬅️ Back: Day 2</a> | <strong>Day 3: Event-Driven Workflows</strong> | <a href="../day-04-rl-control/lecture-notes.md">Next: Day 4 ➡️</a>
</p>
