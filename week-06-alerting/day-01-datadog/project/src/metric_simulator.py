"""
The Noise Canceller: Metric Simulator
This script pushes custom metrics to Datadog to simulate both 'Normal' and 'Anomalous' behavior.
It allows students to test their anomaly detection monitors without needing a live heavy-load environment.
"""

import time
import random
import os
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_series import MetricSeries
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType

def push_metrics(is_anomaly=False):
    configuration = Configuration()
    
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        
        # 1. Generate Data
        # Base CPU around 30%
        value = 30.0 + random.uniform(-5.0, 5.0)
        
        if is_anomaly:
            print("🚀 SIMULATING ANOMALY: Spiking CPU to 95%...")
            value = 95.0 + random.uniform(-2.0, 2.0)
        else:
            print(f"✅ Normal behavior: CPU at {value:.2f}%")

        # 2. Build Payload
        series = [
            MetricSeries(
                metric="aiops.simulator.cpu_usage",
                type=MetricIntakeType.GAUGE,
                points=[
                    MetricPoint(
                        timestamp=int(time.time()),
                        value=value,
                    ),
                ],
                tags=["env:prod", "service:checkout", "simulator:true"],
            )
        ]
        
        body = MetricPayload(series=series)

        try:
            api_instance.submit_metrics(body=body)
        except Exception as e:
            print(f"Error submitting metrics: {e}")

if __name__ == "__main__":
    if not os.environ.get('DD_API_KEY'):
        print("ERROR: Please set DD_API_KEY environment variable.")
        exit(1)

    print("Starting Metric Simulator. Press Ctrl+C to stop.")
    try:
        count = 0
        while True:
            # Every 10 steps, create an anomaly
            trigger_anomaly = (count % 10 == 0 and count != 0)
            push_metrics(is_anomaly=trigger_anomaly)
            
            count += 1
            time.sleep(15) # Pulse every 15 seconds
    except KeyboardInterrupt:
        print("\nSimulator stopped.")
