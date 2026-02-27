# Week 7 Day 3: LLM-powered RCA & Incident Summarization

> **Duration:** 8 hours | **Difficulty:** Intermediate+
> **Focus:** Leveraging Generative AI to make sense of complex operational data.

---

## 🎯 Learning Objectives

By the end of this session, you will:
1. Understand the role of **Large Language Models (LLMs)** in the modern AIOps stack.
2. Build an **Incident Summarizer** that converts raw logs into human-readable reports.
3. Use **Prompt Engineering** to extract Root Cause suggestions from telemetry.
4. Learn how to **Redact Sensitive Data** before sending logs to public APIs (e.g., OpenAI).

---

## 📖 Lecture Content

### 1. The "Wall of Logs" Problem
Even with the best dashboards, a major outage can generate millions of log lines. Humans struggle to find the needle in the haystack. LLMs excel at this because:
- **Semantic Understanding**: They "know" what a database timeout looks like, even if the error message is slightly different.
- **Compression**: They can reduce 10,000 log lines into 3 bullet points.
- **Narrative Generation**: They can explain the "Story" of the outage.

### 2. Prompt Engineering for AIOps
To get a good RCA from an LLM, you can't just say "Fix this log." You need to provide context.

**The "Incidient Prompt" Pattern:**
1. **Role**: "You are an expert SRE."
2. **Context**: "Here is the system topology and recent deployment history."
3. **Evidence**: "Here are the top 20 error logs and the CPU metric spike."
4. **Task**: "Summarize the incident and suggest 3 possible root causes."

### 3. RAG: Retrieval Augmented Generation
The LLM doesn't know *your* company's internal runbooks.
**RAG** allows you to:
1. Search your documentation for similar past incidents.
2. Feed those documents into the LLM context.
3. Ask: "Based on these past incidents, what should I do now?"

### 4. PII Redaction: Safety First
**CRITICAL:** Never send IP addresses, user emails, or auth tokens to a public LLM.
- Use regex-based redaction (e.g., `re.sub()`) in your pre-processing pipeline.
- Replace `192.168.1.5` with `<IP_HOST_A>`.

---

## 🛠️ Implementation: The Log Summarizer

We will build a Python script that takes a "dirty" log file, redacts it, and asks an LLM (simulated via local prompt or API) to summarize it.

---

## ✅ Deliverables for Today

- [ ] A Python script `log_redactor.py` that masks IPs and sensitive keys.
- [ ] A `summarizer.py` script that structures logs into an LLM prompt.
- [ ] A sample "Incident Report" generated from a simulated high-noise log file.

---

<p align="center">
  <a href="../day-02-loops/lecture-notes.md">⬅️ Back: Day 2</a> | <strong>Day 3: LLM RCA</strong> | <a href="../day-04-llm-agents/lecture-notes.md">Next: Day 4 ➡️</a>
</p>
