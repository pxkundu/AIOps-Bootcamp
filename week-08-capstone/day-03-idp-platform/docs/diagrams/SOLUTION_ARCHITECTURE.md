# Solution Architecture: IDP Platform (OpenWebUI + AWS)

Detailed architectural diagrams for the Internal Developer Platform capstone project.

---

## 🏗️ 1. Full Infrastructure Topology

```mermaid
graph TD
    subgraph "Internet"
        USER["Developer Browser"]
        OPENAI["OpenAI API"]
    end

    subgraph "AWS Account"
        subgraph "VPC: 10.0.0.0/16"
            subgraph "Public Subnet: 10.0.1.0/24"
                IGW["Internet Gateway"]
                EC2["EC2 t3.large"]
                EIP["Elastic IP"]
            end
            subgraph "Private Subnet A: 10.0.10.0/24"
                RDS_A["RDS Primary"]
            end
            subgraph "Private Subnet B: 10.0.11.0/24"
                RDS_B["RDS Standby (Multi-AZ)"]
            end
        end
        IAM["IAM Instance Profile"]
        BEDROCK["Amazon Bedrock"]
        CW["CloudWatch Logs"]
    end

    USER -- "HTTPS :443" --> EIP --> EC2
    EC2 -- "API Key" --> OPENAI
    EC2 -- "IAM Role" --> BEDROCK
    EC2 -- "Port 5432" --> RDS_A
    RDS_A -. "Sync Replication" .-> RDS_B
    EC2 -- "Agent" --> CW
    IGW --> EC2
    IAM -. "Attached to" .-> EC2
```

---

## ⚡ 2. Container Architecture on EC2

```mermaid
graph LR
    subgraph "EC2 Host (Docker Engine)"
        subgraph "Docker Network: idp-net"
            OWUI["openwebui:latest<br/>Port 3000 → 80"]
            NGINX["nginx:alpine<br/>Port 443 → 3000"]
        end
    end

    subgraph "External"
        RDS["RDS PostgreSQL<br/>Port 5432"]
        S3["S3 Bucket<br/>(Model Artifacts)"]
    end

    NGINX -- "Reverse Proxy" --> OWUI
    OWUI -- "DATABASE_URL" --> RDS
    OWUI -- "Bedrock SDK" --> S3
```

---

## 🔐 3. Terraform Module Dependency Graph

```mermaid
graph TD
    VPC["module: vpc"] --> SG["module: security_groups"]
    VPC --> SUB_PUB["Public Subnet"]
    VPC --> SUB_PRIV["Private Subnets (x2)"]
    SG --> EC2["module: ec2_instance"]
    SG --> RDS["module: rds_postgres"]
    SUB_PUB --> EC2
    SUB_PRIV --> RDS
    EC2 --> IAM["module: iam_role"]
    IAM --> BEDROCK["Bedrock Access Policy"]
    EC2 --> USERDATA["user_data.sh"]
    USERDATA --> DOCKER["Docker Compose Up"]
```

---

## 🔄 4. End-to-End Request Flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant NGINX as Nginx (443)
    participant OWUI as OpenWebUI (3000)
    participant DB as RDS PostgreSQL
    participant LLM as LLM Provider

    Dev->>NGINX: POST /api/chat (HTTPS)
    NGINX->>OWUI: Forward Request
    OWUI->>DB: Load User Session + History
    DB-->>OWUI: Session Context
    
    alt Provider = OpenAI
        OWUI->>LLM: OpenAI API (API Key)
    else Provider = Bedrock
        OWUI->>LLM: Bedrock InvokeModel (IAM SigV4)
    end
    
    LLM-->>OWUI: Streamed Response
    OWUI->>DB: Save Chat to History
    OWUI-->>NGINX: SSE Stream
    NGINX-->>Dev: Render in Browser
```

---

## 📋 5. Security Posture Summary

| Layer | Control | Implementation |
|-------|---------|----------------|
| **Network** | VPC Isolation | RDS in private subnet, no public IP |
| **Compute** | Security Group | Only ports 22, 80, 443 open on EC2 |
| **Database** | Network ACL | Port 5432 allowed only from EC2 SG |
| **Identity** | IAM Role | Instance Profile with scoped Bedrock policy |
| **Data** | Encryption at Rest | RDS with KMS encryption enabled |
| **Transport** | TLS | Nginx terminates HTTPS with Let's Encrypt or self-signed cert |
| **Application** | Auth | OpenWebUI built-in user authentication |

---

<p align="center">
  <a href="../../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../../project/README.md">Next: Project Guide ➡️</a>
</p>
