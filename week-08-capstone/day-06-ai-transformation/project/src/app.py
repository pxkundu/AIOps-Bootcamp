"""
AI Transformation Platform — Web Portal
Flask application providing the assessment dashboard, agent results,
and ROI visualization based on the AI Transformation 100 framework.
"""

import sys
import os
import json
from flask import Flask, render_template_string, request, jsonify

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from platform.assessment_engine import TransformationAssessor, PILLARS, MATURITY_LEVELS
from agents.transformation_agents import AgentOrchestrator

app = Flask(__name__)
assessor = TransformationAssessor()
orchestrator = AgentOrchestrator()

# Cache results on startup
demo_assessment = assessor.get_demo_assessment()
agent_results = orchestrator.run_all()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Transformation Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 50%, #0d0d2b 100%);
            color: #e0e0e0; min-height: 100vh;
        }
        .header {
            background: rgba(108, 92, 231, 0.15);
            border-bottom: 1px solid rgba(108, 92, 231, 0.3);
            padding: 20px 40px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .header h1 { font-size: 1.5rem; font-weight: 700; color: #a29bfe; }
        .header .source { font-size: 0.8rem; color: #888; }
        .header .source a { color: #6c5ce7; text-decoration: none; }
        .container { max-width: 1400px; margin: 0 auto; padding: 30px 40px; }

        /* Stats Bar */
        .stats-bar {
            display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; padding: 20px; text-align: center;
            transition: all 0.3s ease;
        }
        .stat-card:hover { border-color: #6c5ce7; transform: translateY(-2px); }
        .stat-card .value { font-size: 2rem; font-weight: 700; color: #6c5ce7; }
        .stat-card .label { font-size: 0.8rem; color: #888; margin-top: 4px; }

        /* Section */
        .section { margin-bottom: 30px; }
        .section-title {
            font-size: 1.2rem; font-weight: 600; color: #a29bfe;
            margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
        }

        /* Grid Layout */
        .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 30px; }

        /* Pillar Cards */
        .pillar-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
        .pillar-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px; padding: 16px;
            transition: all 0.3s ease;
        }
        .pillar-card:hover { border-color: #6c5ce7; }
        .pillar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .pillar-name { font-weight: 600; font-size: 0.9rem; }
        .pillar-score { font-weight: 700; color: #6c5ce7; }
        .pillar-bar-bg { background: rgba(255,255,255,0.08); border-radius: 4px; height: 6px; }
        .pillar-bar {
            height: 6px; border-radius: 4px;
            transition: width 1s ease;
        }
        .pillar-level { font-size: 0.75rem; color: #888; margin-top: 4px; }

        /* Recommendations */
        .rec-list { max-height: 400px; overflow-y: auto; }
        .rec-item {
            background: rgba(255,255,255,0.03);
            border-left: 3px solid #6c5ce7;
            padding: 12px 16px; margin-bottom: 8px;
            border-radius: 0 8px 8px 0;
            font-size: 0.85rem;
        }
        .rec-pillar { font-size: 0.7rem; color: #6c5ce7; font-weight: 600; text-transform: uppercase; }

        /* Agent Results */
        .agent-panel {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px; padding: 20px; margin-bottom: 16px;
        }
        .agent-panel h3 { color: #a29bfe; margin-bottom: 12px; font-size: 1rem; }
        .agent-stat { display: flex; justify-content: space-between; padding: 6px 0;
                       border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; }
        .agent-stat:last-child { border-bottom: none; }
        .agent-stat .val { color: #6c5ce7; font-weight: 600; }
        .target-item {
            background: rgba(231, 76, 60, 0.1); border: 1px solid rgba(231, 76, 60, 0.2);
            border-radius: 8px; padding: 10px 14px; margin: 6px 0; font-size: 0.8rem;
        }
        .target-item .score { color: #e74c3c; font-weight: 600; }
        .champion-item {
            background: rgba(46, 204, 113, 0.1); border: 1px solid rgba(46, 204, 113, 0.2);
            border-radius: 8px; padding: 10px 14px; margin: 6px 0; font-size: 0.8rem;
        }
        .champion-item .score { color: #2ecc71; font-weight: 600; }

        /* Footer */
        .footer {
            text-align: center; padding: 30px;
            color: #555; font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05);
        }
        .footer a { color: #6c5ce7; text-decoration: none; }

        @media (max-width: 900px) {
            .stats-bar { grid-template-columns: repeat(2, 1fr); }
            .two-col, .pillar-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 AI Transformation Platform</h1>
        <div class="source">
            Based on <a href="https://www.glean.com/work-ai-institute/ai-transformation-100" target="_blank">
            Glean Work AI Institute — AI Transformation 100</a>
        </div>
    </div>

    <div class="container">
        <!-- Stats Bar -->
        <div class="stats-bar">
            <div class="stat-card">
                <div class="value">{{ assessment.overall_score }}/5</div>
                <div class="label">Overall Maturity</div>
            </div>
            <div class="stat-card">
                <div class="value">{{ sludge.total_sludge_hours_per_week }}</div>
                <div class="label">Sludge Hours/Week</div>
            </div>
            <div class="stat-card">
                <div class="value">{{ champions.total_champions_identified }}</div>
                <div class="label">Champions Found</div>
            </div>
            <div class="stat-card">
                <div class="value">{{ innovation.theater_rate }}</div>
                <div class="label">AI Theater Rate</div>
            </div>
            <div class="stat-card">
                <div class="value">{{ sludge.estimated_annual_savings_at_90_per_hour }}</div>
                <div class="label">Annual Savings (Est.)</div>
            </div>
        </div>

        <!-- Pillar Scores + Recommendations -->
        <div class="two-col">
            <div class="section">
                <div class="section-title">📊 10-Pillar Maturity Scores</div>
                <div class="pillar-grid">
                    {% for pid, ps in pillar_scores.items() %}
                    <div class="pillar-card">
                        <div class="pillar-header">
                            <span class="pillar-name">{{ pillars[pid].icon }} {{ ps.name }}</span>
                            <span class="pillar-score">{{ ps.average }}/5</span>
                        </div>
                        <div class="pillar-bar-bg">
                            <div class="pillar-bar" style="width: {{ ps.average * 20 }}%;
                                background: {% if ps.average >= 4 %}#2ecc71{% elif ps.average >= 3 %}#f1c40f{% elif ps.average >= 2 %}#e67e22{% else %}#e74c3c{% endif %};"></div>
                        </div>
                        <div class="pillar-level">{{ ps.level }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            <div class="section">
                <div class="section-title">🚀 Priority Actions (Top 10)</div>
                <div class="rec-list">
                    {% for action in assessment.priority_actions %}
                    <div class="rec-item">
                        <div class="rec-pillar">{{ action.pillar }}</div>
                        {{ action.action }}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- Agent Results -->
        <div class="section-title">🤖 AI Agent Scan Results</div>
        <div class="two-col">
            <div class="agent-panel">
                <h3>🧹 Sludge Detector</h3>
                <div class="agent-stat"><span>Total Waste</span><span class="val">{{ sludge.total_sludge_hours_per_week }} hrs/week</span></div>
                <div class="agent-stat"><span>Worst Category</span><span class="val">{{ sludge.worst_category }}</span></div>
                <div class="agent-stat"><span>Annual Savings</span><span class="val">{{ sludge.estimated_annual_savings_at_90_per_hour }}</span></div>
                <div style="margin-top: 12px; font-size: 0.8rem; color: #888;">Top Targets:</div>
                {% for t in sludge.top_5_targets[:3] %}
                <div class="target-item">
                    {{ t.task }}<br/>
                    <span class="score">Impact: {{ t.impact_score }}</span> · {{ t.hours_week }}h/week · {{ t.employees }} employees
                </div>
                {% endfor %}
            </div>
            <div class="agent-panel">
                <h3>🏆 Champion Finder</h3>
                <div class="agent-stat"><span>Champions Found</span><span class="val">{{ champions.total_champions_identified }}</span></div>
                <div class="agent-stat"><span>Top Champion</span><span class="val">{{ champions.top_champion }}</span></div>
                <div style="margin-top: 12px; font-size: 0.8rem; color: #888;">Top Performers:</div>
                {% for c in champions.top_5[:3] %}
                <div class="champion-item">
                    {{ c.name }} ({{ c.dept }})<br/>
                    <span class="score">Score: {{ c.score }}</span> · {{ c.usage_week }} uses/week · {{ c.ideas_implemented }} ideas shipped
                </div>
                {% endfor %}
            </div>
        </div>
        <div class="two-col">
            <div class="agent-panel">
                <h3>🔗 Coordination Auditor</h3>
                <div class="agent-stat"><span>Workflows Audited</span><span class="val">{{ coord.total_workflows_audited }}</span></div>
                <div class="agent-stat"><span>Unique Tools</span><span class="val">{{ coord.unique_tools_in_use }}</span></div>
                <div class="agent-stat"><span>Toggle Switches</span><span class="val">{{ coord.total_toggle_switches }}</span></div>
                <div class="agent-stat"><span>Avg Handoff Latency</span><span class="val">{{ coord.avg_handoff_latency_hours }}h</span></div>
                <div class="agent-stat"><span>Slowest Workflow</span><span class="val">{{ coord.slowest_workflow }}</span></div>
            </div>
            <div class="agent-panel">
                <h3>🧪 Innovation Scanner</h3>
                <div class="agent-stat"><span>Total Experiments</span><span class="val">{{ innovation.total_experiments }}</span></div>
                <div class="agent-stat"><span>In Production</span><span class="val">{{ innovation.production_success_rate }}</span></div>
                <div class="agent-stat"><span>AI Theater Rate</span><span class="val">{{ innovation.theater_rate }}</span></div>
                <div style="margin-top: 12px; font-size: 0.8rem; color: #e74c3c;">⚠️ Flagged:</div>
                {% for f in innovation.flagged_for_review %}
                <div class="target-item">
                    {{ f.name }} ({{ f.team }})<br/>
                    <span class="score">Washing Score: {{ f.washing_score }}/5</span> · {{ f.roi }}
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- ROI -->
        <div class="agent-panel">
            <h3>💰 Estimated ROI (per 1,000 knowledge workers)</h3>
            {% for k, v in roi.items() %}
            <div class="agent-stat">
                <span>{{ k.replace('_', ' ').title() }}</span>
                <span class="val">{{ v }}</span>
            </div>
            {% endfor %}
        </div>
    </div>

    <div class="footer">
        AI Transformation Platform · Source: <a href="https://www.glean.com/work-ai-institute/ai-transformation-100">
        Glean Work AI Institute — AI Transformation 100</a> · Built for AIOps Bootcamp Week 8 Day 6
    </div>
</body>
</html>
"""


@app.route("/")
def dashboard():
    return render_template_string(
        DASHBOARD_HTML,
        assessment=demo_assessment,
        pillar_scores=demo_assessment.pillar_scores,
        pillars=PILLARS,
        sludge=agent_results["sludge_analysis"],
        champions=agent_results["champion_analysis"],
        coord=agent_results["coordination_analysis"],
        innovation=agent_results["innovation_analysis"],
        roi=demo_assessment.estimated_roi
    )


@app.route("/api/assessment", methods=["GET"])
def api_assessment():
    return jsonify({
        "org_name": demo_assessment.org_name,
        "overall_score": demo_assessment.overall_score,
        "overall_level": demo_assessment.overall_level,
        "pillar_scores": {
            pid: {"name": ps.name, "average": ps.average, "level": ps.level}
            for pid, ps in demo_assessment.pillar_scores.items()
        },
        "top_strengths": demo_assessment.top_strengths,
        "top_gaps": demo_assessment.top_gaps,
        "priority_actions": demo_assessment.priority_actions,
        "estimated_roi": demo_assessment.estimated_roi
    })


@app.route("/api/agents", methods=["GET"])
def api_agents():
    return jsonify(agent_results)


@app.route("/api/pillars", methods=["GET"])
def api_pillars():
    return jsonify(PILLARS)


@app.route("/api/sludge", methods=["GET"])
def api_sludge():
    return jsonify(agent_results["sludge_analysis"])


@app.route("/api/champions", methods=["GET"])
def api_champions():
    return jsonify(agent_results["champion_analysis"])


@app.route("/api/coordination", methods=["GET"])
def api_coordination():
    return jsonify(agent_results["coordination_analysis"])


@app.route("/api/innovation", methods=["GET"])
def api_innovation():
    return jsonify(agent_results["innovation_analysis"])


if __name__ == "__main__":
    print("=" * 60)
    print("🧠 AI Transformation Platform")
    print("   Based on: Glean Work AI Institute — AI Transformation 100")
    print("   URL: http://localhost:5006")
    print("   APIs: /api/assessment, /api/agents, /api/pillars")
    print("         /api/sludge, /api/champions, /api/coordination")
    print("         /api/innovation")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5006, debug=True)
