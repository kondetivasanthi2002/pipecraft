import pytest
from connectors.lakehouse import ApacheIcebergConnector

@pytest.mark.asyncio
async def test_iceberg_connector():
    conn = ApacheIcebergConnector("db.table")
    data = await conn.read()
    assert len(data) == 1
