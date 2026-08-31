import pytest
from orchestration.autoscaler import WorkerAutoScaler

def test_autoscaler_scale_up():
    scaler = WorkerAutoScaler(min_workers=2, max_workers=16)
    workers = scaler.calculate_required_workers(queue_depth=150, current_workers=4)
    assert workers == 8
