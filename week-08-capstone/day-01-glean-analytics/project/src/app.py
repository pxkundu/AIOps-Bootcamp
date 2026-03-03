from flask import Flask, render_template_string
import pandas as pd
from glean_engine import GleanSecEngine
import os

app = Flask(__name__)

# Mock Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Home Page Template
HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glean-SEC: Enterprise Analytics Monitor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .badge-Critical { background-color: #dc3545; }
        .badge-High { background-color: #ffc107; color: #000; }
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 0; }
    </style>
</head>
<body>
    <div class="hero text-center">
        <h1>🔍 Glean-SEC Monitor</h1>
        <p>Enterprise Pipeline Sentry & Security Discovery</p>
    </div>
    
    <div class="container my-5">
        <div class="row text-center mb-4">
            <div class="col-md-4">
                <div class="card p-3">
                    <h3>{{ total_knowledge }}</h3>
                    <p class="text-muted">Knowledge Objects Indexed</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <h3 class="text-danger">{{ total_alerts }}</h3>
                    <p class="text-muted">Security Risks Detected</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-3">
                    <h3>3</h3>
                    <p class="text-muted">Active Connectors</p>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0">🚨 Active Security Risks (RCA Discovery)</h5>
            </div>
            <div class="card-body">
                <table class="table table-hover">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Risk Type</th>
                            <th>Risk Level</th>
                            <th>Source</th>
                            <th>Target Item</th>
                            <th>Details</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for alert in alerts %}
                        <tr>
                            <td><code>{{ alert.id }}</code></td>
                            <td>{{ alert.type }}</td>
                            <td><span class="badge badge-{{ alert.risk }} p-2">{{ alert.risk }}</span></td>
                            <td>{{ alert.source }}</td>
                            <td>{{ alert.item }}</td>
                            <td>{{ alert.details }}</td>
                            <td>{{ alert.time }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Run the Glean-SEC engine
    engine = GleanSecEngine(DATA_DIR)
    engine.load_data()
    engine.run_discovery()
    
    alerts = engine.security_alerts
    total_knowledge = len(engine.knowledge_base)
    total_alerts = len(alerts)
    
    return render_template_string(
        HOME_PAGE, 
        alerts=alerts, 
        total_knowledge=total_knowledge, 
        total_alerts=total_alerts
    )

if __name__ == "__main__":
    print("🚀 Glean-SEC Dashboard starting on http://localhost:5000")
    app.run(debug=True, port=5000)
