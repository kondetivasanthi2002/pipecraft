# PipeCraft Enterprise Data Pipeline Engine

PipeCraft is a production-grade, asynchronous data pipeline and workflow execution engine designed for high-throughput batch and streaming data engineering workloads.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Build](#build)
- [Run & Usage](#run--usage)
- [Testing](#testing)
- [API Documentation](#api-documentation)

## Overview
PipeCraft provides a modular, scalable framework for building Directed Acyclic Graph (DAG) pipelines, enforcing schemas, masking sensitive PII data, aggregating metrics, and exporting telemetry to Prometheus and OpenTelemetry.

## Architecture
- **Core Async Engine**: Topological DAG sorting, concurrent node dispatcher, state checkpointing, error recovery.
- **15+ Ecosystem Connectors**: S3, Local File, PostgreSQL, MySQL, SQLite, MongoDB, Cassandra, Redis, Kafka, RabbitMQ, REST API, GraphQL, SFTP, Webhooks, Lakehouse.
- **Enterprise Data Transformers**: Schema Enforcer, Sanitizer, GroupBy Aggregator, Categorical Encoder, PII Masker, DuckDB/SQLite SQL Bridge.
- **Workflow Schedulers**: Cron expressions, priority queues, distributed worker pool, SLA monitors, worker auto-scaler.
- **Observability**: Prometheus metrics exporter, structured log correlation, distributed OpenTelemetry tracing, Grafana metrics dashboard.
- **FastAPI Control Plane**: REST endpoints, WebSocket live state stream, CLI runner (`pipecraft`).

## Dependencies
System and runtime requirements:
- **Python**: `3.9` or higher
- **Core Libraries**: `pydantic>=2.0.0`, `fastapi>=0.100.0`, `uvicorn>=0.22.0`, `pyyaml>=6.0`, `click>=8.1.0`, `prometheus-client>=0.17.0`, `httpx>=0.24.0`
- **Testing Requirements**: `pytest>=7.0.0`, `pytest-asyncio>=0.21.0`

## Installation
Follow these steps to set up the development environment and install dependencies:

```bash
# 1. Clone repository
git clone https://github.com/kondetivasanthi2002/pipecraft.git
cd pipecraft

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies from lockfile
pip install -r requirements.txt

# 5. Install PipeCraft package in editable mode
pip install -e .
```

## Build
Commands to compile, package, and build container images:

```bash
# Build Python wheel and source distribution
python setup.py build
python -m build

# Build Docker container image
docker build -t pipecraft-engine:latest .

# Run Docker container
docker run -p 8085:8085 pipecraft-engine:latest
```

## Run & Usage
Run the application using any of the available entry points:

### 1. Run Main Executable Pipeline Runner
```bash
python main.py
```

### 2. Run End-to-End Pipeline Demo
```bash
python run_pipeline_demo.py
```

### 3. Launch FastAPI Control Plane REST Server
```bash
python -m uvicorn api.server:app --host 0.0.0.0 --port 8085
```

### 4. Use PipeCraft CLI Tool
```bash
pipecraft run --config config/default_config.yaml
pipecraft version
```

## Testing
Execute automated PyTest suites covering core DAG execution, connectors, transformers, scheduler, and end-to-end processing:

```bash
# Run all test suites
pytest tests/ -v

# Run with coverage report
pytest --cov=core --cov=connectors --cov=transformers tests/
```

## API Documentation
Once the server is running on `http://localhost:8085`, access interactive documentation at:
- **Interactive Visual Dashboard**: `http://localhost:8085/dashboard`
- **Swagger UI**: `http://localhost:8085/docs`
- **ReDoc UI**: `http://localhost:8085/redoc`
- **Health Check**: `http://localhost:8085/api/v1/health`
