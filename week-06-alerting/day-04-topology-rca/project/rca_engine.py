import networkx as nx
import matplotlib.pyplot as plt

def build_topology():
    """
    Build a sample microservices topology.
    Structure:
    Load Balancer -> Web -> API -> DB
    """
    G = nx.DiGraph()
    
    # Define edges: (caller, callee)
    dependencies = [
        ("LB", "Web-01"),
        ("LB", "Web-02"),
        ("Web-01", "API-Catalog"),
        ("Web-02", "API-Catalog"),
        ("API-Catalog", "Redis-Cache"),
        ("API-Catalog", "Postgres-DB"),
        ("Postgres-DB", "EBS-Storage")
    ]
    
    G.add_edges_from(dependencies)
    return G

def run_rca(graph, active_alerts):
    """
    Identify the root cause from a list of active alerts.
    Logic: The root cause is a node that is alerting but none of its 
    downstream dependencies are alerting.
    """
    root_causes = []
    
    for node in active_alerts:
        # Get all neighbors (downstream dependencies in our DiGraph)
        dependencies = list(graph.neighbors(node))
        
        # If none of the dependencies are in the active_alerts list,
        # it means this node is the 'end of the line' for the failure chain
        is_dependent_failing = any(dep in active_alerts for dep in dependencies)
        
        if not is_dependent_failing:
            root_causes.append(node)
            
    return root_causes

def visualize_topology(graph, active_alerts, root_causes):
    """
    Draw the graph with colored status.
    Red = Root Cause
    Orange = Symptom
    Green = Healthy
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    
    node_colors = []
    for node in graph.nodes():
        if node in root_causes:
            node_colors.append('red')
        elif node in active_alerts:
            node_colors.append('orange')
        else:
            node_colors.append('lightgreen')
            
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, 
            node_size=3000, font_size=10, arrowsize=20)
    
    plt.title("AIOps Topology RCA\nRed: Root Cause | Orange: Symptom")
    plt.savefig("topology_rca.png")
    print("Visualization saved to topology_rca.png")

if __name__ == "__main__":
    # 1. Setup Topology
    topo = build_topology()
    
    # 2. Define Scenario: DB Storage failure
    # This causes the DB and the Catalog API to alert
    alerts = ["API-Catalog", "Postgres-DB", "EBS-Storage"]
    
    print(f"Active Alerts: {alerts}")
    
    # 3. Predict Root Cause
    rc = run_rca(topo, alerts)
    print(f"Identified Root Causes: {rc}")
    
    # 4. Visualize
    visualize_topology(topo, alerts, rc)
