"""
Observability Hub Dashboard — Flask application that ties together
connectors, health monitoring, alert correlation, and MCP actions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template_string, jsonify
from connectors.connector_framework import create_all_connectors
from monitoring.health_monitor import ConnectorHealthMonitor
from alerting.alert_correlator import AlertCorrelator

app = Flask(__name__)

# --- Initialize the Pipeline ---
connectors = create_all_connectors()
monitor = ConnectorHealthMonitor()
correlator = AlertCorrelator(time_window_hours=4)

# Crawl all sources
for conn in connectors:
    conn.crawl()
    monitor.record_snapshot(conn.get_health())
    correlator.ingest_signals(conn.knowledge_objects)

# Run correlation
correlated = correlator.correlate()
dashboard_data = monitor.get_dashboard_data()


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Observability Hub — Glean Connector Monitor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #0f0f23; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
        .card { background: #1a1a3e; border: 1px solid #2a2a5e; }
        .card-header { background: #2a2a5e; }
        .badge-HEALTHY { background: #28a745; }
        .badge-WARNING { background: #ffc107; color: #000; }
        .badge-CRITICAL { background: #dc3545; }
        .hero { background: linear-gradient(135deg, #1a1a3e 0%, #0f0f23 50%, #1e3a5f 100%); padding: 30px 0; }
        .stat-card { text-align: center; padding: 20px; }
        .stat-card h2 { font-size: 2.5rem; font-weight: 700; }
        table { color: #e0e0e0; }
        .table-hover tbody tr:hover { background: #2a2a5e; }
        a { color: #7ecbff; }
    </style>
</head>
<body>
    <div class="hero text-center">
        <h1>🔭 Enterprise Observability Hub</h1>
        <p class="text-muted">Powered by Glean Connector Framework | {{ summary.total_connectors }} Active Connectors</p>
    </div>

    <div class="container my-4">
        <!-- Summary Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card stat-card">
                    <h2 class="text-info">{{ summary.total_items_indexed }}</h2>
                    <p>Knowledge Objects</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <h2 class="text-success">{{ summary.healthy }}</h2>
                    <p>Healthy Connectors</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <h2 class="text-warning">{{ summary.warning }}</h2>
                    <p>Warnings</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <h2 class="text-danger">{{ correlated_count }}</h2>
                    <p>Correlated Incidents</p>
                </div>
            </div>
        </div>

        <!-- Connector Health Table -->
        <div class="card mb-4">
            <div class="card-header"><h5 class="mb-0">📡 Connector Sync Status</h5></div>
            <div class="card-body">
                <table class="table table-hover">
                    <thead>
                        <tr><th>Connector</th><th>Status</th><th>Items Synced</th><th>Change Rate</th><th>Health</th></tr>
                    </thead>
                    <tbody>
                        {% for c in connectors_health %}
                        <tr>
                            <td><strong>{{ c.connector }}</strong></td>
                            <td>{{ c.status }}</td>
                            <td>{{ c.items_synced }}</td>
                            <td>{{ c.change_rate }} items/day</td>
                            <td><span class="badge badge-{{ c.health }} p-2">{{ c.health }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Correlated Incidents -->
        <div class="card mb-4">
            <div class="card-header"><h5 class="mb-0">🔗 Correlated Incidents (Cross-Source RCA)</h5></div>
            <div class="card-body">
                {% for inc in incidents %}
                <div class="card mb-3" style="border-left: 4px solid #dc3545;">
                    <div class="card-body">
                        <h6>{{ inc.id }} — Service: <code>{{ inc.service }}</code></h6>
                        <p><strong>Sources:</strong> {{ inc.sources_involved | join(', ') }}</p>
                        <p><strong>Signals:</strong> {{ inc.signal_count }} related signals</p>
                        <p><strong>🧠 RCA:</strong> {{ inc.suggested_rca }}</p>
                        <p><strong>📋 Actions:</strong></p>
                        <ul>
                            {% for action in inc.suggested_actions %}
                            <li>{{ action }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- MCP Actions -->
        <div class="card">
            <div class="card-header"><h5 class="mb-0">🛰️ MCP Action Server</h5></div>
            <div class="card-body">
                <p>The MCP Action Server is running on <code>http://localhost:5002</code>.</p>
                <p>Available tools: <a href="http://localhost:5002/mcp/v1/tools" target="_blank">View Tool Catalog →</a></p>
            </div>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        DASHBOARD_HTML,
        summary=dashboard_data["summary"],
        connectors_health=dashboard_data["connectors"],
        incidents=correlated,
        correlated_count=len(correlated),
    )


@app.route("/api/health")
def api_health():
    return jsonify(dashboard_data)


@app.route("/api/incidents")
def api_incidents():
    return jsonify(correlated)


if __name__ == "__main__":
    print("🔭 Observability Hub running at http://localhost:5003")
    app.run(debug=True, port=5003)
