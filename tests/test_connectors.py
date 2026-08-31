import pytest
import os
from connectors.storage import LocalFileConnector
from connectors.relational import SQLiteConnector

@pytest.mark.asyncio
async def test_local_file_connector(tmp_path):
    fp = str(tmp_path / "data.json")
    conn = LocalFileConnector(fp, mode="w", format_type="json")
    res = await conn.write([{"id": 1}])
    assert res is True
    assert os.path.exists(fp)

@pytest.mark.asyncio
async def test_sqlite_connector(tmp_path):
    db_file = str(tmp_path / "test.db")
    conn = SQLiteConnector(db_file, table_name="users")
    written = await conn.write([{"id": 1, "username": "alice"}])
    assert written is True
    assert os.path.exists(db_file)
