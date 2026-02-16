# Exercise 01: Polling vs Webhook (The Speed Test)

## 🎯 Objective
Understand the latency difference between **Checking State** (Polling) and **Reacting to Events** (Webhooks).

---

## 🛠️ Task 1: The Slow Way (Polling)

1.  Create `trigger_file.py`:
    - Writes current timestamp to `alert.txt`.
    - Sleeps random amount (0.1 - 2s) before writing.
2.  Create `poller.py`:
    - `while True:` loop.
    - Check if `alert.txt` exists.
    - If yes: Read timestamp. Calculate `delay = now - written_time`. Print delay. Delete file.
    - Sleep 1s.

**Run Both:** See delays up to 1000ms.

## 🛠️ Task 2: The Fast Way (Webhook)

1.  Create `receiver.py` (Flask):
    - Listen on `/alert`.
    - On POST: Read `json['timestamp']`. Calculate `delay = now - sent_time`. Print.
2.  Create `trigger_hook.py`:
    - Sends POST to `http://localhost:5000/alert` with `{'timestamp': time.time()}`.

**Run Both:** See delays ~5-10ms.

## 📝 Deliverable
Capture the output showing the massive speed difference (100x faster).
