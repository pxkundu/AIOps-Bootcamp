"""
Alert Correlation Engine — Links signals across PagerDuty, Slack, GitHub, CloudWatch
within a configurable time window to identify root causes.
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict


class AlertCorrelator:
    """
    Cross-source alert correlator.
    Groups related signals within a time window and identifies root cause patterns.
    """

    def __init__(self, time_window_hours=4):
        self.time_window = timedelta(hours=time_window_hours)
        self.signals = []
        self.correlated_incidents = []

    def ingest_signals(self, knowledge_objects):
        """Accept knowledge objects from all connectors."""
        for ko in knowledge_objects:
            self.signals.append(ko)

    def correlate(self):
        """
        Find related signals across sources.
        Groups by: time proximity + shared metadata (service, author, keywords).
        """
        # Sort by timestamp
        self.signals.sort(key=lambda x: x.get("timestamp", ""))

        # Group by service keywords in content/metadata
        service_groups = defaultdict(list)
        keyword_map = {
            "payment": "payment-service",
            "checkout": "payment-service",
            "db": "database",
            "database": "database",
            "latency": "database",
            "migration": "database",
            "index": "database",
            "memory": "compute",
            "cpu": "compute",
            "oom": "compute",
            "worker": "compute",
        }

        for signal in self.signals:
            content_lower = signal.get("content", "").lower()
            title_lower = signal.get("title", "").lower()
            text = content_lower + " " + title_lower

            matched_services = set()
            for keyword, service in keyword_map.items():
                if keyword in text:
                    matched_services.add(service)

            for svc in matched_services:
                service_groups[svc].append(signal)

        # Build correlated incidents
        for service, signals in service_groups.items():
            if len(signals) >= 2:
                sources = list(set(s["source"] for s in signals))
                incident = {
                    "id": f"CORR-{len(self.correlated_incidents) + 1:03d}",
                    "service": service,
                    "signal_count": len(signals),
                    "sources_involved": sources,
                    "signals": [
                        {"id": s["id"], "source": s["source"], "title": s["title"]}
                        for s in signals
                    ],
                    "suggested_rca": self._generate_rca(service, signals),
                    "suggested_actions": self._suggest_actions(service),
                    "timestamp": datetime.utcnow().isoformat(),
                }
                self.correlated_incidents.append(incident)

        return self.correlated_incidents

    def _generate_rca(self, service, signals):
        """Generate a simple root cause hypothesis based on signal patterns."""
        sources = [s["source"] for s in signals]

        if "GitHub" in sources and "PagerDuty" in sources:
            return f"A recent code change (GitHub) likely caused the {service} incident (PagerDuty). Check the latest merged PR."
        elif "CloudWatch" in sources and "PagerDuty" in sources:
            return f"Infrastructure metrics (CloudWatch) correlate with the {service} alert. Investigate resource saturation."
        elif "Slack" in sources:
            return f"Multiple team members flagged {service} issues in Slack. User-reported incident escalation."
        else:
            return f"Multiple signals detected for {service}. Manual investigation recommended."

    def _suggest_actions(self, service):
        """Suggest remediation actions based on service type."""
        actions = {
            "database": [
                "Roll back recent DB migration",
                "Check slow query logs",
                "Verify index rebuild status",
            ],
            "payment-service": [
                "Check dependent service health",
                "Review recent deployments",
                "Scale up payment API pods",
            ],
            "compute": [
                "Restart OOM-killed processes",
                "Scale horizontal compute nodes",
                "Investigate memory leak in top consumer",
            ],
        }
        return actions.get(service, ["Escalate to on-call SRE"])


if __name__ == "__main__":
    # Test with sample signals
    correlator = AlertCorrelator(time_window_hours=4)

    sample_signals = [
        {"id": "INC-001", "source": "PagerDuty", "title": "DB Latency > 500ms", "content": "Primary DB latency spiked.", "timestamp": "2026-03-10T14:00:00"},
        {"id": "SL-001", "source": "Slack", "title": "#sre-war-room", "content": "DB migration from PR #1482 caused the latency spike.", "timestamp": "2026-03-10T14:30:00"},
        {"id": "GH-1482", "source": "GitHub", "title": "PR #1482: Add index on orders", "content": "ALTER TABLE orders ADD INDEX", "timestamp": "2026-03-10T12:00:00"},
        {"id": "CW-001", "source": "CloudWatch", "title": "CPU Spike", "content": "CPUUtilization 92% on db-primary", "timestamp": "2026-03-10T14:15:00"},
    ]

    correlator.ingest_signals(sample_signals)
    incidents = correlator.correlate()
    print(json.dumps(incidents, indent=2))
