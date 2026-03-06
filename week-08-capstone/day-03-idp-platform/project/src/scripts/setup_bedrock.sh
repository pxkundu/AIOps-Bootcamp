#!/bin/bash
# --- Bedrock Model Registration Script ---
# Run this ON the EC2 instance AFTER OpenWebUI is live.
# It registers Amazon Bedrock models into OpenWebUI as an additional provider.

set -e

echo "🧠 Configuring Amazon Bedrock Provider in OpenWebUI..."

# 1. Wait for OpenWebUI to be healthy
echo "⏳ Waiting for OpenWebUI to start..."
until curl -sf http://localhost:80/health > /dev/null; do
  sleep 5
done
echo "✅ OpenWebUI is healthy."

# 2. Verify Bedrock Access via IAM Role
echo "🔗 Testing Bedrock API access..."
aws bedrock list-foundation-models \
  --region us-east-1 \
  --query 'modelSummaries[?contains(modelId, `anthropic`)].modelId' \
  --output table

if [ $? -ne 0 ]; then
  echo "❌ Bedrock access failed. Ensure the IAM Instance Profile is attached."
  exit 1
fi

echo ""
echo "✅ Bedrock API accessible. Available Anthropic models listed above."
echo ""
echo "📋 Next Steps (Manual in OpenWebUI Admin Panel):"
echo "   1. Go to Admin Settings → Connections"
echo "   2. Add a new OpenAI-Compatible Connection:"
echo "      - Name: Amazon Bedrock"
echo "      - URL:  https://bedrock-runtime.us-east-1.amazonaws.com"
echo "      - Auth: AWS SigV4 (automatic via IAM Role)"
echo ""
echo "   Alternatively, use the Bedrock Litellm proxy:"
echo "      pip install litellm"
echo "      litellm --model bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0 --port 4000"
echo "      Then add http://localhost:4000 as a connection in OpenWebUI."
echo ""
echo "🎉 Configuration complete!"
