# Day 2 Exercise: Exploring Data Patterns & Cardinality

## 🎯 Goal
Understand how different observability signals look and feel by generating and analyzing them manually.

---

## 🛠️ Part 1: Simulating High Cardinality
In this part, we will see how adding a unique label (like a User ID) to a metric impacts the system.

1.  Open the `resources/metrics_simulator.py` we created yesterday.
2.  Run the script to generate basic metrics.
3.  **Task:** Modify the script (or create a new one) to add a `user_id` label to every data point.
4.  **Observation:** How does the file size change when you have 1,000 unique `user_id`s compared to just 1 `region` label?

---

## 🛠️ Part 2: JSON Log Parsing
AIOps tools need to "parse" logs into structured data to analyze them.

1.  Use the `resources/log_generator.py` to produce 100 logs.
2.  **Challenge:** Write a simple Python script (or use `jq`) to find all logs with `level="ERROR"` and calculate the average `duration_ms` for those errors.

---

## 🛠️ Part 3: Manual Trace Correlation
Assume you have the following two logs:

**Log A (Front-end):**
`{"ts": "10:00:01", "msg": "API Request Start", "trace_id": "tx-999", "span_id": "span-1"}`

**Log B (Back-end):**
`{"ts": "10:00:02", "msg": "Database Query", "trace_id": "tx-999", "span_id": "span-2", "parent_id": "span-1"}`

1.  Draw the relationship between these two spans using a Mermaid diagram (or paper).
2.  If Log B's `duration_ms` is 500ms, and Log A's total `duration_ms` is 600ms, how much time was spent on networking/overhead between the services?

---

## ✅ Submission
Submit a short `EXPLAIN.md` file in your project folder answering Part 3, and include the snippet of your Part 2 log parser code.
