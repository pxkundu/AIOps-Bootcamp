"""
AI Transformation Agents
Based on the Glean Work AI Institute's "AI Transformation 100" framework.

Four specialized agents that analyze enterprise data to surface:
1. Administrative sludge (wasted hours)
2. AI champions (through behavior, not titles)
3. Coordination tax (handoff friction and tool sprawl)
4. Innovation health (experiment success rates)
"""

import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict


# ═══════════════════════════════════════════════════════════════
# Agent 1: Sludge Detector
# ═══════════════════════════════════════════════════════════════

@dataclass
class SludgeItem:
    task: str
    category: str
    hours_per_week: float
    employees_affected: int
    sentiment_score: float  # 1 = soul-crushing, 5 = tolerable
    automation_feasibility: float  # 1-5
    impact_score: float = 0.0

    def __post_init__(self):
        self.impact_score = round(
            self.hours_per_week * self.employees_affected * (6 - self.sentiment_score) * self.automation_feasibility / 100,
            1
        )


class SludgeDetector:
    """
    Identifies administrative sludge — the joyless, soul-draining work
    that AI can eliminate. Based on the report's recommendation to collect
    employee nominations and use AI to cluster and prioritize them.
    """

    def __init__(self):
        self.sludge_items = []

    def scan(self) -> List[SludgeItem]:
        """Simulate scanning enterprise data for sludge patterns."""
        self.sludge_items = [
            SludgeItem("Compiling weekly status reports from 5 different tools",
                       "Reporting", 3.5, 200, 1.5, 4.5),
            SludgeItem("Scheduling and rescheduling meetings across time zones",
                       "Scheduling", 2.0, 500, 2.0, 4.0),
            SludgeItem("Chasing approvals stuck in bureaucratic queues",
                       "Approvals", 1.5, 350, 1.0, 3.5),
            SludgeItem("Copy-pasting data between CRM, Jira, and spreadsheets",
                       "Data Entry", 2.5, 150, 1.5, 5.0),
            SludgeItem("Searching for the right document across 6 internal wikis",
                       "Information Retrieval", 1.7, 800, 2.0, 4.5),
            SludgeItem("Writing meeting notes and distributing action items",
                       "Meeting Admin", 1.0, 600, 2.5, 5.0),
            SludgeItem("Manually onboarding new hires with scattered docs",
                       "Onboarding", 4.0, 50, 2.0, 3.5),
            SludgeItem("Updating multiple dashboards with the same metrics",
                       "Dashboard Sync", 1.5, 100, 1.0, 4.0),
            SludgeItem("Preparing briefing decks for leadership reviews",
                       "Deck Building", 3.0, 80, 1.5, 4.0),
            SludgeItem("Routing support tickets to the right team manually",
                       "Ticket Routing", 1.0, 200, 2.0, 4.5)
        ]
        self.sludge_items.sort(key=lambda s: s.impact_score, reverse=True)
        return self.sludge_items

    def get_summary(self) -> Dict:
        if not self.sludge_items:
            self.scan()
        total_hours = sum(s.hours_per_week * s.employees_affected for s in self.sludge_items)
        top_category = {}
        for s in self.sludge_items:
            top_category[s.category] = top_category.get(s.category, 0) + s.impact_score
        worst_category = max(top_category, key=top_category.get)
        return {
            "total_sludge_hours_per_week": round(total_hours),
            "employees_impacted": len(set(s.employees_affected for s in self.sludge_items)),
            "worst_category": worst_category,
            "top_5_targets": [
                {"task": s.task, "category": s.category, "impact_score": s.impact_score,
                 "hours_week": s.hours_per_week, "employees": s.employees_affected}
                for s in self.sludge_items[:5]
            ],
            "estimated_annual_savings_at_90_per_hour": f"${round(total_hours * 52 * 90):,}"
        }


# ═══════════════════════════════════════════════════════════════
# Agent 2: Champion Finder
# ═══════════════════════════════════════════════════════════════

