import pytest
from transformers.cleaner import DataCleanerTransformer
from transformers.security import PIIMaskerTransformer
from transformers.aggregator import GroupByAggregatorTransformer

@pytest.mark.asyncio
async def test_data_cleaner():
    cleaner = DataCleanerTransformer(trim_strings=True)
    out = await cleaner.transform([{"name": "  Alice  "}])
    assert out[0]["name"] == "Alice"

@pytest.mark.asyncio
async def test_pii_masker():
    masker = PIIMaskerTransformer(fields_to_mask=["email"])
    out = await masker.transform([{"email": "alice@example.com"}])
    assert out[0]["email"] != "alice@example.com"

@pytest.mark.asyncio
async def test_group_by_aggregator():
    agg = GroupByAggregatorTransformer(group_by_field="cat", agg_field="val", agg_fn="sum")
    out = await agg.transform([{"cat": "a", "val": 10}, {"cat": "a", "val": 20}])
    assert len(out) == 1
    assert out[0]["val_sum"] == 30.0
