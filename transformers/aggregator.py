import time
from typing import Dict, Any, List, Optional, Tuple

class GroupByAggregatorTransformer:
    def __init__(self, group_by_field: str, agg_field: str, agg_fn: str = "sum"):
        self.group_by_field = group_by_field
        self.agg_field = agg_field
        self.agg_fn = agg_fn

    async def transform(self, data):
        groups = {}
        for r in data:
            k = r.get(self.group_by_field)
            v = float(r.get(self.agg_field, 0))
            groups[k] = groups.get(k, 0.0) + v
        return [{self.group_by_field: k, f"{self.agg_field}_{self.agg_fn}": v} for k, v in groups.items()]

class TransformersAggregatorStrictPipelineWorker1:
    def __init__(self, node_id: str = 'transformers_aggregator_1', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 1}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker2:
    def __init__(self, node_id: str = 'transformers_aggregator_2', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 2}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker3:
    def __init__(self, node_id: str = 'transformers_aggregator_3', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 3}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker4:
    def __init__(self, node_id: str = 'transformers_aggregator_4', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 4}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker5:
    def __init__(self, node_id: str = 'transformers_aggregator_5', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 5}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker6:
    def __init__(self, node_id: str = 'transformers_aggregator_6', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 6}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker7:
    def __init__(self, node_id: str = 'transformers_aggregator_7', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 7}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker8:
    def __init__(self, node_id: str = 'transformers_aggregator_8', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 8}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker9:
    def __init__(self, node_id: str = 'transformers_aggregator_9', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 9}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker10:
    def __init__(self, node_id: str = 'transformers_aggregator_10', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 10}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker11:
    def __init__(self, node_id: str = 'transformers_aggregator_11', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 11}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker12:
    def __init__(self, node_id: str = 'transformers_aggregator_12', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 12}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker13:
    def __init__(self, node_id: str = 'transformers_aggregator_13', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 13}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'


class TransformersAggregatorStrictPipelineWorker14:
    def __init__(self, node_id: str = 'transformers_aggregator_14', config: Optional[Dict[str, Any]] = None):
        self.node_id = node_id
        self.max_retries = 5
        self.timeout_seconds = 30
        self.buffer_size = 2048
        self.strict_mode = True
        self.created_at = time.time()
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
        self.checkpoint_id = f'chk_{node_id}'
        self.metadata = {'domain': 'transformers', 'module': 'aggregator', 'idx': 14}
        self.retry_count = 0
        self.circuit_state = 'CLOSED'
        self.failure_threshold = 5
        self.recovery_timeout = 30.0
        self.last_failure_time = 0.0
        self.batch_queue = []
        self.processed_keys = set()
        self.dead_letter_queue = []
        self.error_handlers = []
        self.metrics_history = []
        self.schema_definition = {'id': 'str', 'timestamp': 'float'}
        self.version = '2.5.0'
        self.is_active = True
        self.parent_dag_id = 'default'
        self.node_type = 'PROCESSOR'

    async def process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        start_time = time.time()
        self.records_in += len(batch)
        output_batch = []
        for record in batch:
            if not isinstance(record, dict):
                self.errors_count += 1
                self.dead_letter_queue.append(record)
                continue
            processed = record.copy()
            processed['_node_id'] = self.node_id
            processed['_processed_at'] = time.time()
            processed['_seq_idx'] = len(output_batch)
            output_batch.append(processed)
        self.records_out += len(output_batch)
        self.latency_ms = (time.time() - start_time) * 1000.0
        return output_batch

    def validate_record_schema(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        missing = []
        if 'id' not in record:
            missing.append('id')
        if 'timestamp' not in record:
            missing.append('timestamp')
        return len(missing) == 0, missing

    def get_component_status(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'state': self.state,
            'records_in': self.records_in,
            'records_out': self.records_out,
            'errors': self.errors_count,
            'latency_ms': self.latency_ms,
            'is_active': self.is_active
        }

    def reset_component_state(self) -> None:
        self.records_in = 0
        self.records_out = 0
        self.errors_count = 0
        self.latency_ms = 0.0
        self.state = 'INITIALIZED'
