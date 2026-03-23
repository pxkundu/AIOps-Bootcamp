"""
AI Transformation Platform — Maturity Assessment Engine
Based on the Glean Work AI Institute's "AI Transformation 100" framework.

Implements a 10-pillar maturity assessment with scoring, recommendations,
and ROI estimation for enterprise AI transformation.
"""

import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional


# ═══════════════════════════════════════════════════════════════
# Data Classes
# ═══════════════════════════════════════════════════════════════

PILLARS = {
    "division_of_labor": {
        "name": "Division of Labor",
        "icon": "🧹",
        "description": "Eliminating administrative sludge and rethinking human-AI task allocation",
        "key_insight": "53% of knowledge worker time is lost to administrative sand traps",
        "source": "Asana State of Work Innovation Report, 2024",
        "questions": [
            "What percentage of employee time is spent on administrative tasks that could be automated?",
            "Do you use AI to extract action items from meetings and compile status updates?",
            "Have employees nominated their most joyless, soul-draining tasks for AI automation?"
        ]
    },
    "expertise": {
        "name": "Expertise",
        "icon": "🎓",
        "description": "Balancing generalists and specialists in AI-augmented workflows",
        "key_insight": "Let generalists build first, bring experts in later — but experts make the final calls",
        "source": "Glean AI Transformation 100",
        "questions": [
            "Do you embed AI-savvy experts in business units, or keep them centralized?",
            "When AI generates options, do domain experts make the final decision?",
            "Are generalists empowered to prototype AI solutions before calling in specialists?"
        ]
    },
    "roles": {
        "name": "Roles",
        "icon": "👤",
        "description": "Creating AI drudgery czars, champions, fleet fixers, and merged roles",
        "key_insight": "Champions emerge through action, not nomination — watch behavior in agent-a-thons",
        "source": "Uber, Udemy, Glean internal programs",
        "questions": [
            "Have you appointed AI drudgery czars to systematically identify automation opportunities?",
            "Do you have peer-to-peer AI champions who spread adoption laterally across teams?",
            "Are you experimenting with merging specialized roles to reduce handoffs?"
        ]
    },
    "control": {
        "name": "Control & Governance",
        "icon": "🛡️",
        "description": "AI governance, policy nuance, and leadership authority",
        "key_insight": "If you don't use AI yourself, you're not qualified to set AI policy for your teams",
        "source": "Reid Hoffman, Jensen Huang, Ethan Mollick",
        "questions": [
            "Do your leaders actively use AI tools before setting AI policies?",
            "Do you have nuanced, regularly updated AI governance policies?",
            "Is AI leadership represented at the C-suite level?"
        ]
    },
    "coordination": {
        "name": "Coordination & Silos",
        "icon": "🔗",
        "description": "Breaking bad silos, building super agents, reducing toggle tax",
        "key_insight": "You can't bolt AI onto a broken system — fix coordination first, then automate",
        "source": "Prof. Paul Leonardi (UCSB), Zendesk, Fortune 20 retailer",
        "questions": [
            "Have you mapped how work really gets done before deploying AI?",
            "Do you use super agents instead of disconnected AI copilots?",
            "Do you measure AI's hidden coordination costs, not just its output?"
        ]
    },
    "hiring_talent": {
        "name": "Hiring & Talent",
        "icon": "📋",
        "description": "Evidence-based workforce decisions and AI bias auditing",
        "key_insight": "80% of AI pilots don't achieve imagined gains — don't cut jobs on projections",
        "source": "Fortune 500 VP, Textio bias research",
        "questions": [
            "Do you wait for demonstrated AI productivity gains before making headcount changes?",
            "Do you use AI to audit and reduce bias in hiring, reviews, and promotions?",
            "Do employees have at least one AI growth goal in their performance objectives?"
        ]
    },
    "learning_development": {
        "name": "Learning & Development",
        "icon": "📚",
        "description": "AI as thinking partner, hack-a-thons, and reverse mentoring",
        "key_insight": "Use AI as a thinking partner, not a substitute for thinking",
        "source": "PwC train-the-trainer, Udemy UDays",
        "questions": [
            "Do you use AI as a thinking partner rather than a substitute for thinking?",
            "Do you run hack-a-thons, agent-a-thons, or prompt-a-thons?",
            "Do junior employees mentor seniors on AI tools (reverse mentoring)?"
        ]
    },
    "innovation": {
        "name": "Innovation",
        "icon": "🧪",
        "description": "AI sandboxes, VC-style bets, and anti-AI-washing defense",
        "key_insight": "Plan for the majority of AI experiments to fail — make probabilistic bets like VCs",
        "source": "David Lloyd (Dayforce), Sahin Ahmed",
        "questions": [
            "Do you have an AI sandbox for safe experimentation?",
            "Is there a mandatory review asking 'Does this really need AI?' for new projects?",
            "Do you plan for the majority of AI experiments to fail (VC-style probabilistic bets)?"
        ]
    },
    "leadership": {
        "name": "Leadership",
        "icon": "🏛️",
        "description": "Leading by example, building organizational AI rhythm, amplification audits",
        "key_insight": "When managers use AI 5+ times/week, team adoption rises to 75%",
        "source": "Worklytics research, Fortune 50 interviews",
        "questions": [
            "Do leaders demo AI tools in staff meetings and show real usage?",
            "Is AI a standing agenda item in executive forums and team meetings?",
            "Have you run an 'amplification audit' — asking what AI will magnify in your culture?"
        ]
    },
    "measurement": {
        "name": "Measurement & ROI",
        "icon": "📊",
        "description": "Tracking real outcomes, avoiding vanity metrics and AI theater",
        "key_insight": "Every AI claim should tie to something specific you can measure — not adjectives",
        "source": "5-Part AI Washing Gut Check",
        "questions": [
            "Is every AI claim in your org tied to a specific, measurable outcome?",
            "Do you guard against vanity metrics and 'AI theater'?",
            "Are metrics in the hands of teams, not just management?"
        ]
    }
}

