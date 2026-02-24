import json
import networkx as nx
from datetime import datetime, timedelta
import pandas as pd

class AlertSentinel:
    def __init__(self, topo_path, alerts_path):
        self.topo_path = topo_path
        self.alerts_path = alerts_path
        self.graph = nx.DiGraph()
        self.alerts = []
        self.nodes_data = {}
        
        self.load_topology()
        self.load_alerts()

    def load_topology(self):
        with open(self.topo_path, 'r') as f:
            data = json.load(f)
            for node in data['nodes']:
                self.graph.add_node(node['id'], **node)
                self.nodes_data[node['id']] = node
            for edge in data['edges']:
                self.graph.add_edge(edge['source'], edge['target'])
        print(f"✅ Loaded Topology: {len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges")

    def load_alerts(self):
        with open(self.alerts_path, 'r') as f:
            self.alerts = json.load(f)
        print(f"✅ Ingested {len(self.alerts)} raw alerts")

    def correlate_alerts(self, window_seconds=60):
        """
        Groups alerts by temporal proximity (Temporal Correlation).
        """
        correlated_groups = []
        if not self.alerts:
            return correlated_groups

        # Sort alerts by timestamp
        sorted_alerts = sorted(self.alerts, key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '')))
        
        current_group = [sorted_alerts[0]]
        
        for i in range(1, len(sorted_alerts)):
            prev_time = datetime.fromisoformat(sorted_alerts[i-1]['timestamp'].replace('Z', ''))
            curr_time = datetime.fromisoformat(sorted_alerts[i]['timestamp'].replace('Z', ''))
            
            if (curr_time - prev_time).total_seconds() <= window_seconds:
                current_group.append(sorted_alerts[i])
            else:
                correlated_groups.append(current_group)
                current_group = [sorted_alerts[i]]
        
        correlated_groups.append(current_group)
        return correlated_groups

    def find_root_cause(self, alert_group):
        """
        Uses topology graph to find the root cause (Topological RCA).
        Strategy: The 'deepest' node in the dependency graph that is failing.
        """
        alerting_services = [a['service'] for a in alert_group]
        
        possible_rcs = []
        for service in alerting_services:
            # Check if this service has any downstream dependencies that are ALSO alerting
            downstream = list(self.graph.neighbors(service))
            symptom_found = False
            for dep in downstream:
                if dep in alerting_services:
                    symptom_found = True
                    break
            
            if not symptom_found:
                possible_rcs.append(service)
        
        return possible_rcs

    def calculate_priority(self, alert_group, root_causes):
        """
        Scores the incident based on criticality and blast radius.
        """
        # Base score from the most critical node involved
        max_crit = max([self.nodes_data.get(a['service'], {}).get('criticality', 1) for a in alert_group])
        
        # Blast radius: How many services are affected?
        blast_radius = len(alert_group)
        
        # Priority Score = Criticality * 10 + Blast Radius * 5
        score = (max_crit * 10) + (blast_radius * 5)
        
        if score > 50: return "P0 - CRITICAL"
        if score > 30: return "P1 - HIGH"
        return "P2 - MEDIUM"

    def process_incidents(self):
        print("\n--- 🧠 AIOps Engine Processing Incidents ---\n")
        incident_groups = self.correlate_alerts()
        
        for i, group in enumerate(incident_groups):
            print(f"Incident #{i+1} ({len(group)} alerts correlated)")
            
            # 1. Identify Root Cause
            rcs = self.find_root_cause(group)
            
            # 2. Score Priority
            priority = self.calculate_priority(group, rcs)
            
            # 3. Generate Summary
            print(f"  Priority: {priority}")
            print(f"  Likely Root Cause: {', '.join(rcs)}")
            print(f"  Impacted Services: {', '.join(set([a['service'] for a in group]))}")
            print(f"  Sample Message: {group[0]['message']}")
            print("-" * 40)

if __name__ == "__main__":
    engine = AlertSentinel(
        topo_path="src/data/topology.json",
        alerts_path="src/data/alerts.json"
    )
    engine.process_incidents()
