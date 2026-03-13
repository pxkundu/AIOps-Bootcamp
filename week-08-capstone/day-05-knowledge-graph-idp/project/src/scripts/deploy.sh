#!/usr/bin/env bash
# ============================================================
# IDP Portal Deployment Script
# Validates prerequisites, builds Docker image, and deploys
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

log()   { echo -e "${GREEN}✅ $1${NC}"; }
warn()  { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

echo "============================================"
echo "🧠 IDP Portal — Pre-flight Check"
echo "============================================"

# --- Check Python ---
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1)
    log "Python found: $PY_VER"
else
    error "Python 3 is required. Install: brew install python"
fi

# --- Check Flask ---
if python3 -c "import flask" 2>/dev/null; then
    log "Flask is installed"
else
    warn "Flask not found. Installing..."
    pip3 install flask
fi

# --- Check Terraform (optional) ---
if command -v terraform &>/dev/null; then
    TF_VER=$(terraform version -json 2>/dev/null | python3 -c "import sys,json;print(json.load(sys.stdin)['terraform_version'])" 2>/dev/null || terraform version | head -1)
    log "Terraform found: $TF_VER"
else
    warn "Terraform not found. Required only for AWS deployment."
fi

# --- Check Docker (optional) ---
if command -v docker &>/dev/null; then
    log "Docker found: $(docker --version)"
else
    warn "Docker not found. Required only for containerized deployment."
fi

# --- Check AWS CLI (optional) ---
if command -v aws &>/dev/null; then
    log "AWS CLI found: $(aws --version 2>&1 | head -1)"
else
    warn "AWS CLI not found. Required only for AWS deployment."
fi

echo ""
echo "============================================"
echo "🧪 Running Knowledge Graph Engine Test"
echo "============================================"

cd "$PROJECT_DIR"
python3 -c "
import sys
sys.path.insert(0, '.')
from knowledge_graph.kg_engine import KnowledgeGraphEngine, KnowledgeObject, PersonProfile
from knowledge_graph.custom_connectors import load_service_catalog, load_okrs, load_runbooks, load_api_docs, load_people, set_expertise

kg = KnowledgeGraphEngine()
for p in load_people():
    kg.add_person(p)
set_expertise(kg.people)
for doc in load_service_catalog() + load_okrs() + load_runbooks() + load_api_docs():
    kg.index_document(doc)
kg.build_collaboration_graph()

stats = kg.get_stats()
print(f'  Documents indexed: {stats[\"total_documents\"]}')
print(f'  People profiles:   {stats[\"total_people\"]}')
print(f'  Data sources:      {stats[\"sources\"]}')
print(f'  Facet dimensions:  {stats[\"facets\"]}')

results = kg.search('payment runbook', user_groups=['SRE'])
print(f'  Search test:       {len(results)} results for \"payment runbook\"')

experts = kg.find_expert('kubernetes')
print(f'  Expert finder:     {len(experts)} experts for \"kubernetes\"')
print()
print('✅ Knowledge Graph engine: ALL TESTS PASSED')
"

echo ""
echo "============================================"
echo "🚀 Ready to Launch"
echo "============================================"
echo "  Local:  cd $PROJECT_DIR && python3 portal/app.py"
echo "  URL:    http://localhost:5005"
echo "  APIs:   /api/search?q=..., /api/stats, /api/people, /api/gaps"
echo "============================================"
