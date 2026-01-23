# Exercise: Building a GitHub Health Exporter

## 🎯 Objective
Create a custom Prometheus exporter that scrapes the GitHub API to monitor "Project Health" (Open Issues, PR Velocity). You will then use Prometheus relabeling to clean up the data.

---

## 📋 Prerequisites
- Python 3.10+
- `pip install prometheus_client requests`
- (Optional) A GitHub Personal Access Token (to avoid rate limits)

---

## 🛠️ Step 1: Writing the Exporter

Create a file named `github_exporter.py`:

```python
import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Define your metrics
REPO_ISSUES = Gauge('github_repo_open_issues', 'Number of open issues', ['repo', 'owner'])
REPO_STARS = Gauge('github_repo_stars', 'Number of stars', ['repo', 'owner'])

def fetch_metrics():
    # Target repository
    owner = "prometheus"
    repo = "prometheus"
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    print(f"Fetching data from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        REPO_ISSUES.labels(repo=repo, owner=owner).set(data['open_issues_count'])
        REPO_STARS.labels(repo=repo, owner=owner).set(data['stargazers_count'])
    else:
        print(f"Error fetching data: {response.status_code}")

if __name__ == "__main__":
    # Start the exporter on port 8000
    start_http_server(8000)
    print("Exporter started on port 8000")
    
    while True:
        fetch_metrics()
        # GitHub API has strict rate limits, don't scrape too fast!
        time.sleep(60) 
```

---

## ⚙️ Step 2: Prometheus Integration

Update your `prometheus.yml` to scrape this new exporter:

```yaml
scrape_configs:
  - job_name: 'github_health'
    static_configs:
      - targets: ['host.docker.internal:8000']
    
    # Task: Relabeling
    metric_relabel_configs:
      - source_labels: [owner]
        target_label: org
        action: replace
      - regex: 'repo' # Practice dropping a label
        action: labeldrop
```

---

## 🚀 Step 3: Run and Verify

1. **Start Exporter:** `python github_exporter.py`
2. **Scrape:** `curl localhost:8000/metrics`
3. **Analyze:** Open Prometheus UI (localhost:9090) and search for `github_repo_open_issues`.

---

## 🧪 Challenge Questions

1. **Labels:** Why did we use `Gauge` instead of `Counter` for "Open Issues"? 
2. **Cardinality:** If you were to add `issue_id` as a label to track every single issue's age, what would happen to Prometheus if the repo had 50,000 issues?
3. **Relabeling:** Did the `labeldrop` action work? Look at the metric in Prometheus—is the `repo` label gone? (Note: `labeldrop` is aggressive—use it only when you've already aggregated the data).

---

## ✅ Deliverable
Show your `github_exporter.py` and a screenshot of Prometheus showing the renamed `org` label and the absence of the `repo` label.
