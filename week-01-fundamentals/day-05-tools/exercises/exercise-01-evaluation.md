# Exercise 1: Real-World Tool Evaluation

## 🎯 Objective
Conduct a comprehensive tool evaluation for a realistic company scenario using structured decision-making.

---

## 📋 Company Scenario

**Company:** FinTech startup "PayFlow"

**Profile:**
- Industry: Financial Technology (Online Payments)
- Team Size: 75 engineers (8 SREs)
- Infrastructure: AWS (us-east-1, eu-west-1)
- Architecture: 120 microservices (Kubernetes)
- Traffic: 50M API requests/day
- Data Volume: ~200GB logs/day, 500k metrics/min
- Budget: $120,000/year for observability
- Compliance: PCI-DSS, SOC 2

**Current State:**
- Prometheus (self-hosted, frequently running out of disk)
- Grafana (10 critical dashboards)
- ELK Stack (expensive, complex to maintain)
- No distributed tracing currently
- 3-5 production incidents/week
- Mean Time to Resolution (MTTR): 2 hours

**Goals:**
- Reduce MTTR to < 30 minutes
- Implement distributed tracing
- Reduce SRE toil from manual log searches
- Improve incident detection (predictive alerts)
- Stay within budget

---

## 📊 Part 1: Requirements Gathering

### Task: Complete this Requirements Matrix

| Requirement | Priority (H/M/L) | Why? | Must-Have Features |
|-------------|------------------|------|-------------------|
| Distributed Tracing | | | |
| Log Aggregation | | | |
| Metrics Storage | | | |
| Anomaly Detection | | | |
| Alert Management | | | |
| Dashboard Creation | | | |
| API Monitoring | | | |
| Cost Optimization | | | |
| PCI-DSS Compliance | | | |
| Multi-Region Support | | | |

**Deliverable:** Filled matrix with justifications

---

## 🔍 Part 2: Vendor Research

### Task: Evaluate 3 Options

Research these three options:

**Option A: Datadog**
- Features:
- Pricing estimate:
- Pros:
- Cons:
- Compliance:

**Option B: Grafana Cloud + Prometheus + Tempo**
- Features:
- Pricing estimate:
- Pros:
- Cons:
- Compliance:

**Option C: Self-Hosted OTel Stack**
- Features:
- Infrastructure costs:
- Engineering costs:
- Pros:
- Cons:

### Pricing Calculation Template

```
Option A (Datadog):
- Infrastructure monitoring: ___ hosts × $15 = $___
- APM: ___ services × $31 = $___
- Log ingestion: ___ GB × $0.10 = $___
- Total monthly: $___
- Annual: $___

Option B (Grafana Cloud):
- Metrics: ___ series × $__ = $___
- Logs: ___ GB × $__ = $___
- Traces: ___ spans × $__ = $___
- Total monthly: $___
- Annual: $___

Option C (Self-Hosted):
- AWS costs (EC2, EBS, S3): $___
- Engineering time (setup): ___ weeks × $__ = $___
- Engineering time (maintenance): ___ FTE × $__ = $___
- Total Year 1: $___
```

---

## ⚖️ Part 3: Decision Matrix

### Task: Score Each Option

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| **Functional Fit** | 25% | /10 | /10 | /10 |
| **Total Cost (3 years)** | 30% | /10 | /10 | /10 |
| **Ease of Implementation** | 15% | /10 | /10 | /10 |
| **Vendor Lock-in Risk** | 10% | /10 | /10 | /10 |
| **Scalability** | 10% | /10 | /10 | /10 |
| **Support & SLA** | 10% | /10 | /10 | /10 |
| **Weighted Score** | 100% | | | |

**Calculation:**
```
Weighted Score = Σ(Score × Weight)
```

---

## 📝 Part 4: Recommendation Document

### Task: Write Executive Summary

Create `tool-evaluation-report.md` with:

#### 1. Executive Summary (1 paragraph)
- Recommendation
- Key reasons
- Expected ROI

#### 2. Detailed Analysis
- Requirements vs capabilities matrix
- TCO comparison (3-year)
- Risk assessment

#### 3. Implementation Plan
- Week 1-2: Setup
- Week 3-4: Migration
- Week 5-6: Training
- Week 7-8: Optimization

#### 4. Success Metrics
- MTTR target: < 30 min
- Alert noise reduction: 50%
- Dashboard adoption: 100% of SREs

---

## 🎯 Part 5: POC (Proof of Concept) Plan

### Task: Design a 2-Week POC

**Week 1: Setup & Instrumentation**
- [ ] Deploy chosen tool(s)
- [ ] Instrument 10 critical services
- [ ] Create 5 key dashboards
- [ ] Set up 3 alert rules

**Week 2: Evaluation**
- [ ] Simulate incident response
- [ ] Measure query performance
- [ ] Test alerting accuracy
- [ ] Calculate actual costs

**Success Criteria:**
1. Can trace a request across 5+ services
2. Find root cause of simulated issue in < 10 min
3. Dashboards load in < 2 seconds
4. No data loss during testing
5. Costs align with estimates (±15%)

---

## ✅ Deliverables

Submit:
1. **Completed requirements matrix** (Part 1)
2. **Vendor research with pricing** (Part 2)
3. **Decision matrix with scores** (Part 3)
4. **Executive recommendation** (Part 4)
5. **POC plan** (Part 5)

---

## 💡 Bonus Challenges

1. **Negotiation Strategy:** How would you negotiate a 25% discount?
2. **Migration Plan:** Detailed runbook for switching from current stack
3. **Rollback Plan:** What if the new tool doesn't work out?
4. **Buy vs Build:** Create a decision framework for when to build custom tooling

---

## 📚 Resources for Research

- Vendor pricing pages (check for hidden costs!)
- G2/Gartner reviews
- Reddit r/devops, r/sre discussions
- StackOverflow survey data
- CNCF landscape
