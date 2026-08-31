import pytest
import asyncio
from core.context import ExecutionContext

@pytest.mark.asyncio
async def test_execution_context_metrics():
    ctx = ExecutionContext("p1", "r1")
    ctx.increment_metric("records_processed", 100)
    assert ctx.metrics["records_processed"] == 100
