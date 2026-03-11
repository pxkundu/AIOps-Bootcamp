"""
Glean-Style Connector Framework: Base Connector + Native Connectors
Simulates the crawl → index → sync lifecycle for enterprise data sources.
"""

import json
import os
import time
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class BaseConnector(ABC):
    """
    Abstract base class for all Glean-style connectors.
    Implements the crawl lifecycle: Configure → Crawl → Index → Active.
    """

    def __init__(self, name, source_type, config):
        self.name = name
        self.source_type = source_type
        self.config = config
        self.status = "Configured"
        self.items_synced = 0
        self.change_rate = 0  # items/day
        self.last_crawl = None
        self.knowledge_objects = []
        self.acl_map = {}  # object_id → allowed_groups
        self.errors = []

    @abstractmethod
    def fetch_data(self):
        """Fetch raw data from the source. Must be implemented by each connector."""
        pass

    def crawl(self):
        """Execute the full crawl lifecycle."""
        print(f"🔄 [{self.name}] Starting crawl...")
        self.status = "Crawling"

        try:
            raw_data = self.fetch_data()
            self.status = "Indexing"
            self._index(raw_data)
            self.status = "Active"
            self.last_crawl = datetime.utcnow().isoformat()
            print(f"✅ [{self.name}] Crawl complete. {self.items_synced} items synced.")
        except Exception as e:
            self.status = "Error"
            self.errors.append(str(e))
            print(f"❌ [{self.name}] Crawl failed: {e}")

    def _index(self, raw_data):
        """Transform raw data into Knowledge Objects."""
        for item in raw_data:
            ko = {
                "id": item.get("id", f"{self.name}-{len(self.knowledge_objects)}"),
                "source": self.name,
                "type": self.source_type,
                "title": item.get("title", "Untitled"),
                "content": item.get("content", ""),
                "author": item.get("author", "system"),
                "timestamp": item.get("timestamp", datetime.utcnow().isoformat()),
                "metadata": item.get("metadata", {}),
            }
            self.knowledge_objects.append(ko)

            # Map ACLs
            allowed = item.get("allowed_groups", ["Public"])
            self.acl_map[ko["id"]] = allowed

        self.items_synced = len(self.knowledge_objects)
        self.change_rate = len(raw_data)

    def get_health(self):
        """Return connector health metrics (per Glean monitoring docs)."""
        return {
            "connector": self.name,
            "source_type": self.source_type,
            "status": self.status,
            "items_synced": self.items_synced,
            "change_rate_per_day": self.change_rate,
            "last_crawl": self.last_crawl,
            "errors": self.errors,
        }


class PagerDutyConnector(BaseConnector):
    """Native Connector: PagerDuty Incidents."""

    def __init__(self, config):
        super().__init__("PagerDuty", "Incident Management", config)

    def fetch_data(self):
        # Simulate fetching from PagerDuty API
        return [
            {
                "id": "INC-001",
                "title": "Database Latency > 500ms",
                "content": "Primary DB latency spiked to 850ms. Affecting checkout flow.",
                "author": "monitoring-bot",
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                "metadata": {"severity": "P1", "service": "payment-api", "status": "triggered"},
                "allowed_groups": ["SRE", "Admins"],
            },
            {
                "id": "INC-002",
                "title": "Memory pressure on worker-node-03",
                "content": "Node memory at 94%. OOM killer may trigger.",
                "author": "cloudwatch-agent",
                "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
                "metadata": {"severity": "P2", "service": "compute-cluster", "status": "acknowledged"},
                "allowed_groups": ["SRE", "DevOps"],
            },
        ]


class SlackConnector(BaseConnector):
    """Native Connector: Slack Channels."""

    def __init__(self, config):
        super().__init__("Slack", "Communication", config)

    def fetch_data(self):
        return [
            {
                "id": "SL-MSG-001",
                "title": "Message in #sre-war-room",
                "content": "The DB migration from PR #1482 seems to have caused the latency spike. Rolling back now.",
                "author": "alice.sre",
                "timestamp": (datetime.utcnow() - timedelta(hours=1, minutes=30)).isoformat(),
                "metadata": {"channel": "#sre-war-room"},
                "allowed_groups": ["SRE"],
            },
            {
                "id": "SL-MSG-002",
                "title": "Message in #general",
                "content": "Anyone else seeing slow checkout? It's been 15 minutes.",
                "author": "bob.dev",
                "timestamp": (datetime.utcnow() - timedelta(hours=1, minutes=45)).isoformat(),
                "metadata": {"channel": "#general"},
                "allowed_groups": ["Public"],
            },
        ]


class JiraConnector(BaseConnector):
    """Native Connector: Jira Issues."""

    def __init__(self, config):
        super().__init__("Jira", "Project Management", config)

    def fetch_data(self):
        return [
            {
                "id": "JIRA-4520",
                "title": "Migrate payment DB to PostgreSQL 16",
                "content": "Migration involves index rebuild. Expected 30min downtime window.",
                "author": "charlie.dba",
                "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                "metadata": {"project": "INFRA", "status": "In Progress", "priority": "High"},
                "allowed_groups": ["SRE", "DevOps", "DBA"],
            },
        ]


class GitHubConnector(BaseConnector):
    """Native Connector: GitHub Commits & PRs."""

    def __init__(self, config):
        super().__init__("GitHub", "Source Control", config)

    def fetch_data(self):
        return [
            {
                "id": "GH-PR-1482",
                "title": "PR #1482: Add composite index on orders table",
                "content": "ALTER TABLE orders ADD INDEX idx_user_date (user_id, created_at);",
                "author": "charlie.dba",
                "timestamp": (datetime.utcnow() - timedelta(hours=3)).isoformat(),
                "metadata": {"repo": "enterprise/payment-service", "branch": "main", "merged": True},
                "allowed_groups": ["Developer", "SRE"],
            },
        ]


class CloudWatchConnector(BaseConnector):
    """Custom Connector: AWS CloudWatch Metrics (built via Glean SDK)."""

    def __init__(self, config):
        super().__init__("CloudWatch", "Monitoring", config)

    def fetch_data(self):
        return [
            {
                "id": "CW-METRIC-001",
                "title": "CPU Spike on db-primary",
                "content": "CPUUtilization hit 92% at 14:30 UTC. Correlated with index rebuild.",
                "author": "cloudwatch",
                "timestamp": (datetime.utcnow() - timedelta(hours=2, minutes=15)).isoformat(),
                "metadata": {"namespace": "AWS/RDS", "metric": "CPUUtilization", "value": 92},
                "allowed_groups": ["SRE", "Admins"],
            },
        ]


# --- Factory ---
def create_all_connectors():
    """Factory to instantiate all configured connectors."""
    return [
        PagerDutyConnector({"api_key": "MOCK_PD_KEY"}),
        SlackConnector({"bot_token": "xoxb-MOCK"}),
        JiraConnector({"api_token": "MOCK_JIRA_TOKEN"}),
        GitHubConnector({"pat": "ghp_MOCK_TOKEN"}),
        CloudWatchConnector({"region": "us-east-1"}),
    ]


if __name__ == "__main__":
    connectors = create_all_connectors()
    for conn in connectors:
        conn.crawl()
        print(json.dumps(conn.get_health(), indent=2))
        print()
