# Exercise 03: The Filter & Mask Challenge

## 🎯 Objective
In AIOps, your pipeline must be "Intelligent". You don't want to store expensive logs you don't need, and you MUST protect user privacy. Today you will implement **Log Sampling** and **PII Masking**.

---

## 🛠️ Step 1: Scenario
You are processing logs from a financial app. The logs contain high volume of `DEBUG` info and sensitive `Account_Number` data.

**Sample Data (`finance.log`):**
```json
{"time": "2024-01-19T20:40:01Z", "level": "DEBUG", "msg": "Heartbeat pulse 1"}
{"time": "2024-01-19T20:40:02Z", "level": "INFO", "msg": "Transaction started", "acc": "DE1234567890"}
{"time": "2024-01-19T20:40:03Z", "level": "DEBUG", "msg": "Cache lookup miss"}
{"time": "2024-01-19T20:40:04Z", "level": "ERROR", "msg": "Insufficient funds", "acc": "US9988776655"}
```

---

## 🔒 Task 1: PII Masking (Privacy)
You must ensure no account numbers (`acc`) leave the edge in plaintext.

**Configuration:**
Use the `modify` filter to replace the `acc` field or use the `rewrite_tag` filter for more complex logic. 

**Draft this Filter in `fluent-bit.conf`:**
```ini
[FILTER]
    Name          modify
    Match         finance.*
    # Simple regex to mask everything except first 2 chars
    # Note: Fluent Bit 2.x supports lua for more complex masking
    Add           data_privacy_level high
```

---

## 📉 Task 2: Adaptive Sampling (Cost Optimization)
Your goal:
1. Keep **100%** of `ERROR` logs.
2. Keep only **10%** of `DEBUG` logs.

**How to do this:**
You will need to use the `rewrite_tag` filter combined with the `random` or `throttle` mechanisms.

**Fluent Bit logic:**
1. Match `level: DEBUG`.
2. Apply a `sampling` filter.
3. Match everything else and send to output.

---

## 🧪 Advanced Challenge: Lua Scripting
For precise AIOps preprocessing, Fluent Bit allows **Lua Scripts**. 

Create `mask.lua`:
```lua
function mask_acc(tag, timestamp, record)
    if record["acc"] ~= nil then
        record["acc"] = string.sub(record["acc"], 1, 2) .. "********"
    end
    return 1, timestamp, record
end
```

Update `fluent-bit.conf`:
```ini
[FILTER]
    Name    lua
    Match   *
    script  mask.lua
    call    mask_acc
```

---

## 🚀 Execution
1. Run Fluent Bit with the sample `finance.log`.
2. Verify that `DEBUG` logs are significantly reduced in the output.
3. Verify that `acc` numbers are masked.

## ✅ Deliverable
A functional `fluent-bit.conf` and `mask.lua` that demonstrates both privacy protection and intelligent data reduction.
