import pytest
import os
from connectors.storage import LocalFileConnector
from transformers.cleaner import DataCleanerTransformer
from transformers.security import PIIMaskerTransformer

@pytest.mark.asyncio
async def test_full_e2e_pipeline_flow(tmp_path):
    out_file = str(tmp_path / "out.json")
    cleaner = DataCleanerTransformer(trim_strings=True)
    masker = PIIMaskerTransformer(fields_to_mask=["email"])
    file_conn = LocalFileConnector(out_file, mode="w", format_type="json")

    raw = [{"name": "  Bob  ", "email": "bob@test.com"}]
    cleaned = await cleaner.transform(raw)
    masked = await masker.transform(cleaned)
    saved = await file_conn.write(masked)

    assert saved is True
    assert os.path.exists(out_file)
