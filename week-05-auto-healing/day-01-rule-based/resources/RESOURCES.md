# Week 5 Day 1 Resources: Rule-Based Remediation

> "If you do it twice, automate it." - Every Sysadmin ever.

---

## 📚 Essential Reading

### The Philosophy
- **[Google SRE Book: Eliminating Toil](https://sre.google/sre-book/eliminating-toil/)** - Why manual work kills engineering velocity.
- **[The Twelve-Factor App: Processes](https://12factor.net/processes)** - Execute the app as one or more stateless processes.

### Tools & Standards
- **[Systemd for Administrators](https://www.freedesktop.org/wiki/Software/systemd/)** - The industry standard for process management on Linux.
- **[Supervisor: A Process Control System](http://supervisord.org/)** - The inspiration for today's project.
- **[Ansible: Intro to Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html)** - Agentless automation engine.

---

## 🛠️ Python Libraries

- **[psutil](https://psutil.readthedocs.io/en/latest/)** - Cross-platform process and system utilities.
- **[subprocess](https://docs.python.org/3/library/subprocess.html)** - Spawning new processes.
- **[requests](https://docs.python-requests.org/en/latest/)** - HTTP library for health checks.
- **[sh](https://amoffat.github.io/sh/)** - A full-fledged subprocess replacement (makes Python look like Bash).

```bash
pip install psutil
```

---

## 💡 Pro Tips for SREs

1.  **Don't Re-invent `systemd`:**
    - Today's project is educational. In production, use `systemd` unit files with `Restart=always`.
    - It handles PID tracking, logging, and dependencies natively.

2.  **The "Kill -9" Trap:**
    - `SIGKILL (-9)` kills instantly. The process cannot clean up (close DB connections, write logs).
    - Always try `SIGTERM (-15)` first. Wait 5 seconds. If still alive, THEN use `SIGKILL`.

3.  **Circuit Breakers:**
    - If a service crashes 5 times in 1 minute, **STOP RESTARTING IT**.
    - It's likely broken (bad config, bad deploy). Constant restarts just spam logs and burn CPU.
    - Alert a human instead.
