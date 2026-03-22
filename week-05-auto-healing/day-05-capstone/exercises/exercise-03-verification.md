# Exercise 03: Post-Remediation Verification

## 🎯 Objective
Trust but Verify. Just because your script returned `True` doesn't mean the server is actually healthy. You must verify the fix.

---

## 🛠️ Task 1: The Verification Logic
Create a `verify_fix(service_name)` function.
- This function should wait 2 seconds (to allow startup).
- It should perform a health check (e.g., check if the process is actually running or ping the HTTP endpoint).

## 🛠️ Task 2: Closed-Loop Execution
Update your `handle_event` flow:
1.  Receive Alert.
2.  Run Healer.
3.  **Immediately call `verify_fix()`**.
4.  If `verify_fix` returns `False`:
    - Log `HEALER_FAILED`.
    - Try a secondary healer (e.g., if "Restart" failed, try "Re-deploy").
    - If all fail, mark as `CRITICAL_FAILURE`.

## 🛠️ Task 3: The Result
Your final JSON response from the webhook should include:
- `remediation_attempted`: True
- `verification_status`: Success/Failed

## 📝 Deliverable
A Python script that simulates a "flappy" service—one that restarts but dies immediately—and shows how your system detects that the "Fix" actually failed.
