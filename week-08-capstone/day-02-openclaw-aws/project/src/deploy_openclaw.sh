#!/bin/bash
# --- 🛡️ OpenClaw-Bedrock Health & Connectivity Utility ---
# This script verifies that your Lightsail Blueprint is correctly configured.

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔍 Starting OpenClaw-Bedrock Verification...${NC}"

# 1. Check OpenClaw Service Health
echo -e "⚙️ Checking OpenClaw Gateway Service..."
if systemctl is-active --quiet openclaw; then
    echo -e "  [${GREEN}OK${NC}] OpenClaw service is running."
else
    echo -e "  [${RED}FAIL${NC}] OpenClaw service is NOT running. Run 'sudo systemctl start openclaw'."
fi

# 2. Verify Node.js Environment
echo -e "🟢 Checking Node.js Environment..."
NODE_VER=$(node -v)
echo -e "  Current Version: $NODE_VER (Minimum v22 required)"

# 3. Bedrock API Access Test (Check if IAM Role is attached)
echo -e "🧠 Testing Amazon Bedrock Permissions..."
# This command checks if the instance can describe bedrock models
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[?modelId==`anthropic.claude-3-5-sonnet-20240620-v1:0`]' --output text > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "  [${GREEN}OK${NC}] Amazon Bedrock API is accessible."
else
    echo -e "  [${YELLOW}WARN${NC}] Bedrock Access Denied. Have you run the IAM script from the Getting Started tab?"
fi

# 4. Local Connectivity
echo -e "🏠 Checking Localhost Bind (Port 3000)..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "  [${GREEN}OK${NC}] Gateway is listening on port 3000."
else
    echo -e "  [${RED}FAIL${NC}] Gateway not found on port 3000."
fi

echo -e "\n${GREEN}✅ Verification Complete.${NC}"
echo -e "👉 If everything is OK, open http://localhost:3000 (via SSH Tunnel) to start your AIOps work."
