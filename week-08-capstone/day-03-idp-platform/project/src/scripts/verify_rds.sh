#!/bin/bash
# --- RDS Health Check & Schema Verification ---
# Run this ON the EC2 instance to verify database connectivity.

set -e

echo "🔍 Verifying RDS PostgreSQL Connection..."

# These values come from Terraform outputs. Set them as environment variables.
DB_HOST="${DB_HOST:-your-rds-endpoint.amazonaws.com}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-openwebui}"
DB_USER="${DB_USER:-idpadmin}"

# 1. Check connectivity via pg_isready
if command -v pg_isready &> /dev/null; then
  pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
else
  echo "⚠️  pg_isready not found. Installing postgresql-client..."
  sudo apt-get install -y postgresql-client
  pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
fi

if [ $? -eq 0 ]; then
  echo "✅ RDS Connection: HEALTHY"
else
  echo "❌ RDS Connection: FAILED"
  echo "  Check: Security Group allows port 5432 from EC2?"
  echo "  Check: DB credentials in docker-compose.yml match Terraform outputs?"
  exit 1
fi

# 2. List OpenWebUI tables (after first run, it auto-migrates)
echo ""
echo "📋 Listing OpenWebUI Tables:"
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
  -c "\dt" 2>/dev/null || echo "  (Tables will appear after the first OpenWebUI startup)"

echo ""
echo "✅ Database verification complete."
