# Resources: LLMs for AIOps

Generative AI is transforming how we handle incidents, documentation, and root cause analysis.

---

## 🛠️ Tools & Models

- **Gemma (Google)**: [Lightweight, state-of-the-art open models](https://ai.google.dev/gemma) - Great for local AIOps tasks.
- **LangChain**: [Framework for building LLM applications](https://www.langchain.com/) - The industry standard for chaining AIOps tasks.
- **Weights & Biases**: [LLM Evaluation and Monitoring](https://wandb.ai/site/solutions/llmops) - Essential for "LLM Ops."
- **Microsoft Presidio**: [PII Redaction Library](https://microsoft.github.io/presidio/) - A robust alternative to our regex-based redactor.

## 📖 Key Readings

- **Incident Analysis at Scale**: [How LLMs help SREs](https://www.pagerduty.com/blog/generative-ai-for-incident-response/)
- **Prompt Engineering Guide**: [General Best Practices](https://www.promptingguide.ai/)
- **Operationalizing LLMs**: [The LLM Ops Landscape](https://github.com/ich918/LLMOps-Roadmap)

## 📺 Videos & Tutorials

- **RAG in 5 Minutes**: [Retrieval Augmented Generation Explained](https://www.youtube.com/watch?v=T-D1OfcDW1M)
- **Vector Databases for SREs**: [Storing and searching logs semantically](https://www.youtube.com/watch?v=klTvEwg3oI4)

## 🧠 Theory: Semantic Search vs. Keyword Search
In the past, we searched logs for the word "ERROR". 
With **Vector Databases** (like Pinecone or Weaviate), we search for the *meaning* of the log. 
If a log says "Database gone away" and another says "Connection refused", a semantic search platform knows they are related to the same underlying network issue.

---

<p align="center">
  <a href="../lecture-notes.md">⬅️ Back: Lecture Notes</a> | <a href="../project/README.md">Next: Project ➡️</a>
</p>
