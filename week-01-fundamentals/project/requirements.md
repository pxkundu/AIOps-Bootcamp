# Week 1 Project: Build Your Observability Foundation

> **Duration:** 4-6 hours | **Difficulty:** Intermediate

---

## 🎯 Project Overview

Build a complete observability setup for a sample application, demonstrating your mastery of Week 1 concepts.

---

## 📋 Requirements

### Core Requirements (Must Complete)

1. **Deploy Observability Stack**
   - Prometheus running and scraping targets
   - Grafana with configured datasources
   - Jaeger collecting traces

2. **Instrument Sample Application**
   - Add OpenTelemetry instrumentation
   - Export metrics to Prometheus
   - Export traces to Jaeger

3. **Create Dashboard**
   - Request rate panel
   - Error rate panel
   - Latency percentiles panel
   - At least one custom panel

4. **Documentation**
   - README with setup instructions
   - Architecture diagram
   - Key decisions explained

### Stretch Goals (Optional)

- [ ] Add alerting rules in Prometheus
- [ ] Configure Grafana alerts
- [ ] Add log collection with Loki
- [ ] Create a troubleshooting runbook
- [ ] Deploy to Kubernetes (Minikube)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Your Observability Stack                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│    │  Demo App    │    │ Prometheus   │    │   Jaeger     │    │
│    │  (Python)    │───▶│  :9090       │    │   :16686     │    │
│    │  :8080       │    └──────┬───────┘    └──────▲───────┘    │
│    └──────┬───────┘           │                   │            │
│           │                   │                   │            │
│           │ OTel Proto        │ PromQL            │ Traces     │
│           │                   │                   │            │
│           └───────────────────┼───────────────────┘            │
│                               │                                 │
│                        ┌──────▼───────┐                        │
│                        │   Grafana    │                        │
│                        │   :3000      │                        │
│                        └──────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
project/
├── README.md                 # Your documentation
├── docker-compose.yml        # Complete stack
├── prometheus/
│   └── prometheus.yml        # Prometheus config
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       └── dashboards/
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
└── docs/
    └── architecture.md       # Architecture decisions
```

---

## 📊 Evaluation Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| **Stack Deployment** | 20 | All services running, properly connected |
| **Instrumentation** | 25 | OTel correctly configured, custom spans/metrics |
| **Dashboard** | 25 | Useful visualizations, good design |
| **Documentation** | 20 | Clear README, architecture explained |
| **Stretch Goals** | 10 | Each completed stretch goal |
| **Total** | 100 | |

---

## 🚀 Getting Started

1. Copy the starter code:
   ```bash
   cp -r ../day-03-instrumentation/demo-app ./app
   cp ../day-02-observability/docker-compose.yml ./
   ```

2. Customize and extend

3. Test your setup:
   ```bash
   docker-compose up -d
   # Generate traffic
   ./load-test.sh
   # Check all UIs
   ```

4. Document everything in README.md

---

## 📝 Submission

Create a new branch and submit:
```bash
git checkout -b week-01-project/your-username
git add .
git commit -m "Week 1 Project: Observability Foundation"
git push origin week-01-project/your-username
```

Then open a Pull Request for review.

---

## 💡 Tips

- Start simple, then add complexity
- Test each component before integrating
- Use Docker logs for debugging
- Check the cheatsheets when stuck
- Ask questions in Discussions!

---

<p align="center">
  <strong>Good luck!</strong> → <a href="../../week-02-data-engineering/">Continue to Week 2</a>
</p>
