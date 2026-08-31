"""Schema Drift Detector Transformer."""
from typing import Any, Dict, List, Tuple
from transformers.base import BaseTransformer

class SchemaDriftDetector(BaseTransformer):
    def __init__(self, expected_schema: Dict[str, str]):
        self.expected_schema = expected_schema

    async def transform(self, data: Any) -> Any:
        if isinstance(data, list) and data:
            sample = data[0]
            drifted_fields = set(sample.keys()) - set(self.expected_schema.keys())
            for item in data:
                item["_schema_drift"] = list(drifted_fields)
        return data
