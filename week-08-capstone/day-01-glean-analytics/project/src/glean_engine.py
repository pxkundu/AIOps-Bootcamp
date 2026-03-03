import json
import os
import re
import pandas as pd
from datetime import datetime

class GleanSecEngine:
    """
    Simulates a Glean-powered Enterprise Security & Analytics Engine.
    Correlates data from Confluence, Slack, and GitHub to identify risks.
    """
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.knowledge_base = []
        self.security_alerts = []
        
    def load_data(self):
        # 1. Ingest Confluence Docs
        with open(os.path.join(self.data_dir, 'confluence.json'), 'r') as f:
            docs = json.load(f)
            for d in docs:
                self.knowledge_base.append({
                    "id": d['id'],
                    "source": "Confluence",
                    "title": d['title'],
                    "content": d['content'],
                    "author": d['author'],
                    "time": d['last_updated']
                })
        
        # 2. Ingest GitHub Code Metadata
        with open(os.path.join(self.data_dir, 'github.json'), 'r') as f:
            repos = json.load(f)
            for r in repos:
                self.knowledge_base.append({
                    "id": f"GH-{r['repo']}",
                    "source": "GitHub",
                    "title": f"File: {r['filename']}",
                    "content": r['content'],
                    "author": "Commit-Automation",
                    "time": r['last_commit']
                })
                
        # 3. Ingest Slack History
        with open(os.path.join(self.data_dir, 'slack.json'), 'r') as f:
            messages = json.load(f)
            for m in messages:
                self.knowledge_base.append({
                    "id": f"SL-{m['time']}",
                    "source": "Slack",
                    "title": f"Message in {m['channel']}",
                    "content": m['message'],
                    "author": m['user'],
                    "time": m['time']
                })
        
        print(f"✅ Indexed {len(self.knowledge_base)} knowledge objects from 3 sources.")

    def run_discovery(self):
        """
        Uses simulated AI search to find security patterns (secrets, credentials, unauth mentions).
        """
        # Secret Keyword Pattern (e.g. 'KEY_VAL', 'TOKEN_')
        secret_pattern = r"([A-Z0-1_]+(?:KEY|TOKEN)[A-Z0-9_]*)"
        
        for obj in self.knowledge_base:
            # 1. Look for secrets in content
            secrets_found = re.findall(secret_pattern, obj['content'])
            if secrets_found:
                self.security_alerts.append({
                    "id": f"SEC-{len(self.security_alerts)}",
                    "type": "Credential Leak",
                    "risk": "Critical",
                    "source": obj['source'],
                    "item": obj['title'],
                    "details": f"Found secrets: {', '.join(secrets_found)}",
                    "author": obj['author'],
                    "time": obj['time']
                })
            
            # 2. Look for keywords about unauthorized data in Slack messages
            if obj['source'] == "Slack" and "creds" in obj['content'].lower():
                self.security_alerts.append({
                    "id": f"SEC-{len(self.security_alerts)}",
                    "type": "Policy Violation",
                    "risk": "High",
                    "source": "Slack",
                    "item": obj['title'],
                    "details": f"User {obj['author']} highlighted a security leak: '{obj['content']}'",
                    "author": obj['author'],
                    "time": obj['time']
                })
        
        print(f"🧠 Glean-SEC Discovery: Identified {len(self.security_alerts)} unique risks.")

    def get_risk_df(self):
        return pd.DataFrame(self.security_alerts)

if __name__ == "__main__":
    # Test simulation
    engine = GleanSecEngine("data")
    engine.load_data()
    engine.run_discovery()
    print(engine.get_risk_df())