MATURITY_LEVELS = {
    1: {"name": "Ad-hoc", "color": "#e74c3c", "description": "No formal AI processes; scattered individual experiments"},
    2: {"name": "Opportunistic", "color": "#e67e22", "description": "Team-level pilots; some awareness of AI potential"},
    3: {"name": "Systematic", "color": "#f1c40f", "description": "Cross-functional programs; formal AI roles and policies"},
    4: {"name": "Managed", "color": "#2ecc71", "description": "Governed, measured, scaled AI deployments with ROI tracking"},
    5: {"name": "Optimizing", "color": "#9b59b6", "description": "Self-improving AI ecosystem; continuous experimentation"}
}


@dataclass
class PillarScore:
    pillar_id: str
    name: str
    scores: list  # List of 3 question scores (1-5)
    average: float = 0.0
    level: str = ""
    recommendations: list = field(default_factory=list)

    def __post_init__(self):
        if self.scores:
            self.average = round(sum(self.scores) / len(self.scores), 1)
            self.level = self._get_level()
            self.recommendations = self._generate_recommendations()

    def _get_level(self):
        for lvl in sorted(MATURITY_LEVELS.keys(), reverse=True):
            if self.average >= lvl - 0.5:
                return MATURITY_LEVELS[lvl]["name"]
        return MATURITY_LEVELS[1]["name"]

    def _generate_recommendations(self):
        recs = RECOMMENDATION_DB.get(self.pillar_id, {})
        if self.average < 2:
            return recs.get("critical", [])
        elif self.average < 3:
            return recs.get("high", [])
        elif self.average < 4:
            return recs.get("medium", [])
        else:
            return recs.get("advanced", [])