@dataclass
class AIChampion:
    name: str
    department: str
    ai_usage_per_week: int
    tips_shared: int
    hackathon_ideas_submitted: int
    ideas_implemented: int
    champion_score: float = 0.0

    def __post_init__(self):
        implementation_rate = self.ideas_implemented / max(self.hackathon_ideas_submitted, 1)
        sharing_ratio = self.tips_shared / max(self.ai_usage_per_week, 1)
        self.champion_score = round(
            (self.ai_usage_per_week * 0.3 +
             sharing_ratio * 20 * 0.3 +
             implementation_rate * 30 * 0.4),
            1
        )


class ChampionFinder:
    """
    Identifies AI champions through behavior, not titles.
    Based on the report: 'Run a prompt-a-thon. Watch who dives in,
    who collaborates, who implements ideas AFTER the challenge ends.'
    """

    def __init__(self):
        self.champions = []

    def scan(self) -> List[AIChampion]:
        """Simulate analyzing employee AI behavior data."""
        self.champions = [
            AIChampion("Alice Chen", "Engineering", 28, 15, 5, 4),
            AIChampion("Marcus Rodriguez", "SRE", 22, 12, 3, 3),
            AIChampion("Priya Sharma", "Product", 18, 20, 7, 3),
            AIChampion("Dave Okafor", "Data Science", 35, 8, 4, 4),
            AIChampion("Sarah Kim", "Marketing", 15, 25, 6, 2),
            AIChampion("James Chen", "Legal", 10, 5, 2, 2),
            AIChampion("Fatima Al-Rashid", "Customer Support", 20, 18, 8, 5),
            AIChampion("Charlie Liu", "Finance", 12, 10, 3, 1),
            AIChampion("Elena Vasquez", "HR", 8, 14, 4, 2),
            AIChampion("Tom Nakamura", "Sales", 16, 22, 5, 3),
        ]
        self.champions.sort(key=lambda c: c.champion_score, reverse=True)
        return self.champions

    def get_summary(self) -> Dict:
        if not self.champions:
            self.scan()
        dept_coverage = {}
        for c in self.champions:
            dept_coverage.setdefault(c.department, []).append(c.name)
        return {
            "total_champions_identified": len([c for c in self.champions if c.champion_score > 10]),
            "top_champion": self.champions[0].name if self.champions else "None",
            "department_coverage": dept_coverage,
            "departments_without_champion": [
                d for d in ["Engineering", "Product", "Sales", "Marketing", "HR",
                           "Finance", "Legal", "SRE", "Customer Support", "Data Science"]
                if d not in dept_coverage
            ],
            "top_5": [
                {"name": c.name, "dept": c.department, "score": c.champion_score,
                 "usage_week": c.ai_usage_per_week, "ideas_implemented": c.ideas_implemented}
                for c in self.champions[:5]
            ]
        }


# ═══════════════════════════════════════════════════════════════
# Agent 3: Coordination Auditor
# ═══════════════════════════════════════════════════════════════

@dataclass
class HandoffChain:
    workflow_name: str
    tools_involved: List[str]
    handoff_count: int
    avg_handoff_latency_hours: float
    toggle_switches: int
    bottleneck_person: str
    total_cycle_time_hours: float = 0.0

    def __post_init__(self):
        self.total_cycle_time_hours = round(
            self.handoff_count * self.avg_handoff_latency_hours + self.toggle_switches * 0.1, 1
        )


