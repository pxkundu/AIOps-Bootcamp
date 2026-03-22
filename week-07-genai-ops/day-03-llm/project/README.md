# Project: The Incident Narrator

Build a pipeline that takes messy application logs and generates a clean, executive summary of what went wrong.

---

## 🎯 Tasks

1. **Redactor (`log_redactor.py`)**: 
   - Write a script to find and replace IP addresses (0.0.0.0) and credit card numbers/tokens with placeholders like `[REDACTED_IP]`.
2. **Context Builder (`context_builder.py`)**:
   - Combine redated logs with "System Context" (e.g., "This service handles payments").
3. **Summarizer (`summarize.py`)**:
   - Create a prompt that asks an LLM to identify the **Timeline**, **Symptoms**, and **Likely Root Cause**.

## 🏃 Running the Simulation

1. **`src/app_logs.txt`**: A file containing 100+ lines of messy logs including errors and noise.
2. **Execution**:
   ```bash
   python3 log_redactor.py app_logs.txt
   python3 summarize.py
   ```

## 📂 File Structure
- `src/log_redactor.py`: Data privacy layer.
- `src/summarize.py`: Prompt engineering and LLM interaction.
- `src/app_logs.txt`: The raw data.
