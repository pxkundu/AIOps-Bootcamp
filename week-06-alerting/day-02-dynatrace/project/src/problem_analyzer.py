"""
The Root Cause Detective: Dynatrace Problem Analyzer
This script fetches active problems from Dynatrace and identifies the 'Root Cause' entity.
It is an essential component of an automated AIOps triage workflow.
"""

import requests
import os
import json

class DynatraceDetective:
    def __init__(self, tenant_url, api_token):
        self.base_url = tenant_url.rstrip('/')
        self.headers = {
            "Authorization": f"Api-Token {api_token}",
            "Content-Type": "application/json"
        }

    def get_recent_problems(self):
        """Fetches problems from the last 2 hours."""
        url = f"{self.base_url}/api/v2/problems"
        params = {
            "from": "now-2h",
            "pageSize": 5
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json().get('problems', [])
        else:
            print(f"Error fetching problems: {response.status_code} - {response.text}")
            return []

    def analyze_root_cause(self, problem_id):
        """Deep-dive into a specific problem to find the root cause."""
        url = f"{self.base_url}/api/v2/problems/{problem_id}"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            
            evidence = data.get('rootCauseEntity', {})
            impacted = data.get('impactLevel', 'UNKNOWN')
            title = data.get('displayId', 'Unknown Problem')
            
            print(f"\n🕵️ Analyzing {title}...")
            print(f"Status: {data.get('status')}")
            print(f"Impact Level: {impacted}")
            
            if evidence:
                print(f"💡 ROOT CAUSE IDENTIFIED: {evidence.get('name')} ({evidence.get('type')})")
            else:
                print("⚠️  Davis AI is still calculating the root cause...")
                
            return data
        return None

if __name__ == "__main__":
    # Get configuration from env
    TENANT = os.environ.get('DT_TENANT_URL') # e.g., https://abc12345.live.dynatrace.com
    TOKEN = os.environ.get('DT_API_TOKEN')

    if not TENANT or not TOKEN:
        print("ERROR: Please set DT_TENANT_URL and DT_API_TOKEN.")
        exit(1)

    detective = DynatraceDetective(TENANT, TOKEN)
    
    problems = detective.get_recent_problems()
    
    if not problems:
        print("✅ No active problems detected in the environment.")
    else:
        for p in problems:
            detective.analyze_root_cause(p['problemId'])