class CoordinationAuditor:
    """
    Maps and measures coordination tax, toggle tax, and handoff friction.
    Based on: 'Map how work is really done before you automate' and
    'Tame AI sprawl with super agents.'
    """

    def __init__(self):
        self.handoff_chains = []

    def scan(self) -> List[HandoffChain]:
        """Simulate mapping enterprise coordination patterns."""
        self.handoff_chains = [
            HandoffChain("Bug Report → Fix → Deploy",
                         ["Jira", "Slack", "GitHub", "Jenkins", "Datadog"], 5, 4.0, 12,
                         "Release Manager"),
            HandoffChain("Customer Escalation → Resolution",
                         ["Zendesk", "Slack", "Confluence", "Jira", "Email"], 6, 3.5, 15,
                         "Support Lead"),
            HandoffChain("New Feature → Production",
                         ["Confluence", "Figma", "Jira", "GitHub", "Slack", "Datadog"], 8, 6.0, 20,
                         "Product Manager"),
            HandoffChain("Onboarding → Productive Employee",
                         ["BambooHR", "Slack", "Confluence", "Google Drive", "Jira", "GitHub"], 10, 24.0, 18,
                         "Hiring Manager"),
            HandoffChain("Incident → Postmortem",
                         ["PagerDuty", "Slack", "Datadog", "Confluence", "Jira"], 4, 2.0, 10,
                         "SRE On-Call"),
            HandoffChain("Quarterly OKR Review",
                         ["Google Sheets", "Slack", "Email", "Confluence", "PowerPoint"], 6, 48.0, 14,
                         "Director"),
        ]
        self.handoff_chains.sort(key=lambda h: h.total_cycle_time_hours, reverse=True)
        return self.handoff_chains

    def get_summary(self) -> Dict:
        if not self.handoff_chains:
            self.scan()
        all_tools = set()
        for h in self.handoff_chains:
            all_tools.update(h.tools_involved)
        total_toggles = sum(h.toggle_switches for h in self.handoff_chains)
        return {
            "total_workflows_audited": len(self.handoff_chains),
            "unique_tools_in_use": len(all_tools),
            "total_handoffs_per_cycle": sum(h.handoff_count for h in self.handoff_chains),
            "total_toggle_switches": total_toggles,
            "avg_handoff_latency_hours": round(
                sum(h.avg_handoff_latency_hours for h in self.handoff_chains) / len(self.handoff_chains), 1
            ),
            "slowest_workflow": self.handoff_chains[0].workflow_name if self.handoff_chains else "N/A",
            "super_agent_consolidation_targets": list(all_tools),
            "top_bottleneck_people": list(set(h.bottleneck_person for h in self.handoff_chains))
        }


# ═══════════════════════════════════════════════════════════════
# Agent 4: Innovation Scanner
# ═══════════════════════════════════════════════════════════════

@dataclass
class AIExperiment:
    name: str
    team: str
    phase: str  # ideation, prototype, pilot, production, retired
    days_in_phase: int
    actual_roi: str
    ai_washing_score: int  # 0-5, 0 = genuine, 5 = pure theater
    is_genuine: bool = True

    def __post_init__(self):
        self.is_genuine = self.ai_washing_score <= 2


class InnovationScanner:
    """
    Tracks AI experiment health and flags 'AI theater'.
    Based on: 'Plan for the majority of your AI experiments to fail'
    and the '5-Part AI Washing Gut Check.'
    """

    def __init__(self):
        self.experiments = []

    def scan(self) -> List[AIExperiment]:
        """Simulate scanning AI experiment portfolio."""
        self.experiments = [
            AIExperiment("Meeting Action Summarizer", "Platform", "production", 45, "2.1 hrs/week saved per user", 0),
            AIExperiment("AI Code Review Assistant", "Engineering", "pilot", 30, "15% faster reviews (measured)", 1),
            AIExperiment("Customer Sentiment Analyzer", "Support", "production", 90, "22% faster escalation", 0),
            AIExperiment("AI-Powered Sales Forecasting", "Sales", "prototype", 60, "No measurable impact yet", 3),
            AIExperiment("Smart Ticket Router", "Support", "pilot", 20, "40% right-first-time routing", 1),
            AIExperiment("AI Strategy Deck Generator", "Executive", "retired", 120, "Produced generic outputs", 4),
            AIExperiment("Automated Compliance Checker", "Legal", "prototype", 45, "Early promising results", 2),
            AIExperiment("AI-Powered Onboarding Guide", "HR", "pilot", 35, "30% faster ramp-up (measured)", 1),
            AIExperiment("Predictive Infrastructure Scaling", "SRE", "production", 180, "18% cost reduction", 0),
            AIExperiment("AI Brand Voice Generator", "Marketing", "retired", 90, "Outputs too generic", 4),
            AIExperiment("Knowledge Gap Detector", "Platform", "pilot", 25, "Identified 47 missing docs", 0),
            AIExperiment("AI-Driven OKR Tracker", "Product", "ideation", 10, "N/A", 2),
        ]
        return self.experiments

    def get_summary(self) -> Dict:
        if not self.experiments:
            self.scan()
        phase_counts = {}
        for e in self.experiments:
            phase_counts[e.phase] = phase_counts.get(e.phase, 0) + 1
        genuine = [e for e in self.experiments if e.is_genuine]
        theater = [e for e in self.experiments if not e.is_genuine]
        production = [e for e in self.experiments if e.phase == "production"]
        return {
            "total_experiments": len(self.experiments),
            "phase_distribution": phase_counts,
            "genuine_ai_projects": len(genuine),
            "ai_theater_projects": len(theater),
            "theater_rate": f"{round(len(theater) / len(self.experiments) * 100)}%",
            "production_success_rate": f"{round(len(production) / len(self.experiments) * 100)}%",
            "flagged_for_review": [
                {"name": e.name, "team": e.team, "washing_score": e.ai_washing_score, "roi": e.actual_roi}
                for e in theater
            ],
            "top_successes": [
                {"name": e.name, "team": e.team, "roi": e.actual_roi}
                for e in production
            ]
        }


