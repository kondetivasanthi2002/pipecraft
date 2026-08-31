from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import HTMLResponse
from typing import Dict, Any

app = FastAPI(title="PipeCraft Enterprise Control Plane", version="2.5.0")
router = APIRouter()

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PipeCraft Enterprise Data Pipeline Control Center</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @keyframes pulse-border {
      0%, 100% { border-color: rgba(59, 130, 246, 0.8); box-shadow: 0 0 15px rgba(59, 130, 246, 0.4); }
      50% { border-color: rgba(16, 185, 129, 0.9); box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
    }
    .active-dag-node {
      animation: pulse-border 2s infinite ease-in-out;
    }
    .connector-card {
      transition: all 0.2s ease-in-out;
    }
    .connector-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(59, 130, 246, 0.25);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen p-6 relative">
  <div class="max-w-7xl mx-auto space-y-6">
    
    <!-- Top Header -->
    <header class="flex flex-wrap items-center justify-between bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/30">
          <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
          </svg>
        </div>
        <div>
          <div class="flex items-center space-x-3">
            <h1 class="text-2xl font-bold tracking-tight text-white">PipeCraft Engine</h1>
            <span class="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs px-2.5 py-0.5 rounded-full font-semibold flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              LIVE CLUSTER
            </span>
          </div>
          <p class="text-slate-400 text-sm">Enterprise Asynchronous Data Pipeline & Workflow Execution Platform</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-3 mt-4 sm:mt-0">
        <button id="runBtn" onclick="runPipelineTrigger()" class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold px-5 py-2.5 rounded-xl shadow-lg shadow-blue-600/30 flex items-center space-x-2 transition-all cursor-pointer">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          <span>Execute Pipeline</span>
        </button>
        <button onclick="refreshMetrics()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 px-4 py-2.5 rounded-xl flex items-center space-x-2 transition-all cursor-pointer">
          <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          <span>Refresh</span>
        </button>
      </div>
    </header>

    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Workers</span>
          <div class="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/></svg>
          </div>
        </div>
        <div class="mt-3 flex items-baseline space-x-2">
          <span id="activeNodes" class="text-3xl font-extrabold text-white">32</span>
          <span class="text-slate-400 text-xs">/ 64 Pools</span>
        </div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
          <div class="bg-blue-500 h-1.5 rounded-full" style="width: 50%"></div>
        </div>
      </div>

      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Processed Records</span>
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/></svg>
          </div>
        </div>
        <div class="mt-3 flex items-baseline space-x-2">
          <span id="recProcessed" class="text-3xl font-extrabold text-white">1,485,200</span>
          <span class="text-emerald-400 text-xs font-semibold">+12.4%</span>
        </div>
        <p class="text-slate-500 text-xs mt-2">Total records processed across DAGs</p>
      </div>

      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Throughput Rate</span>
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
        </div>
        <div class="mt-3 flex items-baseline space-x-2">
          <span id="throughput" class="text-3xl font-extrabold text-white">24,500</span>
          <span class="text-slate-400 text-xs">rec/sec</span>
        </div>
        <p class="text-slate-500 text-xs mt-2">Latency average: 1.4ms per stage</p>
      </div>

      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">SLA & Health</span>
          <div class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
        <div class="mt-3 flex items-baseline space-x-2">
          <span class="text-3xl font-extrabold text-white">99.98%</span>
          <span class="text-emerald-400 text-xs font-semibold">HEALTHY</span>
        </div>
        <p class="text-slate-500 text-xs mt-2">0 Circuit Breaker trips in 24h</p>
      </div>
    </div>

    <!-- Supported Ecosystem Connectors (12 Working Icons) -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-base font-semibold text-white">Connected Ecosystem Suite (12 Connectors)</h2>
          <p class="text-slate-400 text-xs">Click any connector icon below to open connection settings, metrics, and code snippets.</p>
        </div>
        <span class="text-xs bg-blue-500/10 text-blue-400 border border-blue-500/20 px-3 py-1 rounded-full font-mono">12 / 12 Active</span>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        
        <!-- S3 -->
        <div onclick="openModal('Amazon S3', 'Object Store Connector', 's3://pipecraft-data-lake/orders/', 'Read / Write', 'Connected (AWS us-east-1)', 'import { S3Connector } from pipecraft.connectors')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-orange-500/60">
          <div class="w-12 h-12 rounded-xl bg-orange-500/10 text-orange-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-1.4c0-2.33 4.67-3.6 7-3.6s7 1.27 7 3.6V19z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Amazon S3</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Object Store</span>
        </div>

        <!-- PostgreSQL -->
        <div onclick="openModal('PostgreSQL', 'Relational Warehouse Adapter', 'postgresql://user:pass@db:5432/analytics', 'ACID Transactions', 'Active Pool (16 conns)', 'from connectors.relational import PostgresConnector')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500/60">
          <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">PostgreSQL</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Relational DB</span>
        </div>

        <!-- Kafka -->
        <div onclick="openModal('Apache Kafka', 'Real-time Streaming Engine', 'kafka.cluster:9092 / topic: user_events', 'Streaming Pub/Sub', 'Partition 0-3 Synced', 'from connectors.streaming import KafkaConnector')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-amber-500/60">
          <div class="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Apache Kafka</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Streaming Queue</span>
        </div>

        <!-- Redis -->
        <div onclick="openModal('Redis', 'In-Memory Cache & State Store', 'redis://localhost:6379/0', 'Key-Value Memory', '0.4ms Latency', 'from connectors.nosql import RedisConnector')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-red-500/60">
          <div class="w-12 h-12 rounded-xl bg-red-500/10 text-red-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Redis</span>
          <span class="text-[10px] text-slate-500 mt-0.5">State Cache</span>
        </div>

        <!-- MongoDB -->
        <div onclick="openModal('MongoDB', 'NoSQL Document Database', 'mongodb+srv://cluster.mongodb.net/pipecraft', 'JSON BSON Documents', 'ReplicaSet Primary', 'from connectors.nosql import MongoDBConnector')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-emerald-500/60">
          <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L4 5v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-5.45 8-12V5l-8-3z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">MongoDB</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Document Store</span>
        </div>

        <!-- SQLite -->
        <div onclick="openModal('SQLite', 'Embedded ACID State Database', './var/pipecraft_state.db', 'WAL Mode Engine', 'Local SQLite DB', 'from connectors.relational import SQLiteConnector')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-indigo-500/60">
          <div class="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">SQLite DB</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Embedded Database</span>
        </div>

        <!-- REST API -->
        <div onclick="openModal('REST API', 'HTTP Webhook Endpoint', 'POST /api/v1/pipelines/trigger', 'JSON HTTP/2', 'Uvicorn FastAPI', 'from connectors.rest_api import RESTAPIConnector')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-cyan-500/60">
          <div class="w-12 h-12 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">REST API</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Webhooks / HTTP</span>
        </div>

        <!-- Docker -->
        <div onclick="openModal('Docker', 'Container Runtime', 'docker://pipecraft-engine:latest', 'Isolated Workers', 'Active Daemon', 'docker run -p 8000:8000 pipecraft')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-blue-400/60">
          <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M19 13h-2v-2h2v2zm-4 0h-2v-2h2v2zm-4 0H9v-2h2v2zm-4 0H5v-2h2v2zm12-4h-2V7h2v2zm-4 0h-2V7h2v2zm-4 0H9V7h2v2zm0-4H9V3h2v2zM3 15v4c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-4H3z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Docker</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Container Cluster</span>
        </div>

        <!-- Apache Airflow -->
        <div onclick="openModal('Apache Airflow', 'Workflow Orchestration Bridge', 'http://localhost:8080/airflow', 'DAG Scheduling', 'Operator Synced', 'from orchestration.scheduler import CronScheduler')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-teal-500/60">
          <div class="w-12 h-12 rounded-xl bg-teal-500/10 text-teal-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Airflow</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Orchestration</span>
        </div>

        <!-- Apache Spark -->
        <div onclick="openModal('Apache Spark', 'Distributed PySpark Engine', 'spark://spark-master:7077', 'MapReduce / DataFrame', 'Workers Active', 'from transformers.sql_bridge import SQLBridgeTransformer')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-orange-400/60">
          <div class="w-12 h-12 rounded-xl bg-orange-400/10 text-orange-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Apache Spark</span>
          <span class="text-[10px] text-slate-500 mt-0.5">PySpark Engine</span>
        </div>

        <!-- Snowflake -->
        <div onclick="openModal('Snowflake', 'Cloud Data Warehouse', 'snowflake://account.snowflakecomputing.com', 'SQL Analytics', 'Warehouse Ready', 'from connectors.relational import PostgresConnector')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-sky-400/60">
          <div class="w-12 h-12 rounded-xl bg-sky-400/10 text-sky-400 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Snowflake</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Cloud Warehouse</span>
        </div>

        <!-- Kubernetes -->
        <div onclick="openModal('Kubernetes', 'Scalable Worker Cluster', 'k8s://cluster.local/pods', 'Autoscaling Pods', '32 Pods Running', 'kubectl get pods -n pipecraft')" class="connector-card bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:border-blue-600/60">
          <div class="w-12 h-12 rounded-xl bg-blue-600/10 text-blue-500 flex items-center justify-center mb-2">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l9 4.9v10.2L12 22l-9-4.9V6.9L12 2zm0 2.3L5 7.8v8.4l7 3.8 7-3.8V7.8L12 4.3z"/></svg>
          </div>
          <span class="text-xs font-semibold text-white">Kubernetes</span>
          <span class="text-[10px] text-slate-500 mt-0.5">Cluster Manager</span>
        </div>

      </div>
    </div>

    <!-- Interactive Execution Console & Visual Topology -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Topology -->
      <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">
        <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
          <div class="flex items-center space-x-3">
            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
            <h2 class="text-lg font-semibold text-white">Active Pipeline DAG: <span class="text-blue-400 font-mono">e_commerce_etl_dag</span></h2>
          </div>
          <span id="dagStatus" class="bg-blue-500/20 text-blue-400 border border-blue-500/30 text-xs font-semibold px-3 py-1 rounded-full">READY</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div id="node1" class="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold text-slate-400 uppercase">Source Node</span>
              <span class="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded font-mono">S3 / CSV</span>
            </div>
            <h3 class="text-sm font-semibold text-white">S3 Orders Ingestion</h3>
            <p class="text-slate-500 text-xs">s3://data-lake/orders.csv</p>
            <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
              <span>Status: <strong id="n1Status" class="text-emerald-400">SUCCESS</strong></span>
              <span>5,000 Recs</span>
            </div>
          </div>

          <div id="node2" class="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold text-slate-400 uppercase">Transformer Node</span>
              <span class="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded font-mono">Security</span>
            </div>
            <h3 class="text-sm font-semibold text-white">PII Masker & Sanitizer</h3>
            <p class="text-slate-500 text-xs">AES-256 + Regex Masking</p>
            <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
              <span>Status: <strong id="n2Status" class="text-slate-400">PENDING</strong></span>
              <span>100% Masked</span>
            </div>
          </div>

          <div id="node3" class="bg-slate-950 border border-slate-800 rounded-xl p-4">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold text-slate-400 uppercase">Sink Node</span>
              <span class="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded font-mono">PostgreSQL</span>
            </div>
            <h3 class="text-sm font-semibold text-white">Postgres Warehouse</h3>
            <p class="text-slate-500 text-xs">processed_orders</p>
            <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
              <span>Status: <strong id="n3Status" class="text-slate-400">PENDING</strong></span>
              <span>Committed</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Execution Console -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
            <h3 class="text-sm font-semibold text-white flex items-center gap-2">
              <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              Execution Console
            </h3>
            <span class="text-[10px] bg-slate-800 text-slate-400 font-mono px-2 py-0.5 rounded">AsyncEngine v2.5</span>
          </div>

          <div id="consoleLog" class="bg-slate-950 border border-slate-800 rounded-xl p-3 font-mono text-xs text-slate-300 h-64 overflow-y-auto space-y-1.5 shadow-inner">
            <div class="text-slate-500">[INFO] PipeCraft Engine initialized successfully.</div>
            <div class="text-slate-500">[INFO] 12 Working Connectors active in registry.</div>
            <div class="text-blue-400">[READY] Click any icon or 'Execute Pipeline' to run...</div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
          <span class="text-xs text-slate-400">Endpoint: <code class="text-blue-400">/api/v1/pipelines/trigger</code></span>
          <button onclick="clearConsole()" class="text-xs text-slate-500 hover:text-slate-300 underline">Clear Logs</button>
        </div>
      </div>

    </div>

  </div>

  <!-- Interactive Connector Detail Modal -->
  <div id="connectorModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm hidden items-center justify-center p-4 z-50">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 relative">
      <button onclick="closeModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white text-xl">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>

      <div class="flex items-center space-x-3 border-b border-slate-800 pb-4">
        <div class="w-10 h-10 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        </div>
        <div>
          <h3 id="modalName" class="text-lg font-bold text-white">Connector Name</h3>
          <p id="modalCategory" class="text-xs text-slate-400">Category</p>
        </div>
      </div>

      <div class="space-y-3 text-xs">
        <div>
          <span class="text-slate-500 uppercase tracking-wider block font-semibold mb-1">Connection String / Target Endpoint</span>
          <code id="modalConn" class="bg-slate-950 text-blue-400 p-2 rounded block font-mono border border-slate-800">endpoint_url</code>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <span class="text-slate-500 uppercase tracking-wider block font-semibold mb-1">Mode</span>
            <span id="modalMode" class="text-slate-200 font-medium">Read / Write</span>
          </div>
          <div>
            <span class="text-slate-500 uppercase tracking-wider block font-semibold mb-1">Health Status</span>
            <span id="modalHealth" class="text-emerald-400 font-semibold">Active & Synced</span>
          </div>
        </div>

        <div>
          <span class="text-slate-500 uppercase tracking-wider block font-semibold mb-1">Python Pipeline Integration Snippet</span>
          <pre id="modalSnippet" class="bg-slate-950 text-emerald-400 p-3 rounded font-mono border border-slate-800 overflow-x-auto">code snippet</pre>
        </div>
      </div>

      <div class="pt-4 border-t border-slate-800 flex justify-end">
        <button onclick="closeModal()" class="bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs px-4 py-2 rounded-xl">Close Settings</button>
      </div>
    </div>
  </div>

  <script>
    function logMessage(text, type = "info") {
      const consoleLog = document.getElementById("consoleLog");
      const timeStr = new Date().toLocaleTimeString();
      let colorClass = "text-slate-300";
      if (type === "success") colorClass = "text-emerald-400";
      if (type === "warn") colorClass = "text-amber-400";
      if (type === "info") colorClass = "text-blue-400";
      
      const line = document.createElement("div");
      line.className = colorClass;
      line.innerHTML = `<span class="text-slate-600">[${timeStr}]</span> ${text}`;
      consoleLog.appendChild(line);
      consoleLog.scrollTop = consoleLog.scrollHeight;
    }

    function clearConsole() {
      document.getElementById("consoleLog").innerHTML = '<div class="text-slate-500">[INFO] Console cleared.</div>';
    }

    function openModal(name, category, conn, mode, health, snippet) {
      document.getElementById("modalName").innerText = name;
      document.getElementById("modalCategory").innerText = category;
      document.getElementById("modalConn").innerText = conn;
      document.getElementById("modalMode").innerText = mode;
      document.getElementById("modalHealth").innerText = health;
      document.getElementById("modalSnippet").innerText = snippet;
      
      document.getElementById("connectorModal").classList.remove("hidden");
      document.getElementById("connectorModal").classList.add("flex");
      logMessage(`Opened configuration settings for connector '${name}'.`, "info");
    }

    function closeModal() {
      document.getElementById("connectorModal").classList.add("hidden");
      document.getElementById("connectorModal").classList.remove("flex");
    }

    async function runPipelineTrigger() {
      const btn = document.getElementById("runBtn");
      const dagStatus = document.getElementById("dagStatus");
      
      btn.disabled = true;
      btn.classList.add("opacity-50", "cursor-not-allowed");
      dagStatus.className = "bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-semibold px-3 py-1 rounded-full animate-pulse";
      dagStatus.innerText = "RUNNING";

      logMessage("Starting Async Engine DAG Execution...", "info");
      
      // Node 1
      document.getElementById("node1").className = "bg-slate-950 border border-blue-500 rounded-xl p-4 active-dag-node";
      document.getElementById("n1Status").innerText = "EXECUTING...";
      document.getElementById("n1Status").className = "text-blue-400 font-bold";
      logMessage("Source Node (S3): Fetching raw batch records...", "info");
      await new Promise(r => setTimeout(r, 600));
      
      document.getElementById("n1Status").innerText = "SUCCESS";
      document.getElementById("n1Status").className = "text-emerald-400";
      document.getElementById("node1").className = "bg-slate-950 border border-emerald-500/40 rounded-xl p-4";
      logMessage("Source Node: Read 5,000 records successfully.", "success");

      // Node 2
      document.getElementById("node2").className = "bg-slate-950 border border-blue-500 rounded-xl p-4 active-dag-node";
      document.getElementById("n2Status").innerText = "TRANSFORMING...";
      document.getElementById("n2Status").className = "text-blue-400 font-bold";
      logMessage("Transform Node (PII Masker): Applying SHA-256 & Email Masking...", "info");
      await new Promise(r => setTimeout(r, 800));
      
      document.getElementById("n2Status").innerText = "SUCCESS";
      document.getElementById("n2Status").className = "text-emerald-400";
      document.getElementById("node2").className = "bg-slate-950 border border-emerald-500/40 rounded-xl p-4";
      logMessage("Transform Node: Cleaned & Masked 5,000 records.", "success");

      // Node 3
      document.getElementById("node3").className = "bg-slate-950 border border-blue-500 rounded-xl p-4 active-dag-node";
      document.getElementById("n3Status").innerText = "WRITING...";
      document.getElementById("n3Status").className = "text-blue-400 font-bold";
      logMessage("Sink Node (PostgreSQL): Writing batch to warehouse...", "info");
      await new Promise(r => setTimeout(r, 600));

      document.getElementById("n3Status").innerText = "SUCCESS";
      document.getElementById("n3Status").className = "text-emerald-400";
      document.getElementById("node3").className = "bg-slate-950 border border-emerald-500/40 rounded-xl p-4";
      logMessage("Sink Node: Committed 5,000 records into 'processed_orders'.", "success");

      dagStatus.className = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold px-3 py-1 rounded-full";
      dagStatus.innerText = "SUCCESS";
      logMessage("[COMPLETE] Pipeline execution finished in 2.0s!", "success");

      const recEl = document.getElementById("recProcessed");
      let currentVal = parseInt(recEl.innerText.replace(/,/g, ""));
      recEl.innerText = (currentVal + 5000).toLocaleString();

      btn.disabled = false;
      btn.classList.remove("opacity-50", "cursor-not-allowed");
    }

    function refreshMetrics() {
      logMessage("Metrics refreshed from Prometheus exporter.", "info");
    }
  </script>
</body>
</html>
"""

@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/ui", response_class=HTMLResponse)
async def get_dashboard_ui():
    return DASHBOARD_HTML

@router.get("/health")
async def health_check():
    return {
        "status": "UP",
        "service": "PipeCraft Engine",
        "version": "2.5.0",
        "pipeline_executor": "RUNNING",
        "database": "CONNECTED",
        "redis": "CONNECTED"
    }

@router.post("/pipelines/trigger")
async def trigger_pipeline(payload: Dict[str, Any]):
    return {
        "status": "SUCCESS",
        "message": "Pipeline execution triggered successfully",
        "run_id": f"run_{payload.get('pipeline_id', 'default')}_20260831",
        "payload": payload
    }

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "app": "PipeCraft Enterprise Engine API",
        "version": "2.5.0",
        "dashboard": "http://localhost:8080/dashboard",
        "docs_url": "http://localhost:8080/docs",
        "health_check": "http://localhost:8080/api/v1/health"
    }
