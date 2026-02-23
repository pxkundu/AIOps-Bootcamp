# Week 6 Day 4: Topology-Aware Root Cause Analysis (RCA)

> **Duration:** 8 hours | **Difficulty:** Advanced
> **Focus:** Understanding how system dependencies help isolate the source of "Alert Storms."

---

## 🎯 Learning Objectives

By the end of this session, you will:
1. Represent infrastructure as a **Directed Acyclic Graph (DAG)** using `NetworkX`.
2. Map disparate alerts from multiple tools onto a unified topology.
3. Implement the **"Common Upstream" algorithm** to find root causes.
4. Understand the difference between **Temporal** and **Topological** correlation.

---

## 📖 Lecture Content

### 1. The Topology Problem
In a microservices environment, a single database failure can trigger hundreds of alerts across every service that depends on it. 

**The Alert Storm:**
- `db-prod`: Connection Timeout
- `api-checkout`: 500 Internal Server Error
- `payment-service`: Transaction Failed
- `frontend-web`: High Latency

Without topology, you have 4 incidents. With topology, you have **1 Root Cause** and 3 symptoms.

---

### 2. Representing Topology with Graphs
A system topology is a graph where:
- **Nodes** = Services, Databases, Hosts, Load Balancers.
- **Edges** = Dependencies (e.g., "Service A calls Service B").

```python
import networkx as nx

# Create a Directed Graph
G = nx.DiGraph()

# Add dependencies (Source -> Target)
G.add_edge("frontend", "api-gateway")
G.add_edge("api-gateway", "checkout-service")
G.add_edge("checkout-service", "payment-db")
G.add_edge("checkout-service", "inventory-service")
G.add_edge("inventory-service", "inventory-db")
```

---

### 3. Mapping Alerts to the Graph
Once we have a graph, we can "color" the nodes that have active alerts.

```python
# Active Alerts
active_alerts = ["payment-db", "checkout-service", "api-gateway"]

# Any node in active_alerts is marked as 'unhealthy'
for node in G.nodes():
    G.nodes[node]['status'] = 'healthy'
    if node in active_alerts:
        G.nodes[node]['status'] = 'unhealthy'
```

---

### 4. RCA Algorithm: Finding the "Lowest Common Ancestor"
In a dependency graph, the root cause is typically the **deepest** node in the chain that is unhealthy.

**Simple RCA Logic:**
1. Identify all unhealthy nodes.
2. For each unhealthy node, check if any of its **downstream** dependencies are also unhealthy.
3. If a node is unhealthy but *none* of its dependencies are, it is a **Primary Candidate** for the root cause.

```python
def find_root_cause(graph, alerts):
    candidates = []
    for node in alerts:
        # Check if this node has an unhealthy downstream dependency
        is_root = True
        for neighbor in graph.neighbors(node):
            if neighbor in alerts:
                is_root = False
                break
        if is_root:
            candidates.append(node)
    return candidates

# Output: ["payment-db"]
```

---

### 5. Advanced Topic: Probabilistic RCA
Real-world graphs are messy. Sometimes an edge is "flaky." We use **Causal Inference** (e.g., Bayesian Networks) to calculate the probability that Node A caused Node B.

- **Soft Failure:** Service A is slow, but Service B is healthy.
- **Hard Failure:** Service A is disconnected, causing Service B to crash.

---

## 🛠️ Performance Tuning for Large Graphs
1. **Pruning:** Only look at nodes within 2-3 hops of an alert.
2. **Caching:** Pre-compute the dependency tree once a hour (Discovery).
3. **Weighting:** Weigh edges by traffic volume (higher traffic = more likely to propagate failures).

---

## ✅ Deliverables for Today

- [ ] A Python script creating a 10-node topology using `NetworkX`.
- [ ] An RCA function that correctly identifies a database failure in a cascading chain.
- [ ] A visualization of the graph highlighting the identified Root Cause in Red.

---

<p align="center">
  <a href="../day-03-grafana-prom/lecture-notes.md">⬅️ Back: Day 3</a> | <strong>Day 4: Topology RCA</strong> | <a href="../day-05-causality/lecture-notes.md">Next: Day 5 ➡️</a>
</p>
