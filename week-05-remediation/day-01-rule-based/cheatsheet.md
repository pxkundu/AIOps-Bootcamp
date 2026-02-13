# Remediation Cheat Sheet

> **Libraries:** `psutil`, `subprocess`, `requests`, `time`  
> **Tools:** Bash, Ansible

---

## 🐍 Python Process Management (psutil)

Inspect and kill processes safely.

```python
import psutil

# 1. Kill by Name
def kill_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            print(f"Killing {name} (PID: {proc.info['pid']})")
            proc.kill()

# 2. Check Memory Usage (Find Leaks)
def check_memory(limit_mb=500):
    for proc in psutil.process_iter(['name', 'memory_info']):
        mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
        if mem_mb > limit_mb:
            print(f"Warning: {proc.info['name']} creating memory leak ({mem_mb:.1f} MB)")
            return True
    return False

# 3. Kill Process Tree (Parent + Children)
def kill_tree(pid):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()
    parent.kill()
```

---

## 🐚 Shell Execution (subprocess)

Run Bash commands from Python. **Use list arguments** for safety (avoids shell injection).

```python
import subprocess

# 1. Start a Service
try:
    # Run and check output
    result = subprocess.run(
        ["systemctl", "start", "nginx"], 
        check=True, 
        capture_output=True, 
        text=True
    )
    print("Started Nginx successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to start Nginx: {e.stderr}")

# 2. Check if active
def is_active(service):
    res = subprocess.run(
        ["systemctl", "is-active", service], 
        capture_output=True, 
        text=True
    )
    return res.stdout.strip() == "active"
```

---

## ⏳ Exponential Backoff Logic

Retry with increasing delay.

```python
import time

def retry_function(func, max_retries=5):
    delay = 1
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2 # 1, 2, 4, 8, 16
    print("Give up.")
    return False
```

---

## 🤖 Ansible Playbook Sample (Restart)

Fix configuration drift.

```yaml
---
- name: Ensure Nginx is Running
  hosts: webservers
  tasks:
    - name: Check Nginx status
      service:
        name: nginx
        state: started
        enabled: yes
      register: result

    - name: Debug Output
      debug:
        msg: "Started Nginx"
      when: result.changed
```

---

## ⚡ Safety First: Idempotency

Ensure script can run multiple times safely.

```python
import os

# Create file ONLY if it doesn't exist
if not os.path.exists("config.txt"):
    with open("config.txt", "w") as f:
        f.write("setting=true")
else:
    print("Config already exists. Skipping.")
```
