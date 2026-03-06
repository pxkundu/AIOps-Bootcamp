# Resources: IDP Platform — OpenWebUI, Terraform, AWS

Curated references for building and managing the Internal Developer Platform.

---

## 🔍 OpenWebUI

- **Official Docs**: [docs.openwebui.com](https://docs.openwebui.com/) — Installation, configuration, and admin guides.
- **GitHub Repository**: [open-webui/open-webui](https://github.com/open-webui/open-webui) — Source code and issues.
- **Docker Hub**: [ghcr.io/open-webui/open-webui](https://github.com/open-webui/open-webui/pkgs/container/open-webui) — Official container images.
- **Environment Variables**: [Configuration Reference](https://docs.openwebui.com/getting-started/env-configuration) — All supported env vars.

---

## ☁️ AWS Services

- **EC2 User Data**: [AWS Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html) — Bootstrap scripts on launch.
- **RDS PostgreSQL**: [AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html) — Managed database setup.
- **Amazon Bedrock**: [Developer Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) — Foundation model access.
- **IAM Roles for EC2**: [AWS Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) — Secure, keyless API access.
- **VPC Best Practices**: [AWS Architecture Center](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html) — Network isolation patterns.

---

## 🛠️ Terraform

- **Official Registry**: [registry.terraform.io](https://registry.terraform.io/) — Provider and module documentation.
- **AWS Provider**: [hashicorp/aws](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) — Full resource reference.
- **Best Practices**: [HashiCorp Learn](https://developer.hashicorp.com/terraform/tutorials) — State management, modules, workspaces.
- **terraform-aws-modules**: [GitHub](https://github.com/terraform-aws-modules) — Community VPC, EC2, RDS modules.

---

## 🐳 Docker & Containers

- **Docker Compose Reference**: [docs.docker.com](https://docs.docker.com/compose/compose-file/) — Service definitions, volumes, networks.
- **Docker on Ubuntu**: [Installation Guide](https://docs.docker.com/engine/install/ubuntu/) — Official steps.
- **Container Networking**: [Bridge Networks](https://docs.docker.com/network/bridge/) — Multi-container communication.

---

## 🧠 LLM Integration

- **OpenAI API Reference**: [platform.openai.com/docs](https://platform.openai.com/docs/api-reference) — GPT-4o endpoints.
- **LiteLLM Proxy**: [docs.litellm.ai](https://docs.litellm.ai/) — Unified proxy for 100+ LLM providers including Bedrock.
- **Bedrock Model Access**: [Request Model Access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) — Enabling Anthropic models.

---

## 🔐 Security & Production

- **Let's Encrypt with Nginx**: [Certbot Docs](https://certbot.eff.org/) — Free HTTPS certificates.
- **AWS CloudWatch Agent**: [Monitoring Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html) — EC2 metrics and logs.
- **RDS Encryption**: [AWS Docs](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html) — Data at rest encryption.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../project/README.md">Next: Project Guide ➡️</a>
</p>
