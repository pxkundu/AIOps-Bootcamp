import os

def generate_summary_prompt(logs):
    system_context = """
    SERVICE: Payment-Processing-API
    CRITICALITY: High
    TOPOLOGY: Web-App -> Payment-API -> Postgres-DB
    """
    
    prompt = f"""
    ROLE: You are an expert Site Reliability Engineer.
    
    CONTEXT:
    {system_context}
    
    EVIDENCE (Redacted Logs):
    {logs}
    
    TASK:
    Analyze the logs above and provide:
    1. A one-sentence executive summary of the incident.
    2. A timeline of events.
    3. The most likely root cause.
    4. Recommended immediate action.
    """
    return prompt

if __name__ == "__main__":
    if not os.path.exists("clean_logs.txt"):
        print("❌ Error: No clean_logs.txt found. Run log_redactor.py first.")
    else:
        with open("clean_logs.txt", "r") as f:
            logs = f.read()
        
        full_prompt = generate_summary_prompt(logs)
        
        print("--- 🧠 GENERATED LLM PROMPT ---")
        print(full_prompt)
        print("-------------------------------")
        
        # In a real scenario, you'd call an API here:
        # client = OpenAI()
        # response = client.chat.completions.create(...)
        # print(response.choices[0].message.content)
        
        print("\n💡 NOTE: In a real-world AIOps platform, this prompt would be sent to an LLM (Gemma, GPT-4, Llama) to generate the final human-readable incident report.")
