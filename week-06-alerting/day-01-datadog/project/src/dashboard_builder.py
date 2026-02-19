"""
The Noise Canceller: Dashboard as Code
This script generates a 'Triage Center' Dashboard in Datadog.
It provides a single pane of glass for monitoring anomalies and correlated events.
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.model.dashboard import Dashboard
from datadog_api_client.v1.model.dashboard_layout_type import DashboardLayoutType
from datadog_api_client.v1.model.widget import Widget
from datadog_api_client.v1.model.timeseries_widget_definition import TimeseriesWidgetDefinition
from datadog_api_client.v1.model.timeseries_widget_request import TimeseriesWidgetRequest
from datadog_api_client.v1.model.widget_display_type import WidgetDisplayType
from datadog_api_client.v1.model.event_stream_widget_definition import EventStreamWidgetDefinition
from datadog_api_client.v1.model.widget_text_align import WidgetTextAlign
import os

def build_triage_dashboard():
    configuration = Configuration()
    
    with ApiClient(configuration) as api_client:
        api_instance = DashboardsApi(api_client)
        
        # 1. Define Widgets
        widgets = [
            # CPU Anomaly Widget
            Widget(
                definition=TimeseriesWidgetDefinition(
                    title="Real-time CPU Anomalies (ML Powered)",
                    show_legend=True,
                    requests=[
                        TimeseriesWidgetRequest(
                            q="avg:system.cpu.idle{service:checkout}",
                            display_type=WidgetDisplayType.LINE,
                        )
                    ]
                ),
                layout={"x": 0, "y": 0, "width": 6, "height": 4}
            ),
            # Event Cloud Widget
            Widget(
                definition=EventStreamWidgetDefinition(
                    title="Correlated Incident Feed",
                    query="project:noise-canceller",
                    event_size="small"
                ),
                layout={"x": 6, "y": 0, "width": 6, "height": 4}
            )
        ]

        # 2. Build Dashboard Object
        body = Dashboard(
            title="[AIOps] The Noise Canceller Triage Center",
            description="Autonomous Alerting and Event Correlation Dashboard",
            widgets=widgets,
            layout_type=DashboardLayoutType.FREE,
            template_variables=[]
        )

        try:
            response = api_instance.create_dashboard(body)
            print(f"✅ Dashboard Created!")
            print(f"URL: https://app.datadoghq.com/dashboard/{response.id}")
        except Exception as e:
            print(f"Error creating dashboard: {e}")

if __name__ == "__main__":
    if not os.environ.get('DD_API_KEY') or not os.environ.get('DD_APP_KEY'):
        print("ERROR: Please set DD_API_KEY and DD_APP_KEY env variables.")
    else:
        build_triage_dashboard()