@dataclass
class AssessmentResult:
    org_name: str
    assessor: str
    timestamp: str
    pillar_scores: dict  # pillar_id -> PillarScore
    overall_score: float = 0.0
    overall_level: str = ""
    top_strengths: list = field(default_factory=list)
    top_gaps: list = field(default_factory=list)
    priority_actions: list = field(default_factory=list)
    estimated_roi: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.pillar_scores:
            scores = [ps.average for ps in self.pillar_scores.values()]
            self.overall_score = round(sum(scores) / len(scores), 1)
            self.overall_level = self._get_overall_level()
            self._compute_strengths_and_gaps()
            self._compile_priority_actions()
            self._estimate_roi()

    def _get_overall_level(self):
        for lvl in sorted(MATURITY_LEVELS.keys(), reverse=True):
            if self.overall_score >= lvl - 0.5:
                return MATURITY_LEVELS[lvl]["name"]
        return MATURITY_LEVELS[1]["name"]

    def _compute_strengths_and_gaps(self):
        sorted_pillars = sorted(self.pillar_scores.values(), key=lambda ps: ps.average, reverse=True)
        self.top_strengths = [(ps.name, ps.average) for ps in sorted_pillars[:3]]
        self.top_gaps = [(ps.name, ps.average) for ps in sorted_pillars[-3:]]

    def _compile_priority_actions(self):
        all_recs = []
        for ps in self.pillar_scores.values():
            for rec in ps.recommendations:
                all_recs.append({"pillar": ps.name, "action": rec, "pillar_score": ps.average})
        all_recs.sort(key=lambda r: r["pillar_score"])
        self.priority_actions = all_recs[:10]

    def _estimate_roi(self):
        sludge_score = self.pillar_scores.get("division_of_labor", PillarScore("", "", [])).average
        coord_score = self.pillar_scores.get("coordination", PillarScore("", "", [])).average
        # Conservative estimates per 1000 employees
        sludge_hours = max(0, (5 - sludge_score) * 200)
        coord_hours = max(0, (5 - coord_score) * 150)
        hourly_rate = 90
        self.estimated_roi = {
            "sludge_hours_recoverable_per_week": round(sludge_hours),
            "coordination_hours_recoverable_per_week": round(coord_hours),
            "estimated_annual_savings": f"${round((sludge_hours + coord_hours) * hourly_rate * 52):,}",
            "note": "Estimates based on 1,000 knowledge workers at $90/hr average"
        }


# ═══════════════════════════════════════════════════════════════
# Recommendation Database
# ═══════════════════════════════════════════════════════════════

