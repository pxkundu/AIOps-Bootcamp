#!/usr/bin/env bash
# ==============================================================================
# install_mcp_servers.sh
# 
# This script initializes the Node.js dependencies for the Top 10 MCP Servers 
# so they execute much faster when invoked by the MCP Host (e.g. Claude Desktop).
# ==============================================================================

set -e

echo "🚀 Starting global installation of MCP Community Servers..."

# Check requirements
command -v npm >/dev/null 2>&1 || { echo >&2 "❌ npm is required but not installed. Please install Node.js."; exit 1; }

# Install the primary packages globally to cache them
echo "📦 Installing File System MCP..."
npm install -g @modelcontextprotocol/server-filesystem

echo "📦 Installing GitHub MCP..."
npm install -g @modelcontextprotocol/server-github

echo "📦 Installing PostgreSQL MCP..."
npm install -g @modelcontextprotocol/server-postgres

echo "📦 Installing Slack MCP..."
npm install -g @modelcontextprotocol/server-slack

echo "📦 Installing Google Drive MCP..."
npm install -g @modelcontextprotocol/server-google-drive

echo "📦 Installing Jira MCP..."
npm install -g @modelcontextprotocol/server-jira

echo "📦 Installing Notion MCP..."
npm install -g @modelcontextprotocol/server-notion

echo "📦 Installing Linear MCP..."
npm install -g @modelcontextprotocol/server-linear

echo "📦 Installing Sentry MCP..."
npm install -g @modelcontextprotocol/server-sentry

echo "✅ All Javascript-based MCP Servers cached successfully."

echo "🐳 Reminder: The AWS MCP Server relies on Docker. Ensure Docker Desktop is running."
echo "🎉 Setup Complete! You can now paste your claude_desktop_master_config.json into your Host."
