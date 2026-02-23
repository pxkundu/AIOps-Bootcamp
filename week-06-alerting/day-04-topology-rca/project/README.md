# Project: Build a Topology-Aware RCA Engine

In this project, you will build a Python engine that takes a list of active alerts and a system dependency graph, and outputs the most likely Root Cause.

## 🏃 Setup

1. Install requirements:
   ```bash
   pip install networkx matplotlib
   ```

2. Open `rca_engine.py` to begin.

## 🎯 Tasks

1. **Define the Topology:** Create a graph representing a standard 3-tier app (Frontend -> API -> DB).
2. **Inject Alerts:** Simulate a scenario where the DB is down, causing the API and Frontend to alert.
3. **Run RCA:** Implement the logic to "walk the graph" and identify that the DB is the root cause.
4. **Visualize:** Generate a PNG image of the graph with the root cause highlighted.

## 📂 File Structure
- `rca_engine.py`: The main logic.
- `topology.json`: (Optional) Store your graph structure here.
- `output/`: Folder to save your visualizations.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <strong>Day 4 Project</strong> | <a href="../../day-05-causality/lecture-notes.md">Next: Day 5 ➡️</a>
</p>
