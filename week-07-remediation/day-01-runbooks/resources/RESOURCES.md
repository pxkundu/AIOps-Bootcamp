# Resources: Runbook Automation & Self-Healing

Learn more about the tools and patterns used for automated remediation.

---

## 🛠️ Tools & Libraries

- **Ansible Documentation**: [Official Guide](https://docs.ansible.com/ansible/latest/index.html)
- **Ansible Runner**: [Python API for Ansible](https://ansible-runner.readthedocs.io/en/latest/)
- **StackStorm**: [Event-Driven Automation Platform](https://stackstorm.com/) (Industrial-strength alternative to our Python controller).
- **Argo Events**: [Event-Driven Workflows for Kubernetes](https://argoproj.github.io/argo-events/)

## 📖 Key Readings

- **Google SRE Book**: [Automation](https://sre.google/sre-book/automation/) - A must-read on the philosophy of SRE automation.
- **The Ideal Runbook**: [What makes a good runbook?](https://www.pagerduty.com/resources/learn/what-is-a-runbook/)
- **Idempotency in Ops**: [Why it matters for self-healing](https://www.ansible.com/blog/ansible-idempotency-explained)

## 📺 Videos & Tutorials

- **Ansible for Beginners**: [10-Minute Crash Course](https://www.youtube.com/watch?v=gocwRvLhDf8)
- **Self-Healing Systems at Scale**: [Netflix Case Study](https://www.youtube.com/watch?v=0pLq0K7M468)

## 🧠 Theory: The OODA Loop
Automated remediation is often modeled after the **OODA Loop**:
1. **Observe**: Collect telemetry.
2. **Orient**: Contextualize the failure (RCA).
3. **Decide**: Select the appropriate playbook.
4. **Act**: Execute and verify.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../project/README.md">Next: Project ➡️</a>
</p>
