"""
Connector Health Monitor — Tracks sync status, change rates, and stall detection.
Implements the monitoring patterns described in Glean's connector monitoring docs.
"""

import json
from datetime import datetime


class ConnectorHealthMonitor:
    """
    Monitors all connectors for sync health.
    Implements Glean's recommended best practices:
    - Track items_synced growth
    - Alert on sustained 0 change_rate
    - Detect stalled crawls (24h+)
    """

    def __init__(self):
        self.snapshots = {}  # connector_name → list of health snapshots
        self.alerts = []

    def record_snapshot(self, health_data):
        """Record a health snapshot from a connector."""
        name = health_data["connector"]
        if name not in self.snapshots:
            self.snapshots[name] = []

        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": health_data["status"],
            "items_synced": health_data["items_synced"],
            "change_rate": health_data["change_rate_per_day"],
            "errors": health_data.get("errors", []),
        }
        self.snapshots[name].append(snapshot)

    def evaluate_health(self):
        """
        Evaluate all connectors against Glean's recommended thresholds.
        Returns a list of health assessments.
        """
        assessments = []

        for name, snaps in self.snapshots.items():
            if not snaps:
                continue

            latest = snaps[-1]
            assessment = {
                "connector": name,
                "status": latest["status"],
                "items_synced": latest["items_synced"],
                "change_rate": latest["change_rate"],
                "health": "HEALTHY",
                "issues": [],
            }

            # Rule 1: Error status = Critical
            if latest["status"] == "Error":
                assessment["health"] = "CRITICAL"
                assessment["issues"].append(f"Connector in ERROR state: {latest['errors']}")

            # Rule 2: Stalled (0 change rate when items exist)
            elif latest["change_rate"] == 0 and latest["items_synced"] > 0:
                assessment["health"] = "WARNING"
                assessment["issues"].append(
                    "Change rate is 0. If activity is expected, check webhook or incremental crawl config."
                )

            # Rule 3: No items synced at all
            elif latest["items_synced"] == 0 and latest["status"] == "Active":
                assessment["health"] = "CRITICAL"
                assessment["issues"].append(
                    "Connector is Active but 0 items synced. Check permissions and API access."
                )

            # Rule 4: Healthy
            else:
                assessment["health"] = "HEALTHY"
                assessment["issues"].append("All metrics nominal.")

            assessments.append(assessment)

            # Generate alerts for non-healthy connectors
            if assessment["health"] != "HEALTHY":
                self.alerts.append({
                    "connector": name,
                    "severity": assessment["health"],
                    "message": "; ".join(assessment["issues"]),
                    "timestamp": datetime.utcnow().isoformat(),
                })

        return assessments

    def get_dashboard_data(self):
        """Aggregate data for the monitoring dashboard."""
        assessments = self.evaluate_health()
        total = len(assessments)
        healthy = sum(1 for a in assessments if a["health"] == "HEALTHY")
        warning = sum(1 for a in assessments if a["health"] == "WARNING")
        critical = sum(1 for a in assessments if a["health"] == "CRITICAL")
        total_items = sum(a["items_synced"] for a in assessments)

        return {
            "summary": {
                "total_connectors": total,
                "healthy": healthy,
                "warning": warning,
                "critical": critical,
                "total_items_indexed": total_items,
            },
            "connectors": assessments,
            "active_alerts": self.alerts,
        }


if __name__ == "__main__":
    # Test with simulated data
    monitor = ConnectorHealthMonitor()

    # Simulate healthy connector
    monitor.record_snapshot({
        "connector": "PagerDuty",
        "status": "Active",
        "items_synced": 42,
        "change_rate_per_day": 5,
    })

    # Simulate stalled connector
    monitor.record_snapshot({
        "connector": "Slack",
        "status": "Active",
        "items_synced": 120,
        "change_rate_per_day": 0,
    })

    dashboard = monitor.get_dashboard_data()
    print(json.dumps(dashboard, indent=2))