RECOMMENDATION_DB = {
    "division_of_labor": {
        "critical": [
            "Survey employees to collect the top 10 most joyless, soul-draining admin tasks",
            "Deploy a meeting action summary agent (e.g., Glean's Daily Meeting Action Summary)",
            "Audit: how many hours/week do employees spend on status updates, scheduling, and approvals?"
        ],
        "high": [
            "Unify unstructured data (Slack, email, docs) into an AI-searchable Knowledge Graph",
            "Replace briefing decks with AI-compiled briefs from project tools"
        ],
        "medium": [
            "Measure sludge reduction monthly and publish team scorecards",
            "Automate the top 5 admin tasks identified by employees"
        ],
        "advanced": [
            "Build autonomous agents that proactively eliminate sludge without human initiation",
            "Share your sludge automation playbook across the organization"
        ]
    },
    "expertise": {
        "critical": [
            "Embed at least one AI-literate member in each business unit",
            "Establish rule: AI generates options, humans make decisions"
        ],
        "high": [
            "Create a 'generalist → prototype → expert review' workflow for AI projects",
            "Beware 'vibe coding the last mile' — ensure expert review on production-bound AI"
        ],
        "medium": ["Build an expertise directory showing who to consult for each AI domain"],
        "advanced": ["Train domain experts to review and critique AI outputs systematically"]
    },
    "roles": {
        "critical": [
            "Appoint an AI drudgery czar in each major function",
            "Run a prompt-a-thon to surface organic AI champions through behavior"
        ],
        "high": [
            "Create a 'Fleet Fixer' role to coordinate multi-agent systems",
            "Consider merging specialized roles to reduce handoff friction"
        ],
        "medium": ["Decide: is prompt engineering a dedicated role or a universal skill?"],
        "advanced": ["Sketch what your org chart looks like when managers supervise AI agents, not just people"]
    },
    "control": {
        "critical": [
            "Leaders must spend 10+ focused hours using AI before setting policy (Mollick's rule)",
            "Draft initial AI governance policies — nuanced, not one-size-fits-all"
        ],
        "high": [
            "Schedule quarterly AI policy reviews to keep governance current",
            "Break down the walls between IT and HR for AI workforce planning"
        ],
        "medium": ["If AI is crucial to strategy, ensure AI leaders are in the C-suite"],
        "advanced": ["Sketch your future org chart with agent management structures"]
    },
    "coordination": {
        "critical": [
            "Map how work REALLY gets done before deploying AI — not org chart, actual handoffs",
            "Fix broken coordination systems BEFORE expecting AI to improve them"
        ],
        "high": [
            "Pilot a super agent — a single front door to multiple AI tools",
            "Measure toggle tax: how many tool switches per task?"
        ],
        "medium": ["Use AI to stress-test 'happy path' workflows before handoffs"],
        "advanced": ["Deploy truly autonomous agents that resolve coordination without human routing"]
    },
    "hiring_talent": {
        "critical": [
            "Establish rule: NO role changes until AI productivity gains are measured in real world",
            "Audit talent pipeline end-to-end for AI-amplified bias"
        ],
        "high": [
            "Ask employees to set at least one AI growth goal",
            "Use AI to standardize interview notes and reduce evaluation bias"
        ],
        "medium": ["Use AI to create 'How to work with me' manuals for every employee"],
        "advanced": ["Use AI to surface and celebrate employee achievements proactively"]
    },
    "learning_development": {
        "critical": [
            "Position AI as a THINKING PARTNER — not a replacement for thinking",
            "Run your first company-wide hack-a-thon or prompt-a-thon"
        ],
        "high": [
            "Implement reverse mentoring: juniors train seniors on AI tools",
            "Coach teams to use AI to break big challenges into smaller pieces"
        ],
        "medium": ["Design AI incentives that fit your team's DNA — not one-size-fits-all"],
        "advanced": ["Build a continuous learning culture around AI where experimentation is rewarded"]
    },
    "innovation": {
        "critical": [
            "Build an AI sandbox for safe experimentation",
            "Add mandatory review: 'Does this problem actually require AI?'"
        ],
        "high": [
            "Run the 5-Part AI Washing Gut Check on every vendor pitch",
            "Protect dedicated time for AI experimentation"
        ],
        "medium": ["Make probabilistic bets on AI projects like VCs — expect most to fail"],
        "advanced": ["Treat employees as 'customer zero' for AI tools — especially the toughest critics"]
    },
    "leadership": {
        "critical": [
            "Leaders MUST visibly use AI in meetings and one-on-ones",
            "Make AI a standing agenda item in executive forums and team meetings"
        ],
        "high": [
            "Run an 'amplification audit' — what will AI magnify in your culture?",
            "Name the J-curve: acknowledge that AI transformation dips before it climbs"
        ],
        "medium": ["Figure out where time savings from AI actually happen vs. where you wish they would"],
        "advanced": ["Build an organizational AI rhythm — weekly, monthly, quarterly cadences"]
    },
    "measurement": {
        "critical": [
            "Tie EVERY AI claim to a specific, measurable outcome",
            "Kill vanity metrics: 'We deployed 50 AI tools' means nothing without usage data"
        ],
        "high": [
            "Put metrics in the hands of teams, not just management",
            "Don't turn AI adoption into a stack-rank exercise"
        ],
        "medium": ["Track before/after metrics for every AI pilot"],
        "advanced": ["Build automated ROI dashboards that self-update with real-world data"]
    }
}


