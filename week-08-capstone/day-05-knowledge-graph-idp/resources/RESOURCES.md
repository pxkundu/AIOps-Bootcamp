# Resources: Knowledge Graph IDP on AWS

Official documentation, reference architectures, and learning materials.

---

## 🧠 Glean Knowledge Graph

- **Knowledge Graph Overview**: [docs.glean.com/security/knowledge-graph](https://docs.glean.com/security/knowledge-graph) — Core architecture, content integration, people intelligence, activity tracking, collective intelligence.
- **Shared Services**: [docs.glean.com/security/architecture/shared-centralized-services](https://docs.glean.com/security/architecture/shared-centralized-services) — Web delivery, tenant resolution, analytics.
- **Upgrade Model & SDLC**: [docs.glean.com/security/architecture/sdlc](https://docs.glean.com/security/architecture/sdlc) — Development lifecycle and security.
- **Glean Security Overview**: [docs.glean.com/security](https://docs.glean.com/security) — Enterprise security, compliance, and data governance.

---

## 🔌 Glean Connectors & Custom Data Sources

- **Connectors Hub**: [docs.glean.com/connectors/home](https://docs.glean.com/connectors/home) — Full catalog of 100+ native connectors.
- **Custom Data Sources**: [docs.glean.com/connectors/custom/about](https://docs.glean.com/connectors/custom/about) — Build your own connector with the Indexing API.
- **Glean REST APIs**: [docs.glean.com/connectors/custom/glean-apis](https://docs.glean.com/connectors/custom/glean-apis) — API reference for custom connectors.
- **Managing Connectors**: [docs.glean.com/connectors/monitoring](https://docs.glean.com/connectors/monitoring) — Sync status, metrics, and troubleshooting.
- **Excluding Content**: [docs.glean.com/connectors/excluding-content](https://docs.glean.com/connectors/excluding-content) — Inclusion/exclusion data rules.
- **Custom Connector Troubleshooting**: [docs.glean.com/connectors/custom/troubleshooting](https://docs.glean.com/connectors/custom/troubleshooting) — Debug crawl and webhook issues.

---

## 📡 Glean Developer Platform

- **Developer Documentation**: [developers.glean.com](https://developers.glean.com/) — REST APIs for indexing, search, and management.
- **Indexing API - Getting Started**: [developers.glean.com/indexing/getting-started](https://glean-developer-site.vercel.app/api-info/indexing/getting-started/setup-datasource) — Setup custom data sources.
- **Indexing API - Add/Update Datasource**: [developers.glean.com/api/indexing](https://developers.glean.com/api/indexing-api/add-or-update-datasource) — Datasource management endpoint.
- **Python SDK**: [github.com/gleanwork/api-client-python](https://github.com/gleanwork/api-client-python) — Python client for Glean APIs.
- **Developer Community**: [community.glean.com](https://community.glean.com/group/3-glean-developer-community) — Forums, examples, and support.

---

## 🔐 Glean Security & Identity

- **Group-Based Permissions**: [docs.glean.com/.../group-based-permissions](https://docs.glean.com/administration/identity/roles/group-based-permissions) — ACL inheritance from source systems.
- **Managing Visibility**: [docs.glean.com/.../hiding-content](https://docs.glean.com/administration/search/hiding-content#test-groups-for-data-sources) — Test groups and staged rollouts.
- **SSO / SAML Setup**: [docs.glean.com/administration/identity](https://docs.glean.com/administration/identity) — Enterprise identity provider integration.
- **MCP Actions (Agents)**: [docs.glean.com/.../config-actions-mcp](https://docs.glean.com/connectors/configure-actions-in-datasource/config-actions-mcp-from-datasource) — Read/write/execute actions.

---

## ☁️ AWS Services (for IDP Deployment)

- **ECS Fargate**: [docs.aws.amazon.com/ecs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html) — Serverless container orchestration.
- **Application Load Balancer**: [docs.aws.amazon.com/elasticloadbalancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) — Layer 7 load balancing.
- **RDS PostgreSQL**: [docs.aws.amazon.com/rds](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html) — Managed relational database.
- **Secrets Manager**: [docs.aws.amazon.com/secretsmanager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html) — Secure credential management.
- **CloudWatch**: [docs.aws.amazon.com/cloudwatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html) — Monitoring and log aggregation.
- **VPC**: [docs.aws.amazon.com/vpc](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) — Network isolation and security groups.
- **IAM Roles**: [docs.aws.amazon.com/iam](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) — Task-level permissions for ECS.

---

## 🏗️ IDP & Developer Portal Frameworks

- **Backstage (Spotify)**: [backstage.io](https://backstage.io/) — Leading open-source IDP framework.
- **Port**: [getport.io](https://www.getport.io/) — Developer portal platform.
- **Cortex**: [cortex.io](https://www.cortex.io/) — Engineering intelligence platform.
- **OpsLevel**: [opslevel.com](https://www.opslevel.com/) — Service ownership and maturity platform.

---

## 📚 Knowledge Graph & Search Foundations

- **Google Knowledge Graph**: [developers.google.com/knowledge-graph](https://developers.google.com/knowledge-graph) — Google's public KG API.
- **Neo4j Graph Database**: [neo4j.com](https://neo4j.com/) — Native graph database for knowledge graphs.
- **Elasticsearch**: [elastic.co/elasticsearch](https://www.elastic.co/elasticsearch) — Full-text search engine.
- **LinkedIn Knowledge Graph**: [engineering.linkedin.com/blog/2016/10/building-the-linkedin-knowledge-graph](https://engineering.linkedin.com/blog/2016/10/building-the-linkedin-knowledge-graph) — Enterprise KG case study.
- **Knowledge Graphs in Practice (O'Reilly)**: [oreilly.com](https://www.oreilly.com/library/view/knowledge-graphs/9781098127091/) — Book on building enterprise KGs.

---

## 🎥 Video & Learning

- **Glean YouTube**: [youtube.com/@Glean](https://www.youtube.com/channel/UCY0JDJWRBXrR0m1SqWPVB9A) — Product demos and integrations.
- **Backstage by Spotify**: [youtube.com/...](https://www.youtube.com/watch?v=85TQEpNCaU0) — KubeCon talk on building IDPs.
- **Knowledge Graphs Explained**: [youtube.com/...](https://www.youtube.com/watch?v=UOZVGFx8Oos) — IBM Technology explainer.
- **Internal Developer Portals (ThoughtWorks)**: [thoughtworks.com/radar](https://www.thoughtworks.com/radar/techniques/internal-developer-portals) — Tech Radar assessment.

---

## 🌐 Community

- **Glean Community**: [community.glean.com](https://community.glean.com/) — User forums and developer community.
- **Glean GitHub**: [github.com/gleanwork](https://github.com/gleanwork) — Open-source tools and SDKs.
- **Glean Support**: [support.glean.com](https://support.glean.com/hc/en-us/requests/new) — Enterprise support tickets.
- **CNCF Platforms WG**: [tag-app-delivery.cncf.io/wgs/platforms](https://tag-app-delivery.cncf.io/wgs/platforms/) — Cloud-native platform engineering.
- **Platform Engineering Community**: [platformengineering.org](https://platformengineering.org/) — IDP best practices and events.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../project/README.md">Next: Project Guide ➡️</a>
</p>
