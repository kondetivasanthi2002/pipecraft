import pytest
from core.batch_optimizer import BatchChunkOptimizer

def test_batch_chunking():
    opt = BatchChunkOptimizer(chunk_size=2)
    chunks = opt.optimize_chunks([{"id": 1}, {"id": 2}, {"id": 3}])
    assert len(chunks) == 2
