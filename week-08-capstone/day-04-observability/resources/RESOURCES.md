# Resources: Enterprise Observability with Glean Connectors

Official documentation, reference architectures, and learning materials.

---

## 🔍 Glean Connector Documentation

- **Connectors Hub**: [docs.glean.com/connectors/home](https://docs.glean.com/connectors/home) — Full catalog of 100+ native connectors.
- **About Connectors**: [docs.glean.com/connectors/about](https://docs.glean.com/connectors/about) — Architecture and crawling fundamentals.
- **Managing Connectors**: [docs.glean.com/connectors/monitoring](https://docs.glean.com/connectors/monitoring) — Sync status, metrics, troubleshooting, and visibility controls.
- **Custom Connectors**: [docs.glean.com/connectors/custom/about](https://docs.glean.com/connectors/custom/about) — Build your own connector using the Glean SDK.
- **Crawling FAQ**: [docs.glean.com/connectors/crawling-faq](https://docs.glean.com/connectors/crawling-faq) — Common questions about data crawling.
- **Excluding Content**: [docs.glean.com/connectors/excluding-content](https://docs.glean.com/connectors/excluding-content) — Data rules for inclusion/exclusion.
- **Custom Connector Troubleshooting**: [docs.glean.com/connectors/custom/troubleshooting](https://docs.glean.com/connectors/custom/troubleshooting) — Debug crawl failures and webhook issues.

---

## 🛰️ Glean MCP & Actions

- **Configure Actions (MCP)**: [docs.glean.com/.../config-actions-mcp-from-datasource](https://docs.glean.com/connectors/configure-actions-in-datasource/config-actions-mcp-from-datasource) — Setting up read/write/execute actions.
- **Glean SDK (GitHub)**: [github.com/gleanwork](https://github.com/gleanwork) — Open-source tools and SDKs.
- **Model Context Protocol (MCP)**: [modelcontextprotocol.io](https://modelcontextprotocol.io/) — The standard for LLM-to-tool communication.
- **MCP Specification**: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io/) — Full protocol specification for tools and resources.

---

## 📡 Native Connector Guides (Key for Observability)

- **PagerDuty Connector**: [docs.glean.com/connectors/native/pagerduty/home](https://docs.glean.com/connectors/native/pagerduty/home) — Incident ingestion.
- **Slack Connector**: [docs.glean.com/connectors/native/slack/home](https://docs.glean.com/connectors/native/slack/home) — Channel history and war room context.
- **Slack Real-Time Search**: [docs.glean.com/connectors/native/slack-rts/home](https://docs.glean.com/connectors/native/slack-rts/home) — Live message search.
- **Jira Connector**: [docs.glean.com/connectors/native/jira/home](https://docs.glean.com/connectors/native/jira/home) — Issue tracking and project management.
- **Jira Data Center**: [docs.glean.com/connectors/native/jira-dc/home](https://docs.glean.com/connectors/native/jira-dc/home) — Self-hosted Jira integration.
- **GitHub Connector**: [docs.glean.com/connectors/native/github/home](https://docs.glean.com/connectors/native/github/home) — Code changes and PR history.
- **GitHub Enterprise**: [docs.glean.com/connectors/native/github-enterprise-server/home](https://docs.glean.com/connectors/native/github-enterprise-server/home) — On-prem GitHub server.
- **ServiceNow Connector**: [docs.glean.com/connectors/native/servicenow/home](https://docs.glean.com/connectors/native/servicenow/home) — Change management and CMDB.
- **Confluence Connector**: [docs.glean.com/connectors/native/confluence/home](https://docs.glean.com/connectors/native/confluence/home) — Runbook and documentation sync.
- **Azure DevOps Connector**: [docs.glean.com/connectors/native/azure-devops/home](https://docs.glean.com/connectors/native/azure-devops/home) — Pipeline and board integration.
- **Freshservice Connector**: [docs.glean.com/connectors/native/freshservice/home](https://docs.glean.com/connectors/native/freshservice/home) — IT service management.
- **Teams Connector**: [docs.glean.com/connectors/native/teams/home](https://docs.glean.com/connectors/native/teams/home) — Microsoft Teams chat ingestion.
- **Zoom Connector**: [docs.glean.com/connectors/native/zoom/home](https://docs.glean.com/connectors/native/zoom/home) — Meeting transcript search.

---

## 🔗 Glean API & Developer Documentation

- **Glean Admin API**: [developers.glean.com](https://developers.glean.com/) — REST APIs for managing data sources, users, and permissions.
- **Indexing API**: [developers.glean.com/indexing](https://developers.glean.com/docs/indexing_api/overview) — Push custom documents to Glean.
- **Client SDK (Python)**: [github.com/gleanwork/glean-python-sdk](https://github.com/gleanwork/api-client-python) — Programmatic access to Glean search and management.
- **Webhook Events**: [developers.glean.com/webhooks](https://developers.glean.com/docs/indexing_api/webhooks) — Real-time notifications on data changes.

---

## 🛡️ Security & Permissions

- **Group-Based Permissions**: [docs.glean.com/.../group-based-permissions](https://docs.glean.com/administration/identity/roles/group-based-permissions) — ACL inheritance from source systems.
- **Managing Visibility**: [docs.glean.com/.../hiding-content](https://docs.glean.com/administration/search/hiding-content#test-groups-for-data-sources) — Test groups and staged rollouts.
- **Manage Test Groups**: [app.glean.com/admin/setup/apps/testing](https://app.glean.com/admin/setup/apps/testing) — Configure test group membership.
- **Data Governance**: [docs.glean.com/administration/security](https://docs.glean.com/security) — Enterprise security and compliance overview.
- **SSO / SAML Setup**: [docs.glean.com/administration/identity](https://docs.glean.com/administration/identity) — Enterprise identity provider integration.

---

## 📚 Observability Foundations

- **Google SRE Book — Monitoring**: [sre.google/sre-book/monitoring-distributed-systems](https://sre.google/sre-book/monitoring-distributed-systems/) — The 4 golden signals.
- **Google SRE Book — Alerting on SLOs**: [sre.google/workbook/alerting-on-slos](https://sre.google/workbook/alerting-on-slos/) — Data-driven alerting.
- **OpenTelemetry**: [opentelemetry.io](https://opentelemetry.io/) — Vendor-neutral observability framework.
- **Prometheus**: [prometheus.io/docs](https://prometheus.io/docs/introduction/overview/) — Metrics collection and alerting.
- **Grafana**: [grafana.com/docs](https://grafana.com/docs/grafana/latest/) — Dashboarding and visualization.
- **ELK Stack**: [elastic.co/guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html) — Elasticsearch, Logstash, Kibana for log management.
- **Fluentd / Fluent Bit**: [fluentd.org](https://www.fluentd.org/) — Unified logging layer.
- **Alert Fatigue Research**: [PagerDuty Blog](https://www.pagerduty.com/blog/reduce-alert-fatigue/) — Why correlation matters.
- **Causal Inference for RCA**: [Microsoft DoWhy](https://microsoft.github.io/dowhy/) — Algorithmic root cause analysis.

---

## 🤖 AIOps & Intelligent Operations

- **Gartner AIOps Market Guide**: [gartner.com/en/information-technology/glossary/aiops](https://www.gartner.com/en/information-technology/glossary/aiops-artificial-intelligence-operations) — Industry definition and landscape.
- **Moogsoft AIOps**: [moogsoft.com](https://www.moogsoft.com/) — AI-powered noise reduction and correlation.
- **BigPanda**: [bigpanda.io](https://www.bigpanda.io/) — Event correlation and automation platform.
- **PagerDuty AIOps**: [pagerduty.com/features/aiops](https://www.pagerduty.com/features/ai-operations/) — Intelligent triage and grouping.
- **Datadog AIOps**: [datadoghq.com/product/watchdog](https://www.datadoghq.com/product/watchdog/) — Anomaly detection for metrics and logs.

---

## 🎥 Video Learning & Tutorials

- **Glean Product Demo**: [youtube.com/@Glean](https://www.youtube.com/channel/UCY0JDJWRBXrR0m1SqWPVB9A) — Official Glean YouTube channel.
- **SRE Observability (Google Cloud)**: [youtube.com/...](https://www.youtube.com/watch?v=xjO0ieFblw4) — Google SRE team on monitoring and alerting.
- **OpenTelemetry Deep Dive**: [youtube.com/...](https://www.youtube.com/watch?v=r8UvWSX3KA8) — CNCF conference talk on OTel fundamentals.
- **AIOps Explained (IBM)**: [youtube.com/...](https://www.youtube.com/watch?v=pyhGjNh_P7A) — IBM Technology on AIOps fundamentals.
- **PagerDuty University**: [university.pagerduty.com](https://www.pagerduty.com/university/) — Free incident management training.

---

## 🏗️ Dashboard & Visualization Tools

- **Grafana Dashboards**: [grafana.com/grafana/dashboards](https://grafana.com/grafana/dashboards/) — Pre-built dashboard templates.
- **Apache ECharts**: [echarts.apache.org](https://echarts.apache.org/en/index.html) — Rich charting library for custom dashboards.
- **Chart.js**: [chartjs.org](https://www.chartjs.org/) — Simple yet flexible JavaScript charting.
- **D3.js**: [d3js.org](https://d3js.org/) — Data-driven documents for advanced visualization.
- **Retool**: [retool.com](https://retool.com/) — Rapid internal tool building with API integrations.

---

## 🌐 Community & Ecosystem

- **Glean Community**: [glean.com/community](https://www.glean.com/community) — User forums and best practices.
- **Glean LinkedIn**: [linkedin.com/company/gleanwork](https://www.linkedin.com/company/gleanwork/about) — Industry updates and announcements.
- **Glean GitHub**: [github.com/gleanwork](https://github.com/gleanwork) — Open-source projects and SDKs.
- **CNCF Observability TAG**: [github.com/cncf/tag-observability](https://github.com/cncf/tag-observability) — Cloud-native observability standards.
- **SRE Weekly Newsletter**: [sreweekly.com](https://sreweekly.com/) — Curated SRE and reliability articles.
- **DevOps Subreddit**: [reddit.com/r/devops](https://www.reddit.com/r/devops/) — Community discussions on tooling and practices.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../project/README.md">Next: Project Guide ➡️</a>
</p>
