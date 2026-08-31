import pytest
from transformers.drift_detector import SchemaDriftDetector

@pytest.mark.asyncio
async def test_schema_drift():
    detector = SchemaDriftDetector({"id": "int"})
    res = await detector.transform([{"id": 1, "new_col": "val"}])
    assert "new_col" in res[0]["_schema_drift"]
