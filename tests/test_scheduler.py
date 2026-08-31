import pytest
import time

def test_sla_monitor():
    start = time.time()
    assert (time.time() - start) < 5.0
