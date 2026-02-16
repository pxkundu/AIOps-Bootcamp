# Week 5 Day 3 Project: The Reactor (Event-Driven Remediation) ⚛️

> **Challenge:** You are building the central nervous system of your AIOps platform. Alerts come from everywhere (CloudWatch, Prometheus, GitHub). Your "Reactor" must catch them and fire the correct response instantly.

---

## 🎯 Objective
Build a Flask-based **Event Receiver** (`app.py`) that:
1.  **Ingests** JSON payloads in CloudEvents format.
2.  **Routes** based on `event_type` ("database.crash", "security.intrusion").
3.  **Executes** the correct remediation logic in `handlers.py`.
4.  **Responds** with HTTP 200 within 50ms.

---

## 📂 Project Structure

```
reactor/
├── src/
│   ├── app.py          # The Webhook Server (Router)
│   └── handlers.py     # The Business Logic (Fix DB, Block IP)
├── run_simulation.py   # The Fire Hose (Sends 10 events)
└── README.md
```

## 🛠️ Step 1: Define CloudEvents Schema

Your receiver must validate that every POST request has:
- `specversion`: "1.0"
- `type`: String (e.g., "server.down")
- `source`: String (e.g., "prometheus")
- `data`: Dict (The details)

If any field is missing, return HTTP 400 "Bad Request".

## 🛠️ Step 2: Implement Handlers (`src/handlers.py`)

Write functions for:
1.  `restart_vm(server_id)`: Prints "Rebooting server {id}..."
2.  `block_ip(ip_address)`: Prints "Blocking firewall rule for {ip}..."
3.  `scale_up(service)`: Prints "Adding 2 replicas to {service}..."

## 🛠️ Step 3: The Router (`src/app.py`)

- **POST /events**
- Parse JSON.
- If `type == "server.down"` -> `handlers.restart_vm(data['id'])`
- If `type == "security.bruteforce"` -> `handlers.block_ip(data['ip'])`
- Else -> Log "Unknown event type" and return 200 (Don't error out, just acknowledge).

## 🚀 Twist: HMAC Security
(Optional) Configure a SECRET_KEY = "my_secret".
simulation must send `X-Hub-Signature` header.
Receiver must verify the signature matches the payload.
If not, return 403 Forbidden.

## 📝 Deliverable
Run `python run_simulation.py` (provided solution).
It will fire 10 events.
Your server logs should show:
```text
[INFO] Received server.down for i-12345
[ACTION] Rebooting server i-12345...
[INFO] Received security.bruteforce for 192.168.1.50
[ACTION] Blocking firewall rule for 192.168.1.50...
```