# ═══════════════════════════════════════════════════════════════
# Assessment Engine
# ═══════════════════════════════════════════════════════════════

class TransformationAssessor:
    """Runs the 10-pillar AI Transformation maturity assessment."""

    def __init__(self):
        self.pillars = PILLARS
        self.levels = MATURITY_LEVELS

    def get_pillars(self):
        """Return pillar definitions for the UI."""
        return self.pillars

    def assess(self, org_name: str, assessor: str, responses: dict) -> AssessmentResult:
        """
        Run the full assessment.
        responses: {pillar_id: [score1, score2, score3]} where scores are 1-5
        """
        pillar_scores = {}
        for pillar_id, scores in responses.items():
            if pillar_id in self.pillars:
                ps = PillarScore(
                    pillar_id=pillar_id,
                    name=self.pillars[pillar_id]["name"],
                    scores=scores
                )
                pillar_scores[pillar_id] = ps

        result = AssessmentResult(
            org_name=org_name,
            assessor=assessor,
            timestamp=datetime.now().isoformat(),
            pillar_scores=pillar_scores
        )
        return result

    def get_demo_assessment(self) -> AssessmentResult:
        """Run a demo assessment with sample data for a mid-maturity enterprise."""
        demo_responses = {
            "division_of_labor": [4, 3, 2],
            "expertise": [3, 4, 3],
            "roles": [2, 2, 1],
            "control": [3, 2, 2],
            "coordination": [2, 1, 2],
            "hiring_talent": [3, 3, 2],
            "learning_development": [4, 3, 2],
            "innovation": [2, 3, 1],
            "leadership": [3, 3, 2],
            "measurement": [2, 2, 1]
        }
        return self.assess("Acme Corp (Demo)", "AI Transformation Team", demo_responses)


# ═══════════════════════════════════════════════════════════════
# CLI Demo
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    assessor = TransformationAssessor()
    result = assessor.get_demo_assessment()

    print("=" * 70)
    print(f"🧠 AI TRANSFORMATION MATURITY REPORT — {result.org_name}")
    print(f"📅 {result.timestamp}")
    print(f"👤 Assessed by: {result.assessor}")
    print("=" * 70)
    print(f"\n🎯 Overall Score: {result.overall_score}/5.0 ({result.overall_level})")

    print(f"\n{'─' * 70}")
    print("📊 PILLAR SCORES")
    print(f"{'─' * 70}")
    for pid, ps in result.pillar_scores.items():
        icon = PILLARS[pid]["icon"]
        bar = "█" * int(ps.average * 4) + "░" * (20 - int(ps.average * 4))
        print(f"  {icon} {ps.name:<28} {bar} {ps.average}/5.0 ({ps.level})")

    print(f"\n{'─' * 70}")
    print("💪 TOP STRENGTHS")
    for name, score in result.top_strengths:
        print(f"  ✅ {name}: {score}/5.0")

    print(f"\n{'─' * 70}")
    print("⚠️  TOP GAPS (Highest Priority)")
    for name, score in result.top_gaps:
        print(f"  🔴 {name}: {score}/5.0")

    print(f"\n{'─' * 70}")
    print("🚀 TOP 10 PRIORITY ACTIONS")
    for i, action in enumerate(result.priority_actions, 1):
        print(f"  {i:2d}. [{action['pillar']}] {action['action']}")

    print(f"\n{'─' * 70}")
    print("💰 ESTIMATED ROI (per 1,000 knowledge workers)")
    for k, v in result.estimated_roi.items():
        label = k.replace("_", " ").title()
        print(f"  📈 {label}: {v}")

    print(f"\n{'=' * 70}")
    print("Report generated by the AI Transformation Platform")
    print(f"Source: Glean Work AI Institute — AI Transformation 100")
    print(f"{'=' * 70}")
