import asyncio
import time
import json
from config.settings import settings
from config.schema_validator import ConfigSchemaValidator
from core.context import ExecutionContext
from core.state import SQLiteStateStore
from connectors.storage import LocalFileConnector
from connectors.relational import SQLiteConnector
from transformers.schema import SchemaEnforcerTransformer
from transformers.cleaner import DataCleanerTransformer
from transformers.security import PIIMaskerTransformer
from transformers.aggregator import GroupByAggregatorTransformer
from telemetry.health import HealthMonitor

async def main():
    print("==================================================")
    print("PIPECRAFT DATA PIPELINE ENGINE DEMO RUN")
    print("==================================================")
    
    health = HealthMonitor.get_system_health()
    print(f"--> System Health: Status={health['status']} | App={settings.system.app_name}")

    valid, errors = ConfigSchemaValidator.validate_dict(settings.model_dump())
    print(f"--> Configuration Validation: {'PASS' if valid else 'FAIL'}")

    ctx = ExecutionContext(pipeline_id="demo_pipeline_001", run_id="run_20260831")
    state_store = SQLiteStateStore("./var/pipecraft_state.db")
    state_store.save_state("demo_run", {"status": "STARTING", "timestamp": time.time()})
    print(f"--> Initialized ExecutionContext & SQLite State Store")

    raw_data = [
        {"order_id": 1001, "customer_name": "  Alice Smith  ", "email": "alice@example.com", "category": "electronics", "amount": 250.50},
        {"order_id": 1002, "customer_name": "  Bob Jones  ", "email": "bob@domain.org", "category": "electronics", "amount": 150.00},
        {"order_id": 1003, "customer_name": "  Charlie Brown  ", "email": "charlie@company.com", "category": "books", "amount": 45.99},
        {"order_id": 1004, "customer_name": "  Diana Prince  ", "email": "diana@hero.com", "category": "books", "amount": 89.95},
        {"order_id": 1005, "customer_name": "  Edward Nigma  ", "email": "edward@gotham.com", "category": "electronics", "amount": 599.99}
    ]
    print(f"--> Ingested Raw Dataset: {len(raw_data)} records")

    cleaner = DataCleanerTransformer(trim_strings=True)
    cleaned_data = await cleaner.transform(raw_data)
    print(f"--> Applied DataCleanerTransformer: Trimmed customer names")

    masker = PIIMaskerTransformer(fields_to_mask=["email"])
    masked_data = await masker.transform(cleaned_data)
    print(f"--> Applied PIIMaskerTransformer: Masked emails")
    for r in masked_data[:2]:
        print(f"    Record #{r['order_id']}: Name='{r['customer_name']}', Email='{r['email']}'")

    aggregator = GroupByAggregatorTransformer(group_by_field="category", agg_field="amount", agg_fn="sum")
    aggregated_data = await aggregator.transform(masked_data)
    print(f"--> Applied GroupByAggregatorTransformer: Total spending per category:")
    for agg in aggregated_data:
        print(f"    Category '{agg['category']}': Total Amount = ${agg['amount_sum']:.2f}")

    db_conn = SQLiteConnector(db_path="./var/output_orders.db", table_name="processed_orders")
    await db_conn.write(masked_data)
    
    file_conn = LocalFileConnector(filepath="./var/category_aggregates.json", mode="w", format_type="json")
    await file_conn.write(aggregated_data)
    print(f"--> Saved output to SQLite DB ('./var/output_orders.db') and JSON ('./var/category_aggregates.json')")

    ctx.increment_metric("records_processed", len(raw_data))
    state_store.save_state("demo_run", {"status": "SUCCESS", "elapsed_seconds": ctx.get_elapsed_time()})

    print("==================================================")
    print(f"[SUCCESS] PIPELINE RUN COMPLETED SUCCESSFULLY in {ctx.get_elapsed_time():.3f}s")
    print(f"          Total Records Processed: {ctx.metrics['records_processed']}")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(main())
