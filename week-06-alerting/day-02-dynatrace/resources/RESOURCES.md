# Week 6 Day 2 Resources: Dynatrace, Davis AI, & Causal RCA

Level up your RCA skills with these professional resources.

---

## 📚 Official Documentation
- **[Davis AI Overview](https://www.dynatrace.com/platform/davis-ai/)** - The official landing page for the Davis Engine.
- **[Problems API v2](https://www.dynatrace.com/support/help/dynatrace-api/environment-api/problems-v2)** - Reference for the API used in today's project.
- **[Smartscape Topology](https://www.dynatrace.com/support/help/platform/smartscape)** - How Dynatrace maps your entire IT landscape automatically.

---

## 🛠️ Specialized Tools
- **[Dynatrace CLI](https://github.com/dynatrace/dynatrace-cli)** - Official CLI for managing Dynatrace resources.
- **[Keptn](https://keptn.sh/)** - An open-source orchestrator for cloud-native apps that uses Dynatrace for automated "Quality Gates".
- **[Monaco (Monitoring as Code)](https://github.com/dynatrace/dynatrace-configuration-as-code)** - The enterprise tool for managing Dynatrace config across multiple environments.

---

## 🎓 Learning Paths
- **[Dynatrace University](https://university.dynatrace.com/)** - Extensive free training and certifications.
- **[Davis AI for SREs](https://www.dynatrace.com/news/blog/sre-enablement-with-davis-ai/)** - Deep dive blog into SRE workflows.

---

## 💡 Pro Tips for Causal RCA
1.  **Tagging is Life:** Just like with Datadog, use Automated Tagging Rules in Dynatrace to group your Azure resources by `Owner`, `Service`, and `Environment`.
2.  **Topological Quality:** Davis is only as good as the map. Use **OneAgent** wherever possible because it auto-discovers dependencies that manual logs won't show.
3.  **Root Cause vs Impact:** Remember that a single root cause can impact many components. Always fix the **Root Cause Entity** first, and the rest will recover automatically.
