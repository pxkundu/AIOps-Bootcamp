# Week 5 Day 2 Resources: Context-Aware Remediation

> "It's not a bug, it's a feature." - context matters.

---

## 📚 Essential Reading

### The Theory of Smart Triage
- **[Interpretable Machine Learning (Christoph Molnar)](https://christophm.github.io/interpretable-ml-book/)** - Why simple models (Trees) beat Black Boxes (Neural Nets) for Ops.
- **[Google SRE: Symptoms vs Causes](https://sre.google/sre-book/monitoring-distributed-systems/#symptoms-versus-causes)** - Why alert on symptoms, but act on causes.

### Industry Examples
- **[Netflix Automated Canary Analysis (Kayenta)](https://netflixtechblog.com/automated-canary-analysis-at-netflix-with-kayenta-3260bc7169c2)** - Using stats to decide "Rollback or Promote?".
- **[PagerDuty Event Intelligence](https://www.pagerduty.com/platform/event-intelligence/)** - Automatic grouping and context enrichment for alerts.

---

## 🛠️ Tools & Libraries

- **[scikit-learn (Decision Trees)](https://scikit-learn.org/stable/modules/tree.html)** - The core logic engine.
- **[SHAP (SHapley Additive exPlanations)](https://shap.readthedocs.io/en/latest/)** - Explain *why* the model made a decision.
- **[Drools (Java)](https://www.drools.org/)** - Enterprise-grade Rule Engine (if Python is too small).

---

## 💡 Pro Tips for SREs

1.  **Start Simple (Manual Tree):**
    - Don't jump to ML immediately.
    - Write a Python script with `if/elif`. 
    - Only use ML when the rules become unmanageable (> 50 rules).

2.  **Explainability is Mandatory:**
    - If your bot restarts the DB, it MUST say why.
    - Bad: "Restarting DB."
    - Good: "Restarting DB because (CPU > 95%) AND (No Backup Running)."

3.  **The "Human in the Loop" Pattern:**
    - For high-risk actions (Drop Data), the bot should Slack a human: "I recommend dropping table X. [Approve/Deny]".
    - Record the human's choice to train the model for next time.
