# Prerequisites Guide

> Ensure you meet these requirements before starting the AIOps Bootcamp.

---

## 📋 Required Skills

### 1. Python (Intermediate)

**What you need:**
- Write functions, classes, and modules
- Use pandas, numpy for data manipulation
- Basic understanding of APIs (requests library)
- Virtual environments (venv/conda)

**Self-Assessment:**
```python
# Can you understand and modify this code?
import pandas as pd
from dataclasses import dataclass

@dataclass
class Metric:
    name: str
    value: float
    timestamp: str

def process_metrics(metrics: list[Metric]) -> pd.DataFrame:
    df = pd.DataFrame([vars(m) for m in metrics])
    return df.groupby('name')['value'].mean()
```

**Brush up:** [Python for DevOps - Free Course](https://realpython.com/)

---

### 2. Linux/Command Line (Basic)

**What you need:**
- Navigate file system (cd, ls, pwd, find)
- File operations (cat, grep, awk, sed basics)
- Process management (ps, top, kill)
- SSH and remote connections
- Package management (apt/yum)

**Self-Assessment:**
```bash
# Can you explain what these commands do?
find /var/log -name "*.log" -mtime -1 | xargs grep -l "ERROR"
ps aux | grep python | awk '{print $2}' | xargs kill -9
```

**Brush up:** [Linux Command Line Basics](https://linuxjourney.com/)

---

### 3. Git/GitHub (Basic)

**What you need:**
- Clone, commit, push, pull
- Branching and merging
- Pull requests
- Basic conflict resolution

**Self-Assessment:**
```bash
# Can you execute this workflow?
git checkout -b feature/my-feature
git add .
git commit -m "Add new feature"
git push origin feature/my-feature
# Then create a PR on GitHub
```

**Brush up:** [Git Handbook](https://guides.github.com/introduction/git-handbook/)

---

### 4. Cloud Fundamentals (Basic)

**What you need:**
- Understand VMs, containers, serverless concepts
- Basic networking (VPC, subnets, load balancers)
- Object storage (S3/GCS/Blob)
- IAM basics

**Self-Assessment:**
- Can you deploy a simple app to AWS/GCP/Azure?
- Do you understand the difference between EC2 and Lambda?
- Can you explain what a VPC is?

**Brush up:** 
- [Cloud Engineering Foundation](https://github.com/pxkundu/AWS-cloud_engineering_topics)
- [AWS Cloud Practitioner](https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/)
- [GCP Fundamentals](https://cloud.google.com/training/cloud-infrastructure)

---

### 5. DevOps Concepts (Foundational)

**What you need:**
- CI/CD pipelines (GitHub Actions, Jenkins, etc.)
- Infrastructure as Code concepts
- Container basics (Docker)
- Basic monitoring concepts

**Self-Assessment:**
```yaml
# Can you understand this GitHub Actions workflow?
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build -t myapp .
      - run: docker run myapp pytest
```

**Brush up:** 
- [DevSecOps Bootcamp](https://github.com/pxkundu/DevSecOps-Bootcamp)
- [DevOps Roadmap](https://roadmap.sh/devops)
- [GenAI Builder Bootcamp](https://github.com/pxkundu/aws-genai-labs-builder)

---

## 💻 Required Setup

### Hardware
- **RAM**: 16GB minimum (32GB recommended)
- **Storage**: 50GB free space
- **CPU**: 4+ cores recommended

### Software (Install Before Week 1)

| Tool | Version | Purpose |
|------|---------|---------|
| Docker Desktop | Latest | Container runtime |
| Python | 3.10+ | Primary language |
| Git | Latest | Version control |
| VS Code / IDE | Latest | Code editing |
| kubectl | Latest | Kubernetes CLI |

### Accounts Needed
- [ ] GitHub account
- [ ] Docker Hub account
- [ ] Cloud account (AWS/GCP/Azure free tier)
- [ ] OpenAI API key (for Week 7)

---

## ✅ Ready Checklist

Before starting Week 1, confirm:

- [ ] Can write intermediate Python code
- [ ] Comfortable with Linux command line
- [ ] Can use Git for version control
- [ ] Have basic cloud knowledge
- [ ] Understand CI/CD concepts
- [ ] Docker Desktop installed and running
- [ ] Python 3.10+ installed
- [ ] All accounts created

---

## 🔄 Not Ready Yet?

If you need to brush up on prerequisites, we recommend:

| Gap | Resource | Time |
|-----|----------|------|
| Python | [Python for Everybody](https://www.py4e.com/) | 2 weeks |
| Linux | [Linux Journey](https://linuxjourney.com/) | 1 week |
| Git | [Learn Git Branching](https://learngitbranching.js.org/) | 2-3 days |
| Docker | [Docker Getting Started](https://docs.docker.com/get-started/) | 3-4 days |
| Cloud | [AWS/GCP Free Tier Labs](https://aws.amazon.com/free/) | 1 week |

---

<p align="center">
  <strong>Ready?</strong> → <a href="week-01-fundamentals/README.md">Start Week 1</a>
</p>
