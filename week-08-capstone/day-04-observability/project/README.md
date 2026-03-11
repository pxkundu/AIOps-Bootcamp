# Project Guide: Enterprise Observability Hub — Step-by-Step

Build a complete observability, monitoring, logging, and alerting platform using Glean's connector patterns.

---

## 📋 Prerequisites

| Requirement | Installation |
|-------------|-------------|
| **Python 3.10+** | `brew install python` |
| **Flask** | `pip install flask` |
| **Pandas** | `pip install pandas` |

---

## 🏗️ Phase 1: Run the Connector Framework

### Step 1.1: Start all connectors and crawl data

```bash
cd project/src
python connectors/connector_framework.py
```

**Expected Output:**
```
🔄 [PagerDuty] Starting crawl...
✅ [PagerDuty] Crawl complete. 2 items synced.
🔄 [Slack] Starting crawl...
✅ [Slack] Crawl complete. 2 items synced.
🔄 [Jira] Starting crawl...
✅ [Jira] Crawl complete. 1 items synced.
🔄 [GitHub] Starting crawl...
✅ [GitHub] Crawl complete. 1 items synced.
🔄 [CloudWatch] Starting crawl...
✅ [CloudWatch] Crawl complete. 1 items synced.
```

Each connector follows the **Glean crawl lifecycle**: `Configured → Crawling → Indexing → Active`.

---

## 📊 Phase 2: Monitor Connector Health

### Step 2.1: Run the Health Monitor

```bash
python monitoring/health_monitor.py
```

**What to Look For (per Glean docs):**
- `items_synced`: Should increase over time during initial crawl.
- `change_rate_per_day`: A 0 value when activity is expected means check your config.
- `status`: "Active" = healthy. "Error" = investigate immediately.

---

## 🔗 Phase 3: Run the Alert Correlator

### Step 3.1: Test cross-source correlation

```bash
python alerting/alert_correlator.py
```

**Expected Output:**
The correlator groups signals from PagerDuty, Slack, GitHub, and CloudWatch by service (e.g., `database`) and generates:
- **RCA hypothesis**: "A recent code change (GitHub) likely caused the database incident."
- **Suggested actions**: "Roll back recent DB migration", "Check slow query logs".

---

## 🛰️ Phase 4: Start the MCP Action Server

### Step 4.1: Launch the action server

```bash
python alerting/mcp_action_server.py
```

### Step 4.2: View available tools

```bash
curl http://localhost:5002/mcp/v1/tools | python -m json.tool
```

### Step 4.3: Acknowledge an incident (Human-in-the-Loop)

**First call (requires confirmation):**
```bash
curl -X POST http://localhost:5002/mcp/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "acknowledge_incident", "parameters": {"incident_id": "INC-001"}, "user": "alice"}'
```

**Second call (with confirmation):**
```bash
curl -X POST http://localhost:5002/mcp/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "acknowledge_incident", "parameters": {"incident_id": "INC-001"}, "user": "alice", "confirmed": true}'
```

### Step 4.4: Create a Jira RCA ticket

```bash
curl -X POST http://localhost:5002/mcp/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "create_jira_ticket", "parameters": {"summary": "P1 RCA: DB Latency Spike", "description": "Root cause: index rebuild from PR #1482", "priority": "High"}, "user": "alice", "confirmed": true}'
```

### Step 4.5: View the audit trail

```bash
curl http://localhost:5002/mcp/v1/execute \
  -X POST -H "Content-Type: application/json" \
  -d '{"tool": "get_audit_log", "user": "admin"}'
```

---

## 🔭 Phase 5: Launch the Observability Dashboard

### Step 5.1: Start the full hub

```bash
python app.py
```

### Step 5.2: Open in browser

Navigate to `http://localhost:5003`

You will see:
- **Knowledge Object count** across all 5 connectors.
- **Connector health table** with sync status and change rates.
- **Correlated incidents** with RCA suggestions and remediation actions.

---

## 📄 Phase 6: Generate Connector Reports

### Step 6.1: Launch the Interactive Report Generator

```bash
python scripts/report_generator.py
```

### Step 6.2: Select a report type

```
📋 Available Reports:
  [0] Full Aggregate Report (all connectors)
  [1] PagerDuty (Incident Management)
  [2] Slack (Communication)
  [3] Jira (Project Management)
  [4] GitHub (Source Control)
  [5] CloudWatch (Monitoring)
  [q] Quit

👉 Select report number:
```

### Step 6.3: Individual connector reports include:

- **Status & Health**: Sync status, items synced, change rate, last crawl time.
- **ACL Summary**: Total indexed objects and list of authorized groups.
- **Content Summary**: Knowledge objects broken down by author.
- **Metadata Fields**: All metadata keys and unique values per connector.
- **Sample Objects**: First 3 crawled knowledge objects for inspection.

### Step 6.4: Aggregate reports include:

- **Platform Summary**: Total connectors, healthy/warning/critical counts, total items indexed.
- **Per-Connector Health**: Status and metrics for each connector.
- **Active Alerts**: Warnings and critical alerts from the health monitor.
- **Correlated Incidents**: Cross-source RCA incidents with suggested actions.
- **All Individual Reports**: Full detail for every connector in a single file.

Reports are saved as JSON to `project/src/reports/`.

---

## 🖥️ Phase 7: Open the HTML Monitoring Dashboard

### Step 7.1: Open the static dashboard

```bash
open monitoring/dashboard.html
# Or on Linux: xdg-open monitoring/dashboard.html
```

### Step 7.2: Dashboard features

The dashboard provides a reference-grade visualization of all Glean connector monitoring data:

| Section | Description |
|---------|-------------|
| **Summary Cards** | Total connectors, healthy, warning, critical counts, total items |
| **Sync Status Table** | Per-connector status, items synced, change rate, 7-day sparkline, visibility |
| **Active Alerts** | Stalled and errored connectors with remediation guidance |
| **Content Distribution** | Items broken down by type (incidents, messages, tickets, code, metrics) |

---

## 📂 File Map

| File | Purpose |
|------|---------|
| `connectors/connector_framework.py` | Base connector class + 5 native/custom connectors |
| `monitoring/health_monitor.py` | Sync status tracking and stall detection |
| `monitoring/dashboard.html` | Static HTML monitoring dashboard with sparklines and alerts |
| `alerting/alert_correlator.py` | Cross-source signal correlation and RCA |
| `alerting/mcp_action_server.py` | MCP action server with human-in-the-loop |
| `scripts/report_generator.py` | Interactive CLI for per-connector and aggregate reports |
| `app.py` | Main Flask dashboard that ties everything together |
| `config/observability_config.json` | Connector + alerting + MCP configuration |

---

## 🔧 Configuration Reference

### Connector Data Rules (from `observability_config.json`)

| Connector | Include | Exclude |
|-----------|---------|---------|
| **Slack** | `#sre-war-room`, `#production-alerts` | `#hr-confidential`, `#finance-internal` |
| **GitHub** | `enterprise/payment-service` | `enterprise/secret-configs` |
| **CloudWatch** | `AWS/RDS`, `AWS/EC2` namespaces | — |

### Visibility Rollout (per Glean best practices)

1. Set new connectors to **"test-group-only"**.
2. Verify results with SRE team.
3. Promote to **"visible-to-everyone"** after validation.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../resources/RESOURCES.md">Next: Resources ➡️</a>
</p>
