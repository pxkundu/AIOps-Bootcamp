"""
The Root Cause Detective: Serverless DQL Dashboard
This script programmatically creates a Dynatrace Dashboard (using DQL - Dynatrace Query Language)
tailored for a Serverless Architecture on AWS (Lambda, API Gateway, S3).
"""

import requests
import os
import json

class ServerlessDashboardBuilder:
    def __init__(self, tenant_url, api_token):
        self.base_url = tenant_url.rstrip('/')
        self.headers = {
            "Authorization": f"Api-Token {api_token}",
            "Content-Type": "application/json"
        }

    def create_dashboard(self):
        """
        Creates a Dashboard using the Dynatrace Documents API (New Grail Platform).
        This dashboard uses DQL for real-time aggregation of AWS Serverless metrics.
        """
        url = f"{self.base_url}/api/v2/dashboards"
        
        # Dashboard Definition (Simplified for the Dashboards v2 API)
        # Note: In the new platform, you often use 'Documents' for DQL, 
        # but the standard Dashboards API still supports DQL via tiles.
        dashboard_json = {
            "dashboardMetadata": {
                "name": "[AIOps] AWS Serverless Triage Center (DQL)",
                "shared": True,
                "owner": "AIOps-Bootcamp",
                "tags": ["aws", "serverless", "dql"]
            },
            "tiles": [
                {
                    "name": "Lambda: Invocations vs Errors",
                    "tileType": "DQL",
                    "configured": True,
                    "bounds": {"top": 0, "left": 0, "width": 6, "height": 4},
                    "tileFilter": {},
                    "customProperties": {
                        "dql": 'fetch metrics | filter metric.key == "aws.lambda.invocations" or metric.key == "aws.lambda.errors" | summarize value = sum(value), by:{dt.entity.aws_lambda_function, metric.key} | fieldsAdd status = if(metric.key == "aws.lambda.errors", "ERROR", "TOTAL")'
                    }
                },
                {
                    "name": "API Gateway: P95 Latency",
                    "tileType": "DQL",
                    "configured": True,
                    "bounds": {"top": 0, "left": 6, "width": 6, "height": 4},
                    "tileFilter": {},
                    "customProperties": {
                        "dql": 'fetch metrics | filter metric.key == "aws.apigateway.latency" | summarize p95 = percentile(value, 95), by:{dt.entity.aws_api_gateway}'
                    }
                },
                {
                    "name": "Top Failing Lambda Functions (Root Cause)",
                    "tileType": "DQL",
                    "configured": True,
                    "bounds": {"top": 4, "left": 0, "width": 12, "height": 4},
                    "tileFilter": {},
                    "customProperties": {
                        "dql": 'fetch events | filter event.type == "ERROR_EVENT" and dt.entity.aws_lambda_function != "" | summarize count = count(), by:{dt.entity.aws_lambda_function} | sort count desc'
                    }
                }
            ]
        }

        print("🚀 Creating DQL-Powered Serverless Dashboard...")
        response = requests.post(url, headers=self.headers, json=dashboard_json)
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Dashboard Successfully Created!")
            print(f"ID: {data.get('id')}")
            print(f"URL: {self.base_url}/#dashboard;id={data.get('id')}")
        else:
            print(f"❌ Failed to create dashboard: {response.status_code} - {response.text}")

if __name__ == "__main__":
    TENANT = os.environ.get('DT_TENANT_URL')
    TOKEN = os.environ.get('DT_API_TOKEN')

    if not TENANT or not TOKEN:
        print("ERROR: Please set DT_TENANT_URL and DT_API_TOKEN environment variables.")
        exit(1)

    builder = ServerlessDashboardBuilder(TENANT, TOKEN)
    builder.create_dashboard()
