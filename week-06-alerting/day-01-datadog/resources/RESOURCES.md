# Week 6 Day 1 Resources: Datadog & AIOps

Optimize your alerting strategies with these industry-grade resources.

---

## 📚 Official Documentation
- **[Datadog Watchdog](https://docs.datadoghq.com/watchdog/)** - Automated anomaly detection for traces and metrics.
- **[Monitor Anomaly Detection](https://docs.datadoghq.com/monitors/types/anomaly/)** - Detailed guide on algorithms like `agile`, `robust`, and `basic`.
- **[Datadog API Reference](https://docs.datadoghq.com/api/latest/)** - Everything you need for Monitoring-as-Code.

---

## 🛠️ Specialized Tools
- **[Dogshell](https://github.com/DataDog/dogshell)** - A CLI tool to interact with the Datadog API directly from your terminal.
- **[Terraform Datadog Provider](https://registry.terraform.io/providers/DataDog/datadog/latest/docs)** - Manage thousands of monitors using HCL code.

---

## 🎓 Learning Paths
- **[Datadog Learning Center](https://learn.datadoghq.com/)** - Free courses on observability and alerting.
- **[SRE Fundamentals at Datadog](https://www.datadoghq.com/blog/sre-fundamentals/)** - Blog series on modern reliability practices.

---

## 💡 Pro Tips for The Noise Canceller
1.  **Use 'Multi-Alert':** Never create one monitor per host. Use `avg by {host}` to create one monitor that manages 1000 hosts.
2.  **The 2-Minute Rule:** If an anomaly lasts less than 2 minutes, ignore it. Spikes happen; patterns matter.
3.  **Tag Everything:** Correlation is impossible without a consistent tagging strategy (e.g., `env`, `service`, `team`).
