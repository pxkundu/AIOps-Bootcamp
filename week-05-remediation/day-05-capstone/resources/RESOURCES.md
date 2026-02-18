# Week 5 Capstone Resources: Self-Healing Architecture

Congratulations on reaching the Capstone! Below are resources to help you transition from this simulation to production-ready autonomous systems.

---

## 🏗️ Production Tools (Aegis in Real Life)

1.  **[StackStorm (Extreme Automation)](https://stackstorm.com/)**: Probably the closest thing to "Project Aegis" in the open-source world. It uses "Sensors" to listen for events and "Workflows" to heal systems.
2.  **[PagerDuty Process Automation](https://www.pagerduty.com/platform/automation/)**: Formerly Rundeck. The industry standard for runbook automation and self-healing.
3.  **[Argo CD & Notifications](https://argocd-notifications.readthedocs.io/)**: For self-healing in Kubernetes (GitOps pattern).
4.  **[Falco](https://falco.org/)**: For security-focused self-healing. Detecting threats in real-time and triggering block actions.

---

## 📖 Essential Reading & Case Studies

1.  **[The Netflix Chaos Monkey](https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116)**: How Netflix perfected the art of failing on purpose to test their self-healing.
2.  **[Google SRE Book: Automation](https://sre.google/sre-book/automation-at-google/)**: The philosophy of eliminating toil through automation.
3.  **[MAPE-K Loop in Autonomous Computing](https://en.wikipedia.org/wiki/Autonomic_computing#The_MAPE-K_Loop)**: The formal architectural definition of what you built today.

---

## 🎓 Career Path: The Autonomous Engineer

Building Project Aegis moves you from a "Support Engineer" to an **AIOps/Reliability Architect**. 

**Focus areas for your next steps:**
- **Security Automation (SOAR):** Building healing loops for security incidents.
- **FinOps Automation:** Building loops to scale down or delete unused resources to save money.
- **Canary Automation:** Using AI to decide if a new deployment is healthy or should be rolled back.

---

## ✅ Capstone Checklist
- [ ] Is my system idempotent?
- [ ] Do I have a "Human Escalation" path?
- [ ] Is every action logged for auditing?
- [ ] Does my system respect maintenance/backup windows?

**You are now and AIOps Remediation Specialist!**
