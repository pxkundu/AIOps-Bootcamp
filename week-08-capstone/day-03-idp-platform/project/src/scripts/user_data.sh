#!/bin/bash
# --- EC2 User Data: Automated IDP Platform Bootstrap ---
# This script runs ONCE on first boot of the EC2 instance.
# It installs Docker, pulls OpenWebUI, and configures the RDS connection.

set -e

LOG_FILE="/var/log/idp-bootstrap.log"
exec >> $LOG_FILE 2>&1

echo "⏳ [$(date)] Starting IDP Platform Bootstrap..."

# ============================================================
# 1. SYSTEM UPDATE & ESSENTIALS
# ============================================================
apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release jq

# ============================================================
# 2. INSTALL DOCKER ENGINE
# ============================================================
echo "🐳 Installing Docker Engine..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$${VERSION_CODENAME}") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

# ============================================================
# 3. INSTALL AWS CLI (for Bedrock interaction)
# ============================================================
echo "☁️ Installing AWS CLI v2..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
cd /tmp && unzip -q awscliv2.zip && ./aws/install
cd /home/ubuntu

# ============================================================
# 4. CREATE APPLICATION DIRECTORY
# ============================================================
APP_DIR="/opt/idp-platform"
mkdir -p $APP_DIR
cd $APP_DIR

# ============================================================
# 5. GENERATE DOCKER COMPOSE
# ============================================================
echo "📝 Generating docker-compose.yml..."
cat > docker-compose.yml <<EOF
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: openwebui
    restart: always
    ports:
      - "80:8080"
    environment:
      - DATABASE_URL=postgresql://${db_user}:${db_password}@${db_host}:${db_port}/${db_name}
      - OPENAI_API_KEY=${openai_api_key}
      - OPENAI_API_BASE_URLS=https://api.openai.com/v1
      - WEBUI_SECRET_KEY=$(openssl rand -hex 32)
      - ENABLE_SIGNUP=true
    volumes:
      - openwebui-data:/app/backend/data

volumes:
  openwebui-data:
EOF

# ============================================================
# 6. LAUNCH THE PLATFORM
# ============================================================
echo "🚀 Launching OpenWebUI..."
docker compose up -d

echo "✅ [$(date)] IDP Platform Bootstrap Complete!"
echo "🌐 Access the platform at http://$(curl -s ifconfig.me)"
