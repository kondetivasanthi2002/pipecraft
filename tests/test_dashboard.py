import pytest
from telemetry.dashboard import TelemetryDashboardGenerator

def test_dashboard_generator():
    dash = TelemetryDashboardGenerator.generate_grafana_dashboard_json()
    assert dash["title"] == "PipeCraft Engine Metrics"
