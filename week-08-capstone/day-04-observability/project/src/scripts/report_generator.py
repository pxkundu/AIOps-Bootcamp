"""
Connector Report Generator — Interactive CLI tool that produces
per-connector and aggregate status reports in JSON and HTML format.
"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from connectors.connector_framework import create_all_connectors
from monitoring.health_monitor import ConnectorHealthMonitor
from alerting.alert_correlator import AlertCorrelator


def generate_individual_report(connector):
    """Generate a detailed report for a single connector."""
    health = connector.get_health()
    ko_count_by_author = {}
    for ko in connector.knowledge_objects:
        author = ko.get("author", "unknown")
        ko_count_by_author[author] = ko_count_by_author.get(author, 0) + 1

    metadata_summary = {}
    for ko in connector.knowledge_objects:
        for key, val in ko.get("metadata", {}).items():
            if key not in metadata_summary:
                metadata_summary[key] = []
            metadata_summary[key].append(str(val))

    report = {
        "report_type": "Individual Connector Report",
        "generated_at": datetime.utcnow().isoformat(),
        "connector_name": connector.name,
        "source_type": connector.source_type,
        "status": health["status"],
        "items_synced": health["items_synced"],
        "change_rate_per_day": health["change_rate_per_day"],
        "last_crawl": health["last_crawl"],
        "errors": health["errors"],
        "acl_summary": {
            "total_objects": len(connector.acl_map),
            "unique_groups": list(set(
                g for groups in connector.acl_map.values() for g in groups
            )),
        },
        "content_summary": {
            "total_knowledge_objects": len(connector.knowledge_objects),
            "by_author": ko_count_by_author,
        },
        "metadata_fields": {k: list(set(v)) for k, v in metadata_summary.items()},
        "sample_objects": connector.knowledge_objects[:3],
    }
    return report


def generate_aggregate_report(connectors, monitor, correlator):
    """Generate a full platform-wide observability report."""
    dashboard = monitor.get_dashboard_data()
    incidents = correlator.correlate()

    individual_reports = []
    for conn in connectors:
        individual_reports.append(generate_individual_report(conn))

    report = {
        "report_type": "Aggregate Observability Report",
        "generated_at": datetime.utcnow().isoformat(),
        "platform_summary": dashboard["summary"],
        "connector_health": dashboard["connectors"],
        "active_alerts": dashboard["active_alerts"],
        "correlated_incidents": incidents,
        "individual_reports": individual_reports,
    }
    return report


def save_report(report, filename):
    """Save a report to JSON file."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)
    print(f"📄 Report saved: {filepath}")
    return filepath


def interactive_menu():
    """Interactive CLI for generating reports."""
    print("=" * 60)
    print("🔭 Glean Connector Report Generator")
    print("=" * 60)

    # Initialize pipeline
    connectors = create_all_connectors()
    monitor = ConnectorHealthMonitor()
    correlator = AlertCorrelator(time_window_hours=4)

    for conn in connectors:
        conn.crawl()
        monitor.record_snapshot(conn.get_health())
        correlator.ingest_signals(conn.knowledge_objects)

    print("\n📋 Available Reports:")
    print("  [0] Full Aggregate Report (all connectors)")
    for i, conn in enumerate(connectors, 1):
        print(f"  [{i}] {conn.name} ({conn.source_type})")
    print("  [q] Quit")

    while True:
        choice = input("\n👉 Select report number: ").strip()

        if choice.lower() == "q":
            print("👋 Goodbye!")
            break
        elif choice == "0":
            report = generate_aggregate_report(connectors, monitor, correlator)
            save_report(report, f"aggregate_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
            print(f"\n📊 Platform Summary:")
            print(f"   Total Connectors: {report['platform_summary']['total_connectors']}")
            print(f"   Healthy: {report['platform_summary']['healthy']}")
            print(f"   Warnings: {report['platform_summary']['warning']}")
            print(f"   Critical: {report['platform_summary']['critical']}")
            print(f"   Total Items: {report['platform_summary']['total_items_indexed']}")
            print(f"   Correlated Incidents: {len(report['correlated_incidents'])}")
        elif choice.isdigit() and 1 <= int(choice) <= len(connectors):
            conn = connectors[int(choice) - 1]
            report = generate_individual_report(conn)
            save_report(report, f"{conn.name.lower()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
            print(f"\n📊 {conn.name} Report:")
            print(f"   Status: {report['status']}")
            print(f"   Items Synced: {report['items_synced']}")
            print(f"   Change Rate: {report['change_rate_per_day']} items/day")
            print(f"   Authors: {report['content_summary']['by_author']}")
            print(f"   ACL Groups: {report['acl_summary']['unique_groups']}")
            print(f"   Metadata: {list(report['metadata_fields'].keys())}")
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    interactive_menu()
