# Capstone Project: Requirements & Evaluation

> **Duration:** 20+ hours | Complete by end of Week 8

---

## 🎯 Overview

Your capstone project demonstrates mastery of all AIOps concepts covered in this bootcamp. Choose one of the project options and build a production-quality solution.

---

## 📋 Project Options

### Option 1: Full-Stack AIOps Platform
**Difficulty:** Advanced | **Best for:** Those wanting comprehensive experience

**Requirements:**
- Metrics ingestion from at least 2 sources
- Anomaly detection using ML (not just thresholds)
- Alert correlation and deduplication
- At least 1 auto-remediation action
- Dashboard with real-time updates

**Tech Stack Suggestion:**
- Prometheus + Grafana for metrics
- Python for ML models
- Redis/Kafka for event processing
- Ansible for remediation

---

### Option 2: Intelligent Log Analytics Platform
**Difficulty:** Intermediate-Advanced | **Best for:** Those interested in NLP/LLM

**Requirements:**
- Log collection from multiple sources
- Automatic log parsing and clustering (Drain3)
- Anomaly detection on log sequences
- LLM-powered root cause suggestions
- Search and visualization interface

**Tech Stack Suggestion:**
- Fluentd/Fluent Bit for collection
- Elasticsearch for storage
- Python + Drain3 for parsing
- OpenAI/Claude API for LLM features
- Kibana or custom UI

---

### Option 3: Predictive Alerting System  
**Difficulty:** Intermediate | **Best for:** Those interested in forecasting

**Requirements:**
- Time-series data collection
- Multiple forecasting models (Prophet, ARIMA)
- Dynamic threshold calculation
- SLA breach prediction
- Alert routing with priority scores

**Tech Stack Suggestion:**
- Prometheus for metrics
- Prophet/statsmodels for forecasting
- Python for model serving
- PagerDuty/Opsgenie integration
- Grafana for visualization

---

## 🏗️ Technical Requirements (All Options)

### Must Have
- [ ] Docker Compose for one-command deployment
- [ ] README with clear setup instructions
- [ ] Architecture documentation with diagrams
- [ ] At least one ML/AI component
- [ ] Working demo (local or cloud)

### Should Have  
- [ ] Test coverage (unit tests at minimum)
- [ ] Configuration via environment variables
- [ ] Logging and basic observability
- [ ] Error handling and resilience

### Nice to Have
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Load testing results
- [ ] Performance benchmarks

---

## 📊 Evaluation Rubric

### Technical Implementation (30 points)

| Score | Criteria |
|-------|----------|
| 25-30 | Production-quality code, clean architecture, excellent error handling |
| 18-24 | Good code quality, clear structure, handles edge cases |
| 10-17 | Working code, some organization, basic error handling |
| 0-9 | Incomplete or non-functional implementation |

### ML/AI Integration (25 points)

| Score | Criteria |
|-------|----------|
| 21-25 | Appropriate model selection, proper evaluation, clear improvement over baseline |
| 15-20 | Working ML component, basic evaluation |
| 8-14 | ML attempted, minimal evaluation |
| 0-7 | No meaningful ML integration |

### Documentation (20 points)

| Score | Criteria |
|-------|----------|
| 17-20 | Professional README, architecture diagrams, API docs, troubleshooting guide |
| 12-16 | Good README, some diagrams, setup instructions |
| 6-11 | Basic README, minimal documentation |
| 0-5 | Missing or inadequate documentation |

### Demo & Presentation (15 points)

| Score | Criteria |
|-------|----------|
| 13-15 | Clear narration, shows key features, handles questions well |
| 9-12 | Demonstrates main functionality, reasonable explanation |
| 5-8 | Basic demo, limited explanation |
| 0-4 | No demo or broken demo |

### Innovation (10 points)

| Score | Criteria |
|-------|----------|
| 9-10 | Novel approaches, extra features, goes beyond requirements |
| 6-8 | Some creative elements, solid execution |
| 3-5 | Meets basic requirements |
| 0-2 | Minimal effort beyond scaffolding |

**Total: 100 points | Passing: 70 points**

---

## 📅 Timeline

| Day | Milestone |
|-----|-----------|
| Day 1 | Choose project, set up repository, create architecture doc |
| Day 2 | Core infrastructure (Docker, basic services) |
| Day 3 | ML/AI component implementation |
| Day 4 | Integration, testing, polish |
| Day 5 | Documentation, demo preparation |
| Day 6 | Final testing, stretch goals |
| Day 7 | Presentation, peer review |

---

## 🚀 Submission

### Step 1: Create Project Repository
```bash
mkdir capstone-project
cd capstone-project
git init
```

### Step 2: Include Required Files
```
capstone-project/
├── README.md                # Setup, usage, architecture overview
├── ARCHITECTURE.md          # Detailed design decisions
├── docker-compose.yml       # One-command deployment
├── src/                     # Source code
├── tests/                   # Test files
├── notebooks/               # Any analysis notebooks
├── demo/                    # Screenshots, video link
└── .github/workflows/       # Optional CI/CD
```

### Step 3: Submit Pull Request
```bash
git checkout -b capstone/your-username
git add .
git commit -m "Capstone: [Project Name]"
git push origin capstone/your-username
```

Open a PR with:
- Project title
- Chosen option (1, 2, or 3)
- Demo link or video
- Self-assessment against rubric

---

## 💡 Tips for Success

1. **Start with architecture** - Plan before coding
2. **Get something working early** - Iterate from MVP
3. **Test as you go** - Don't leave testing to the end
4. **Document decisions** - Explain WHY, not just WHAT
5. **Ask for help** - Use Discussions when stuck
6. **Manage scope** - It's better to do less well than more poorly

---

## ❓ FAQ

**Q: Can I use a different tech stack?**
A: Yes, as long as you meet the requirements and justify your choices.

**Q: Can I work in a team?**
A: This is an individual project, but you can collaborate on ideas.

**Q: What if I can't meet the deadline?**
A: Communicate early. We can discuss extensions.

**Q: How long should the demo video be?**
A: 5-10 minutes maximum, covering key features.

---

<p align="center">
  <strong>Good luck! Build something you're proud to show employers.</strong>
</p>
