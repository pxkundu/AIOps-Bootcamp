# Project Guide: AI Transformation Platform

Build a platform that operationalizes the Glean Work AI Institute's "AI Transformation 100" framework.

---

## 📋 Prerequisites

| Requirement | Installation |
|-------------|-------------|
| **Python 3.10+** | `brew install python` |
| **Flask** | `pip install flask` |

---

## 🧪 Phase 1: Run the Assessment Engine

```bash
cd project/src
python platform/assessment_engine.py
```

**Expected output:** A full maturity report with 10-pillar scores, strengths, gaps, priority actions, and ROI estimates.

---

## 🤖 Phase 2: Run the AI Agents

```bash
python agents/transformation_agents.py
```

**Expected output:** Scan results from 4 agents — Sludge Detector (847 hrs/week waste), Champion Finder (10 champions), Coordination Auditor (6 workflow bottlenecks), Innovation Scanner (AI theater detection).

---

## 🚀 Phase 3: Launch the Platform

```bash
python app.py
```

Navigate to `http://localhost:5006`

**Dashboard shows:**
- Overall maturity score (radar-style per pillar)
- Sludge detection results with impact scores
- AI champion leaderboard
- Coordination audit with tool count and toggle tax
- Innovation portfolio with AI theater flagging
- Estimated annual ROI

---

## 📡 Phase 4: Explore the APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/assessment` | GET | Full 10-pillar maturity assessment |
| `/api/agents` | GET | All agent scan results |
| `/api/pillars` | GET | 10-pillar definitions and questions |
| `/api/sludge` | GET | Administrative sludge analysis |
| `/api/champions` | GET | AI champion identification |
| `/api/coordination` | GET | Coordination tax audit |
| `/api/innovation` | GET | Innovation portfolio health |

```bash
curl http://localhost:5006/api/sludge | python -m json.tool
```

---

## 📂 File Map

| `platform/assessment_engine.py` | 10-pillar scoring engine with 30 questions and 80+ recommendations |
| `agents/transformation_agents.py` | 4 AI agents: Sludge, Champions, Coordination, Innovation |
| `app.py` | Flask dashboard with dark-themed UI and 7 API endpoints |
| `scripts/deploy_platform.sh` | Shell script for infrastructure setup and platform launch |
| `scripts/generate_report.py` | Executive report generator for enterprise discovery results |
| `config/platform_config.json` | Core platform settings, ROI formulas, and Agentic scan parameters |
| `config/pillar_config.json` | Detailed pillar weighting, industry benchmarks, and ROI timelines |

---

## 🛠️ Phase 5: Run Executive Discovery Report

If you want a paper-ready report of your organization's AI Transformation readiness:

```bash
python scripts/generate_report.py
```

**Outcome:** Creates `enterprise_scan_report.md` with prioritized sludge targets and champion leaderboards.

---

## 🐳 Phase 6: Automated Deployment

To provision and launch the entire platform in one go:

```bash
bash scripts/deploy_platform.sh
```


---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../resources/RESOURCES.md">Next: Resources ➡️</a>
</p>
