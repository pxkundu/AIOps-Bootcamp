# Project Guide: IDP Platform — Step-by-Step Deployment

This is the complete walkthrough for deploying the Internal Developer Platform from scratch.

---

## 📋 Prerequisites

| Requirement | How to Get It |
|-------------|---------------|
| **AWS Account** | [Create Free Tier Account](https://aws.amazon.com/free/) |
| **Terraform** (>= 1.5) | `brew install terraform` (macOS) |
| **AWS CLI** (v2) | `brew install awscli` (macOS) |
| **OpenAI API Key** | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| **SSH Key Pair** | Created via AWS Console or `ssh-keygen` |

---

## 🏗️ Phase 1: Local Testing (Optional but Recommended)

Before spending on AWS, test the full stack locally:

```bash
cd project/src/docker
export OPENAI_API_KEY="sk-your-key-here"
docker compose -f docker-compose.local.yml up -d
```

Open `http://localhost:3000` — you should see the OpenWebUI login screen.

---

## ☁️ Phase 2: Terraform — Provision AWS Infrastructure

### Step 2.1: Configure AWS Credentials
```bash
aws configure
# Enter: Access Key ID, Secret Key, Region (us-east-1), Output (json)
```

### Step 2.2: Create an SSH Key Pair
```bash
aws ec2 create-key-pair \
  --key-name aiops-idp-key \
  --query 'KeyMaterial' \
  --output text > aiops-idp-key.pem
chmod 400 aiops-idp-key.pem
```

### Step 2.3: Initialize Terraform
```bash
cd project/src/terraform
cp terraform.tfvars.sample terraform.tfvars
# Edit terraform.tfvars with your values (API keys, passwords, IP)
terraform init
```

### Step 2.4: Plan & Review
```bash
terraform plan
```
Review the plan. You should see:
- 1 VPC
- 3 Subnets (1 public, 2 private)
- 2 Security Groups
- 1 IAM Role + Instance Profile
- 1 RDS Instance
- 1 EC2 Instance
- 1 Elastic IP

### Step 2.5: Deploy!
```bash
terraform apply -auto-approve
```

Wait ~8-10 minutes. Terraform will output:
```
ec2_public_ip   = "54.XX.XX.XX"
rds_endpoint    = "aiops-idp-db.xxxxx.us-east-1.rds.amazonaws.com:5432"
openwebui_url   = "http://54.XX.XX.XX"
ssh_command     = "ssh -i aiops-idp-key.pem ubuntu@54.XX.XX.XX"
```

---

## 🐳 Phase 3: Verify the Application

### Step 3.1: SSH into the Instance
```bash
ssh -i aiops-idp-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### Step 3.2: Check Bootstrap Logs
```bash
sudo tail -f /var/log/idp-bootstrap.log
# Wait until you see "IDP Platform Bootstrap Complete!"
```

### Step 3.3: Verify Docker Containers
```bash
docker ps
# You should see the openwebui container in "Up" status
```

### Step 3.4: Verify RDS Connectivity
```bash
chmod +x /opt/idp-platform/verify_rds.sh
export DB_HOST="<rds_endpoint_from_terraform>"
export DB_USER="idpadmin"
export DB_PASSWORD="<your_password>"
export DB_NAME="openwebui"
./verify_rds.sh
```

---

## 🧠 Phase 4: Configure LLM Providers

### Step 4.1: Access OpenWebUI
Open `http://<EC2_PUBLIC_IP>` in your browser.
- **First User** = Automatic Admin.
- Create your admin account.

### Step 4.2: Verify OpenAI (Already Connected)
OpenAI is pre-configured via the `OPENAI_API_KEY` environment variable.
- Go to **Settings → Models** → You should see GPT-4o listed.
- Test with: *"What is AIOps?"*

### Step 4.3: Add Amazon Bedrock
SSH into the EC2 instance and run:
```bash
chmod +x /opt/idp-platform/setup_bedrock.sh
./setup_bedrock.sh
```
Follow the output instructions to add Bedrock as a provider in the Admin Panel.

**Option A (Recommended): LiteLLM Proxy**
```bash
pip install litellm
litellm --model bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0 --port 4000 &
```
Then in OpenWebUI Admin → Connections → Add: `http://localhost:4000`

**Option B: Direct API**
Add `https://bedrock-runtime.us-east-1.amazonaws.com` as an OpenAI-compatible endpoint.

---

## 🛡️ Phase 5: Harden for Production

| Action | Command |
|--------|---------|
| Enable HTTPS | Use `certbot` with Nginx reverse proxy |
| Restrict Signup | Set `ENABLE_SIGNUP=false` in docker-compose |
| Backup RDS | Enable automated snapshots in RDS console |
| Monitor | Install CloudWatch agent on EC2 |

---

## 🧹 Phase 6: Teardown (When Done)

```bash
cd project/src/terraform
terraform destroy -auto-approve
```

---

## 📂 File Map

| File | Purpose |
|------|---------|
| `terraform/main.tf` | Core infrastructure (VPC, EC2, RDS, IAM) |
| `terraform/variables.tf` | Input variable definitions |
| `terraform/outputs.tf` | Key outputs (IPs, URLs) |
| `terraform/terraform.tfvars.sample` | Sample values template |
| `scripts/user_data.sh` | EC2 bootstrap automation |
| `scripts/setup_bedrock.sh` | Bedrock provider configuration |
| `scripts/verify_rds.sh` | Database connectivity check |
| `docker/docker-compose.local.yml` | Local development stack |

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../resources/RESOURCES.md">Next: Resources ➡️</a>
</p>
