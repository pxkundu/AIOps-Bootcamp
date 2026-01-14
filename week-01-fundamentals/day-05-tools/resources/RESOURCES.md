# Day 5 Resources: Vendor & Tool Research Guide

> **Navigate the complex landscape of AIOps and observability tools.**

---

## 🌐 Official Vendor Resources

### All-in-One Platforms

**Datadog**
*   [Official Documentation](https://docs.datadoghq.com/)
*   [Pricing Calculator](https://www.datadoghq.com/pricing/)
*   [Community Forum](https://community.datadoghq.com/)
*   [Status Page](https://status.datadoghq.com/)

**New Relic**
*   [Documentation](https://docs.newrelic.com/)
*   [Pricing](https://newrelic.com/pricing)
*   [University (Free Training)](https://learn.newrelic.com/)
*   [Nerd Blog](https://newrelic.com/blog)

**Dynatrace**
*   [Documentation](https://www.dynatrace.com/support/help)
*   [Pricing](https://www.dynatrace.com/pricing/)
*   [Perform Conference](https://www.dynatrace.com/perform/)
*   [Davis AI Guide](https://www.dynatrace.com/platform/artificial-intelligence/)

**Splunk**
*   [Docs](https://docs.splunk.com/)
*   [Observability Cloud](https://www.splunk.com/en_us/products/observability-cloud.html)
*   [.conf (Annual Conference)](https://conf.splunk.com/)

---

## 📊 Comparison & Research Sites

### Independent Reviews
*   **[G2](https://www.g2.com/categories/application-performance-monitoring)** - User reviews and ratings
*   **[Gartner Peer Insights](https://www.gartner.com/reviews/market/application-performance-monitoring)** - Enterprise reviews
*   **[TrustRadius](https://www.trustradius.com/apm-application-performance-monitoring)** - Detailed buyer guides

### Market Analysis
*   **[Gartner Magic Quadrant for APM](https://www.gartner.com/en/documents/magic-quadrant-application-performance-monitoring)** - Annual analysis
*   **[Forrester Wave for AIOps](https://www.forrester.com/)** - Vendor comparisons
*   **[IDC MarketScape](https://www.idc.com/)** - Market sizing and trends

### Community Resources
*   **[r/devops Tool Discussions](https://www.reddit.com/r/devops/)** - Real-world experiences
*   **[r/sre](https://www.reddit.com/r/sre/)** - SRE perspectives on tools
*   **[CNCF Slack](https://cloud-native.slack.com/)** - #observability channel
*   **[SREcon Talks](https://www.usenix.org/conferences/srecon)** - Tool usage case studies

---

## 💰 Understanding Pricing Models

### Common Pricing Dimensions

| Vendor | Primary Metric | Additional Charges | Hidden Costs |
|--------|---------------|-------------------|---------------|
| **Datadog** | Hosts + APM hosts | Logs ($0.10/GB), Custom metrics, Spans | Retention beyond 15 days |
| **New Relic** | GB ingested | Compute units, Users | Query complexity |
| **Dynatrace** | Full-stack monitoring units | DEM, Session Replay | Professional services |
| **Splunk** | GB indexed | Search heads, Indexers | Infrastructure |
| **Grafana Cloud** | Metrics series + Log GB | Traces, Profiles | - |

### Negotiation Tips

1. **Request POC Credits:** Most vendors offer $5k-10k in credits for evaluation
2. **Annual Commitment:** 20-30% discount for annual vs monthly
3. **Competitor Leverage:** "Vendor X offered us..."
4. **Volume Discounts:** Negotiate better rates at scale
5. **Contract Terms:** Push back on auto-renewal clauses

---

## 🎓 Training & Certification

### Free Training Programs

**Datadog Learning Center**
- Foundation course (2 hours)
- APM Deep Dive (3 hours)
- Free certification exam

**New Relic University**
- Full Stack Observability (4 hours)
- Observability Maturity (2 hours)
- Free certificates

**Grafana Labs**
- Grafana Fundamentals (3 hours)
- Loki Tutorial (2 hours)
- All free on YouTube

**Prometheus Tutorials**
- [PromCon](https://promcon.io/) videos
- [Robust Perception Blog](https://www.robustperception.io/blog)

---

## 📚 Books & White Papers

### Essential Reading

**"Observability Engineering" by Charity Majors et al.**
- Focus: Cultural shift to observability
- Relevance: Tool-agnostic principles
- Where: O'Reilly

**"The Art of Monitoring" by James Turnbull**
- Focus: Practical monitoring with open-source tools
- Relevance: Prometheus, Grafana patterns
- Where: Turnbull Press

**Vendor White Papers:**
- **[Dynatrace: State of Cloud Observability](https://www.dynatrace.com/resources/)** - Annual report
- **[New Relic: Observability Forecast](https://newrelic.com/resources)** - Trends
- **[Datadog: Monitoring Modern Infrastructure](https://www.datadoghq.com/state-of-monitoring/)** - Real data from customers

---

## 🛠️ Evaluation Tools

### Vendor Assessment Checklist

Use this when evaluating any tool:

**Technical Fit:**
- [ ] Supports our languages/frameworks
- [ ] Integrates with our CI/CD
- [ ] Handles our data volume
- [ ] Meets compliance requirements (HIPAA, SOC 2, etc.)
- [ ] Supports our deployment model (cloud/on-prem/hybrid)

**Operational:**
- [ ] Setup time < 1 week
- [ ] Team can learn in < 1 month
- [ ] Maintenance requires < 0.5 FTE
- [ ] Uptime SLA > 99.9%
- [ ] Support response time acceptable

**Commercial:**
- [ ] Fits within budget (including growth)
- [ ] Contract terms acceptable
- [ ] No forced bundling
- [ ] Data export capabilities (avoid lock-in)
- [ ] Transparent pricing (no hidden fees)

---

## 🔬 POC (Proof of Concept) Framework

### Week 1: Setup
- Day 1-2: Deploy tool
- Day 3-4: Instrument 5-10 services
- Day 5: Create dashboards

### Week 2: Evaluation
- Day 1-2: Simulate incidents, test RCA
- Day 3: Performance testing (query speed, data lag)
- Day 4: Cost validation
- Day 5: Team feedback collection

### Success Metrics:
1. **Functional:** Can we solve our top 3 pain points?
2. **Performance:** Dashboards load in < 3 seconds?
3. **Ease of Use:** Can junior engineer use it after 1 day training?
4. **Cost:** Actual spend within 15% of estimate?

---

## 📈 Emerging Vendors to Watch

### Next-Generation Tools (2026)

**OpenTelemetry Native:**
- **[SigNoz](https://signoz.io/)** - Open-source, OTel-first APM
- **[Highlight.io](https://www.highlight.io/)** - Session replay + observability
- **[Odigos](https://odigos.io/)** - Auto-instrumentation for K8s

**eBPF-Based:**
- **[Pixie](https://pixie.io/)** (acquired by New Relic) - Zero instrumentation
- **[Parca](https://www.parca.dev/)** - Continuous profiling
- **[Cilium/Hubble](https://cilium.io/)** - Network observability

**AI-First:**
- **[Anodot](https://www.anodot.com/)** - Autonomous anomaly detection
- **[Mona](https://www.monalabs.io/)** - AI Observability (for ML models)

---

## 🎯 Vendor Selection: Real Case Studies

### Case Study 1: E-Commerce Startup → Datadog
**Scale:** 50 microservices, $5M ARR
**Why:** Fast setup, great UX, integrated APM
**Cost:** $3k/month
**Lesson:** Pay for convenience when you're growing fast

### Case Study 2: Enterprise Bank → Dynatrace
**Scale:** 500+ apps, heavily hybrid (cloud + mainframe)
**Why:** Auto-discovery, Davis AI, enterprise support
**Cost:** $500k/year
**Lesson:** Enterprise features justify premium pricing

### Case Study 3: Tech Company → Grafana Cloud
**Scale:** 200 microservices, cost-conscious
**Why:** OTel-native, no vendor lock-in, transparent pricing
**Cost:** $1.5k/month
**Lesson:** Open-source familiarity reduces learning curve

---

## 💡 Anti-Patterns to Avoid

1. **Tool Sprawl:** Don't use 10 different tools "because they're best-of-breed"
2. **Shiny Object Syndrome:** Don't switch tools every year
3. **Blind RFP:** Don't select a tool without hands-on POC
4. **Ignoring TCO:** Don't forget engineering costs of self-hosted solutions
5. **Vendor Lock-in:** Don't use proprietary SDKs (use OTel!)

---

<p align="center">
  <a href="../lecture-notes.md">Back to Lecture Notes</a>
</p>
