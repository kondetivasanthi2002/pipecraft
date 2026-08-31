import pytest
import asyncio
from core.context import ExecutionContext

@pytest.fixture
def execution_context():
    return ExecutionContext("test_pipeline", "run_123")
