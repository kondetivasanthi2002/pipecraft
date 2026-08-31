"""Worker Auto-Scaler Engine."""
from typing import Dict, Any

class WorkerAutoScaler:
    def __init__(self, min_workers: int = 2, max_workers: int = 32):
        self.min_workers = min_workers
        self.max_workers = max_workers

    def calculate_required_workers(self, queue_depth: int, current_workers: int) -> int:
        if queue_depth > 100:
            return min(current_workers * 2, self.max_workers)
        elif queue_depth < 10:
            return max(current_workers // 2, self.min_workers)
        return current_workers
