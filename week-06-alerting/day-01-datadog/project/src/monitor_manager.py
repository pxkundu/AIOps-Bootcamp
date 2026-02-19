"""
The Noise Canceller: Datadog Monitor Manager
This script programmatically creates an Anomaly Detection monitor in Datadog.
It is designed to ignore 'predictable' spikes and only alert on true outliers.
"""

import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds
from datadog_api_client.v1.model.monitor_type import MonitorType

def create_intelligent_monitor():
    # 1. Configuration
    configuration = Configuration()
    # These should be set in your environment variables
    # configuration.api_key['apiKeyAuth'] = os.environ.get('DD_API_KEY')
    # configuration.api_key['appKeyAuth'] = os.environ.get('DD_APP_KEY')

    with ApiClient(configuration) as api_client:
        api_instance = MonitorsApi(api_client)
        
        # 2. Define the Monitor
        # query format: avg(last_4h):anomalous(avg:aws.ec2.cpu{env:prod}, 'agile', 3, direction='both', alert_window='last_15m', interval=60, count_default_zero='true') >= 0.95
        body = Monitor(
            name="[AIOps] EC2 CPU Anomaly Detection - Prod Checkout",
            type=MonitorType.QUERY_ALERT,
            query="avg(last_4h):anomalous(avg:system.cpu.idle{service:checkout}, 'agile', 3, direction='below', alert_window='last_15m', interval=60) >= 0.8",
            message="""
                {{#is_alert}}
                🚨 **True Anomaly Detected** 🚨
                Service: {{service.name}}
                Host: {{host.name}}
                The CPU behavior is significantly different from historical seasonality. 
                Please check the @slack-ops-channel
                {{/is_alert}}
                
                {{#is_recovery}}
                ✅ Service recovered.
                {{/is_recovery}}
            """,
            tags=["team:core-reliability", "project:noise-canceller", "env:prod"],
            thresholds=MonitorThresholds(
                critical=0.8,
                critical_recovery=0.5
            )
        )

        try:
            response = api_instance.create_monitor(body)
            print(f"Successfully created monitor: {response.id}")
            print(f"View here: https://app.datadoghq.com/monitors/{response.id}")
        except Exception as e:
            print(f"Exception when calling MonitorsApi->create_monitor: {e}")

if __name__ == "__main__":
    if not os.environ.get('DD_API_KEY') or not os.environ.get('DD_APP_KEY'):
        print("ERROR: Please set DD_API_KEY and DD_APP_KEY environment variables.")
    else:
        create_intelligent_monitor()
