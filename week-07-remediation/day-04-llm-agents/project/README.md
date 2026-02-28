# Lab: Building the ReAct Troubleshooting Agent

In this lab, you move from standard summarization to **Agentic Reasoning**. You will build an agent that can decide which diagnostic tools to run based on an incoming alert.

---

## 🏗️ Architecture: The Loop
Your agent follows the **Thought -> Action -> Observation** cycle.

1. **Thought**: The LLM analyzes the current state.
2. **Action**: The LLM chooses a Python function to execute.
3. **Observation**: The output of the function is fed back into the LLM context.

---

## 🎯 Project Tasks

### Task 1: Design the Workflow
Use the [Design Challenge Template](../design-challenge.md) to map out how your agent should handle a **Database Latency** alert.

### Task 2: Implement a Simulated Agent
Open `src/simulated_agent.py`. This script demonstrates a hardcoded reasoning loop. 
**Your Job:** Convert the hardcoded `reason()` method into a dynamic one that uses an LLM API (OpenAI, Anthropic, or local Ollama).

### Task 3: Add a Safety Gate
Modify the code so that the agent **cannot** call any tool until it has logged a "Confidence Score" $> 0.7$.

---

## 🏃 Setup
1. (Optional) Install LangChain if you want to use a framework:
   ```bash
   pip install langchain langchain-openai
   ```
2. Run the simulation to see the trace:
   ```bash
   python3 src/simulated_agent.py
   ```

---

<p align="center">
  <a href="../workshop-guide.md">⬅️ Back: Workshop Guide</a> | <strong>Day 4 Project</strong> | <a href="../../day-05-chatops/lecture-notes.md">Next: Day 5 ➡️</a>
</p>
