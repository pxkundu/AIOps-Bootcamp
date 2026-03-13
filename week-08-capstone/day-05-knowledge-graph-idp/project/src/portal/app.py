"""
IDP Portal — Flask-based Internal Developer Portal powered by the Knowledge Graph.
Provides: Search, People Directory, Service Catalog, OKR Dashboard, and Knowledge Gaps.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, render_template_string, jsonify
from knowledge_graph.kg_engine import KnowledgeGraphEngine
from knowledge_graph.custom_connectors import (
    load_service_catalog, load_okrs, load_runbooks, load_api_docs,
    load_people, set_expertise
)

app = Flask(__name__)

# --- Bootstrap Knowledge Graph ---
kg = KnowledgeGraphEngine()

# Load people
for person in load_people():
    kg.add_person(person)
set_expertise(kg.people)

# Load all content
for doc in load_service_catalog() + load_okrs() + load_runbooks() + load_api_docs():
    kg.index_document(doc)

# Build collaboration graph
kg.build_collaboration_graph()

# Simulate activity
kg.record_view("RB-001", "dave")
kg.record_view("RB-001", "charlie")
kg.record_view("SVC-001", "eve")
kg.search("payment runbook", user_groups=["SRE"])
kg.search("kubernetes troubleshooting", user_groups=["SRE"])
kg.search("quarterly budget report", user_groups=["Executives"])

PORTAL_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise IDP — Knowledge Graph Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0d1a; --card: #12162e; --border: #1e2548;
            --text: #e0e4f0; --muted: #8890b5; --accent: #6366f1;
            --green: #34d399; --yellow: #fbbf24; --red: #f87171; --blue: #60a5fa;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); }

        .nav { background:linear-gradient(90deg,#1e1b4b,#312e81); padding:16px 32px; display:flex; justify-content:space-between; align-items:center; }
        .nav h1 { font-size:1.3rem; }
        .nav .links a { color:var(--muted); text-decoration:none; margin-left:24px; font-size:0.85rem; }
        .nav .links a:hover { color:var(--text); }

        .hero { text-align:center; padding:48px 20px 24px; }
        .hero h2 { font-size:2rem; font-weight:700; margin-bottom:12px; }
        .hero p { color:var(--muted); max-width:600px; margin:0 auto 24px; }

        .search-box { max-width:680px; margin:0 auto; display:flex; gap:8px; }
        .search-box input { flex:1; padding:14px 20px; border-radius:10px; border:1px solid var(--border); background:var(--card); color:var(--text); font-size:1rem; outline:none; }
        .search-box input:focus { border-color:var(--accent); }
        .search-box button { padding:14px 28px; border-radius:10px; border:none; background:var(--accent); color:#fff; font-weight:600; cursor:pointer; }

        .container { max-width:1200px; margin:32px auto; padding:0 20px; }
        .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-bottom:32px; }

        .card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; transition:transform 0.2s; }
        .card:hover { transform:translateY(-2px); }
        .card h3 { font-size:1rem; margin-bottom:8px; }
        .card p { font-size:0.85rem; color:var(--muted); line-height:1.5; }
        .tag { display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.7rem; font-weight:600; margin:4px 4px 0 0; }
        .tag-sre { background:rgba(99,102,241,0.2); color:var(--accent); }
        .tag-service { background:rgba(52,211,153,0.2); color:var(--green); }
        .tag-okr { background:rgba(251,191,36,0.2); color:var(--yellow); }
        .tag-runbook { background:rgba(248,113,113,0.2); color:var(--red); }
        .tag-api { background:rgba(96,165,250,0.2); color:var(--blue); }

        .section-title { font-size:1.1rem; font-weight:600; margin-bottom:16px; padding-bottom:8px; border-bottom:1px solid var(--border); }

        .stat-row { display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:32px; }
        .stat { background:var(--card); border:1px solid var(--border); border-radius:10px; padding:20px; text-align:center; }
        .stat .val { font-size:2rem; font-weight:700; }
        .stat .lbl { font-size:0.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-top:4px; }

        .person { display:flex; align-items:center; gap:12px; padding:12px 16px; background:var(--card); border:1px solid var(--border); border-radius:10px; }
        .avatar { width:40px; height:40px; border-radius:50%; background:var(--accent); display:flex; align-items:center; justify-content:center; font-weight:700; font-size:1rem; }
        .person-info h4 { font-size:0.9rem; } .person-info p { font-size:0.75rem; color:var(--muted); }

        #results { margin-top:24px; }

        @media(max-width:768px) { .stat-row { grid-template-columns:repeat(2,1fr); } }
    </style>
</head>
<body>
    <div class="nav">
        <h1>🧠 Enterprise IDP</h1>
        <div class="links">
            <a href="/">Home</a>
            <a href="/api/stats">Stats API</a>
            <a href="/api/people">People API</a>
            <a href="/api/gaps">Knowledge Gaps</a>
        </div>
    </div>

    <div class="hero">
        <h2>Your Company's Intelligence Layer</h2>
        <p>Search across services, runbooks, OKRs, APIs, and people — all in one place.</p>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search: 'payment runbook', 'kubernetes expert', 'Q1 OKR'..." />
            <button onclick="doSearch()">Search</button>
        </div>
    </div>

    <div class="container">
        <!-- Stats -->
        <div class="stat-row">
            <div class="stat"><div class="val" style="color:var(--accent)">{{ stats.total_documents }}</div><div class="lbl">Knowledge Objects</div></div>
            <div class="stat"><div class="val" style="color:var(--green)">{{ stats.total_people }}</div><div class="lbl">People Profiles</div></div>
            <div class="stat"><div class="val" style="color:var(--blue)">{{ stats.total_searches }}</div><div class="lbl">Searches</div></div>
            <div class="stat"><div class="val" style="color:var(--yellow)">{{ stats.facets }}</div><div class="lbl">Facet Dimensions</div></div>
            <div class="stat"><div class="val" style="color:var(--red)">{{ stats.knowledge_gaps }}</div><div class="lbl">Knowledge Gaps</div></div>
        </div>

        <div id="results"></div>

        <!-- Service Catalog -->
        <h3 class="section-title">📦 Service Catalog</h3>
        <div class="grid">
            {% for svc in services %}
            <div class="card">
                <h3>{{ svc.title }}</h3>
                <p>{{ svc.content[:120] }}...</p>
                <div style="margin-top:8px;">
                    <span class="tag tag-service">{{ svc.metadata.tier }}</span>
                    <span class="tag tag-api">{{ svc.metadata.language }}</span>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- People Directory -->
        <h3 class="section-title">👥 People Directory</h3>
        <div class="grid">
            {% for p in people %}
            <div class="person">
                <div class="avatar">{{ p.name[0] }}</div>
                <div class="person-info">
                    <h4>{{ p.name }}</h4>
                    <p>{{ p.role }} · {{ p.team }}</p>
                    <p>Expertise: {{ p.expertise | join(', ') }}</p>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- OKRs -->
        <h3 class="section-title">🎯 Engineering OKRs</h3>
        <div class="grid">
            {% for okr in okrs %}
            <div class="card">
                <h3>{{ okr.title }}</h3>
                <p>{{ okr.content[:150] }}...</p>
                <div style="margin-top:8px;">
                    <span class="tag tag-okr">{{ okr.metadata.status }}</span>
                    <span class="tag tag-sre">{{ okr.metadata.team }}</span>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
    async function doSearch() {
        const q = document.getElementById('searchInput').value;
        if (!q) return;
        const res = await fetch('/api/search?q=' + encodeURIComponent(q));
        const data = await res.json();
        const container = document.getElementById('results');
        if (data.length === 0) {
            container.innerHTML = '<div class="card" style="border-left:3px solid var(--red);"><h3>No results found</h3><p>This query has been logged as a knowledge gap.</p></div>';
            return;
        }
        let html = '<h3 class="section-title">🔍 Search Results for "' + q + '"</h3><div class="grid">';
        data.forEach(r => {
            const d = r.document;
            const typeClass = {'runbook':'tag-runbook','service':'tag-service','okr':'tag-okr','api-doc':'tag-api'}[d.doc_type] || 'tag-sre';
            html += '<div class="card"><h3>' + d.title + '</h3><p>' + d.content.substring(0,140) + '...</p>';
            html += '<div style="margin-top:8px;"><span class="tag ' + typeClass + '">' + d.doc_type + '</span>';
            html += '<span class="tag tag-sre">' + d.source + '</span>';
            html += '<span class="tag" style="background:rgba(255,255,255,0.05);color:var(--muted);">Score: ' + r.score + '</span></div></div>';
        });
        html += '</div>';
        container.innerHTML = html;
    }
    document.getElementById('searchInput').addEventListener('keydown', e => { if(e.key==='Enter') doSearch(); });
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    stats = kg.get_stats()
    services = [d.to_dict() for d in kg.documents.values() if d.doc_type == "service"]
    people = [p.to_dict() for p in kg.people.values()]
    okrs = [d.to_dict() for d in kg.documents.values() if d.doc_type == "okr"]
    return render_template_string(PORTAL_HTML, stats=stats, services=services, people=people, okrs=okrs)


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "")
    groups = request.args.get("groups", "SRE,Developer,Platform,Data,DevEx,Executives,Public").split(",")
    results = kg.search(query, user_groups=groups)
    return jsonify(results)


@app.route("/api/stats")
def api_stats():
    return jsonify(kg.get_stats())


@app.route("/api/people")
def api_people():
    return jsonify([p.to_dict() for p in kg.people.values()])


@app.route("/api/expert/<topic>")
def api_expert(topic):
    return jsonify(kg.find_expert(topic))


@app.route("/api/gaps")
def api_gaps():
    return jsonify(kg.get_knowledge_gaps())


@app.route("/api/trending")
def api_trending():
    return jsonify(kg.compute_trending())


@app.route("/api/facets")
def api_facets():
    return jsonify(kg.get_facets())


if __name__ == "__main__":
    print("🧠 IDP Portal running at http://localhost:5005")
    print("📡 APIs: /api/search?q=..., /api/stats, /api/people, /api/expert/<topic>, /api/gaps, /api/trending, /api/facets")
    app.run(debug=True, port=5005)