# ═══════════════════════════════════════════════════════════════
# Agent Orchestrator
# ═══════════════════════════════════════════════════════════════

class AgentOrchestrator:
    """Coordinates all four AI transformation agents."""

    def __init__(self):
        self.sludge = SludgeDetector()
        self.champions = ChampionFinder()
        self.coordination = CoordinationAuditor()
        self.innovation = InnovationScanner()

    def run_all(self) -> Dict:
        """Execute all agents and compile results."""
        return {
            "timestamp": datetime.now().isoformat(),
            "sludge_analysis": self.sludge.get_summary(),
            "champion_analysis": self.champions.get_summary(),
            "coordination_analysis": self.coordination.get_summary(),
            "innovation_analysis": self.innovation.get_summary()
        }


# ═══════════════════════════════════════════════════════════════
# CLI Demo
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    orch = AgentOrchestrator()
    results = orch.run_all()

    print("=" * 70)
    print("🤖 AI TRANSFORMATION AGENTS — ENTERPRISE SCAN RESULTS")
    print(f"📅 {results['timestamp']}")
    print("=" * 70)

    # Sludge
    s = results["sludge_analysis"]
    print(f"\n🧹 SLUDGE DETECTOR")
    print(f"   Total waste: {s['total_sludge_hours_per_week']} hrs/week across the org")
    print(f"   Worst category: {s['worst_category']}")
    print(f"   Estimated annual savings: {s['estimated_annual_savings_at_90_per_hour']}")
    print("   Top targets:")
    for t in s["top_5_targets"]:
        print(f"     ‣ {t['task']} (impact: {t['impact_score']})")

    # Champions
    c = results["champion_analysis"]
    print(f"\n🏆 CHAMPION FINDER")
    print(f"   Champions identified: {c['total_champions_identified']}")
    print(f"   Top champion: {c['top_champion']}")
    print("   Top 5:")
    for ch in c["top_5"]:
        print(f"     ‣ {ch['name']} ({ch['dept']}) — score: {ch['score']}, implemented: {ch['ideas_implemented']}")

    # Coordination
    co = results["coordination_analysis"]
    print(f"\n🔗 COORDINATION AUDITOR")
    print(f"   Workflows audited: {co['total_workflows_audited']}")
    print(f"   Unique tools: {co['unique_tools_in_use']}")
    print(f"   Total toggle switches: {co['total_toggle_switches']}")
    print(f"   Slowest workflow: {co['slowest_workflow']}")

    # Innovation
    inn = results["innovation_analysis"]
    print(f"\n🧪 INNOVATION SCANNER")
    print(f"   Total experiments: {inn['total_experiments']}")
    print(f"   Production success rate: {inn['production_success_rate']}")
    print(f"   AI theater rate: {inn['theater_rate']}")
    print("   Flagged for review:")
    for f in inn["flagged_for_review"]:
        print(f"     ⚠️  {f['name']} ({f['team']}) — washing score: {f['washing_score']}")

    print(f"\n{'=' * 70}")
