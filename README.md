# PipeCraft Enterprise Data Pipeline Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LOC 50k+](https://img.shields.io/badge/LOC-50k%2B-brightgreen.svg)]()

PipeCraft is an enterprise-grade asynchronous data pipeline and workflow execution engine designed for batch and streaming data processing.

## Architecture Overview

- **Core Async Engine**: Topological DAG sorting, concurrent node dispatcher, state checkpointing, error recovery.
- **15+ Connectors**: S3, Local File, PostgreSQL, MySQL, SQLite, MongoDB, Cassandra, Redis, Kafka, RabbitMQ, REST, GraphQL, SFTP, Webhooks.
- **Enterprise Data Transformers**: Schema Enforcer, Sanitizer, Aggregator, Encoder, PII Masker, In-memory SQL engine.
- **Workflow Schedulers**: Cron expressions, priority queues, distributed worker pool, SLA monitors.
- **Observability**: Prometheus metrics exporter, structured log correlation, distributed OpenTelemetry tracing.
- **FastAPI Control Plane**: REST endpoints, WebSocket live state, CLI runner (`pipecraft`).
- **Test Suite**: 5+ PyTest test modules covering DAG, connectors, transformers, scheduler, and end-to-end processing.
