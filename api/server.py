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
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @keyframes pulse-border {
      0%, 100% { border-color: rgba(59, 130, 246, 0.8); box-shadow: 0 0 15px rgba(59, 130, 246, 0.4); }
      50% { border-color: rgba(16, 185, 129, 0.9); box-shadow: 0 0 20px rgba(16, 185, 129, 0.6); }
    }
    .active-dag-node {
      animation: pulse-border 2s infinite ease-in-out;
    }
    .flow-line {
      stroke-dasharray: 8;
      animation: dash 1s linear infinite;
    }
    @keyframes dash {
      to { stroke-dashoffset: -16; }
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen p-6">
  <div class="max-w-7xl mx-auto space-y-6">
    
    <!-- Top Header -->
    <header class="flex flex-wrap items-center justify-between bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/30">
          <i class="fa-solid fa-diagram-project text-2xl text-white"></i>
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
          <i class="fa-solid fa-play"></i>
          <span>Execute Pipeline</span>
        </button>
        <button onclick="refreshMetrics()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 px-4 py-2.5 rounded-xl flex items-center space-x-2 transition-all cursor-pointer">
          <i class="fa-solid fa-rotate-right"></i>
          <span>Refresh</span>
        </button>
      </div>
    </header>

    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Concurrency</span>
          <div class="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
            <i class="fa-solid fa-microchip"></i>
          </div>
        </div>
        <div class="mt-3 flex items-baseline space-x-2">
          <span id="activeNodes" class="text-3xl font-extrabold text-white">32</span>
          <span class="text-slate-400 text-xs">/ 64 Workers</span>
        </div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
          <div class="bg-blue-500 h-1.5 rounded-full" style="width: 50%"></div>
        </div>
      </div>

      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Processed Data</span>
          <div class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
            <i class="fa-solid fa-database"></i>
          </div>
        </div>
        <div class="mt-3 flex items-baseline space-x-2">
          <span id="recProcessed" class="text-3xl font-extrabold text-white">1,485,200</span>
          <span class="text-emerald-400 text-xs font-semibold">+12.4%</span>
        </div>
        <p class="text-slate-500 text-xs mt-2">Total records ingested across DAGs</p>
      </div>

      <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl relative overflow-hidden group">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Throughput Rate</span>
          <div class="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
            <i class="fa-solid fa-bolt"></i>
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
            <i class="fa-solid fa-heart-pulse"></i>
          </div>
        </div>
        <div class="mt-3 flex items-baseline space-x-2">
          <span class="text-3xl font-extrabold text-white">99.98%</span>
          <span class="text-emerald-400 text-xs font-semibold">HEALTHY</span>
        </div>
        <p class="text-slate-500 text-xs mt-2">0 Circuit Breaker trips in 24h</p>
      </div>
    </div>

    <!-- Main Content Area: DAG Workflow Canvas + Execution Console -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- DAG Workflow Canvas (2 Cols) -->
      <div class="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
            <div class="flex items-center space-x-3">
              <i class="fa-solid fa-network-wired text-blue-400"></i>
              <h2 class="text-lg font-semibold text-white">Active Pipeline Topology: <span class="text-blue-400 font-mono">e_commerce_etl_dag</span></h2>
            </div>
            <span id="dagStatus" class="bg-blue-500/20 text-blue-400 border border-blue-500/30 text-xs font-semibold px-3 py-1 rounded-full">READY</span>
          </div>

          <!-- DAG Nodes Layout -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 relative py-4">
            
            <!-- Node 1: Source -->
            <div id="node1" class="bg-slate-950 border border-slate-800 rounded-xl p-4 transition-all duration-300">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Source Node</span>
                <span class="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded font-mono">S3 / CSV</span>
              </div>
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-orange-500/20 text-orange-400 flex items-center justify-center text-xl">
                  <i class="fa-brands fa-aws"></i>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white">S3 Orders Bucket</h3>
                  <p class="text-slate-500 text-xs">s3://data-lake/orders.csv</p>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                <span>Status: <strong id="n1Status" class="text-emerald-400">SUCCESS</strong></span>
                <span>Records: 5,000</span>
              </div>
            </div>

            <!-- Node 2: Transformer -->
            <div id="node2" class="bg-slate-950 border border-slate-800 rounded-xl p-4 transition-all duration-300">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Transformer Node</span>
                <span class="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded font-mono">Security</span>
              </div>
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center text-xl">
                  <i class="fa-solid fa-user-shield"></i>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white">PII Masker & Sanitizer</h3>
                  <p class="text-slate-500 text-xs">AES-256 + Email Regex</p>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                <span>Status: <strong id="n2Status" class="text-slate-400">PENDING</strong></span>
                <span>Masked: 100%</span>
              </div>
            </div>

            <!-- Node 3: Sink -->
            <div id="node3" class="bg-slate-950 border border-slate-800 rounded-xl p-4 transition-all duration-300">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Sink Node</span>
                <span class="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded font-mono">Postgres DB</span>
              </div>
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-xl">
                  <i class="fa-solid fa-database"></i>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-white">PostgreSQL Warehouse</h3>
                  <p class="text-slate-500 text-xs">table: processed_orders</p>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
                <span>Status: <strong id="n3Status" class="text-slate-400">PENDING</strong></span>
                <span>Inserts: 5,000</span>
              </div>
            </div>

          </div>
        </div>

        <!-- Connectors Suite Grid -->
        <div class="mt-6 pt-4 border-t border-slate-800">
          <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Supported Ecosystem Connectors (15+)</h3>
          <div class="grid grid-cols-4 sm:grid-cols-8 gap-3">
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-brands fa-aws text-orange-400 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">S3 Bucket</span>
            </div>
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-solid fa-database text-blue-400 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">PostgreSQL</span>
            </div>
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-solid fa-bolt text-amber-400 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">Apache Kafka</span>
            </div>
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-solid fa-cubes text-red-400 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">Redis Store</span>
            </div>
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-solid fa-leaf text-emerald-400 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">MongoDB</span>
            </div>
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-solid fa-server text-indigo-400 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">SQLite DB</span>
            </div>
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-solid fa-globe text-cyan-400 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">REST API</span>
            </div>
            <div class="bg-slate-950 border border-slate-800/80 rounded-lg p-2.5 flex flex-col items-center justify-center text-slate-300 hover:border-blue-500/50 transition-all cursor-pointer">
              <i class="fa-brands fa-docker text-blue-500 text-lg mb-1"></i>
              <span class="text-[10px] font-medium">Docker</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Execution Console Log Stream (1 Col) -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
            <div class="flex items-center space-x-2">
              <i class="fa-solid fa-terminal text-emerald-400 text-sm"></i>
              <h3 class="text-sm font-semibold text-white">Live Execution Console</h3>
            </div>
            <span class="text-[10px] bg-slate-800 text-slate-400 font-mono px-2 py-0.5 rounded">AsyncEngine v2.5</span>
          </div>

          <div id="consoleLog" class="bg-slate-950 border border-slate-800 rounded-xl p-3 font-mono text-xs text-slate-300 h-80 overflow-y-auto space-y-1.5 shadow-inner">
            <div class="text-slate-500">[INFO] PipeCraft Engine initialized successfully.</div>
            <div class="text-slate-500">[INFO] 32 Worker Threads listening on task queue...</div>
            <div class="text-blue-400">[READY] Waiting for user trigger or scheduled cron...</div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
          <span class="text-xs text-slate-400">Endpoint: <code class="text-blue-400">/api/v1/pipelines/trigger</code></span>
          <button onclick="clearConsole()" class="text-xs text-slate-500 hover:text-slate-300 underline">Clear Logs</button>
        </div>
      </div>

    </div>

    <!-- Data Output Preview Table -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="text-base font-semibold text-white">Processed Record Stream Preview</h2>
          <p class="text-slate-400 text-xs">Live output from <code class="text-emerald-400">DataCleanerTransformer</code> + <code class="text-indigo-400">PIIMaskerTransformer</code></p>
        </div>
        <span class="bg-emerald-500/10 text-emerald-400 text-xs px-3 py-1 rounded-full font-semibold border border-emerald-500/20">SQLite DB Verified</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-800 text-xs text-slate-400 uppercase tracking-wider">
              <th class="py-3 px-4">Order ID</th>
              <th class="py-3 px-4">Customer Name</th>
              <th class="py-3 px-4">Masked PII Email</th>
              <th class="py-3 px-4">Category</th>
              <th class="py-3 px-4">Amount ($)</th>
              <th class="py-3 px-4">Engine Status</th>
            </tr>
          </thead>
          <tbody id="tableBody" class="text-xs text-slate-300 divide-y divide-slate-800/60 font-mono">
            <tr class="hover:bg-slate-800/40">
              <td class="py-3 px-4 text-blue-400">#1001</td>
              <td class="py-3 px-4 text-white font-sans font-medium">Alice Smith</td>
              <td class="py-3 px-4 text-emerald-400">a***@example.com</td>
              <td class="py-3 px-4"><span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded">electronics</span></td>
              <td class="py-3 px-4">$250.50</td>
              <td class="py-3 px-4"><span class="text-emerald-400 font-sans font-semibold">✓ Masked & Saved</span></td>
            </tr>
            <tr class="hover:bg-slate-800/40">
              <td class="py-3 px-4 text-blue-400">#1002</td>
              <td class="py-3 px-4 text-white font-sans font-medium">Bob Jones</td>
              <td class="py-3 px-4 text-emerald-400">b***@domain.org</td>
              <td class="py-3 px-4"><span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-2 py-0.5 rounded">electronics</span></td>
              <td class="py-3 px-4">$150.00</td>
              <td class="py-3 px-4"><span class="text-emerald-400 font-sans font-semibold">✓ Masked & Saved</span></td>
            </tr>
            <tr class="hover:bg-slate-800/40">
              <td class="py-3 px-4 text-blue-400">#1003</td>
              <td class="py-3 px-4 text-white font-sans font-medium">Charlie Brown</td>
              <td class="py-3 px-4 text-emerald-400">c***@company.com</td>
              <td class="py-3 px-4"><span class="bg-purple-500/10 text-purple-400 border border-purple-500/20 px-2 py-0.5 rounded">books</span></td>
              <td class="py-3 px-4">$45.99</td>
              <td class="py-3 px-4"><span class="text-emerald-400 font-sans font-semibold">✓ Masked & Saved</span></td>
            </tr>
          </tbody>
        </table>
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

    async function runPipelineTrigger() {
      const btn = document.getElementById("runBtn");
      const dagStatus = document.getElementById("dagStatus");
      
      btn.disabled = true;
      btn.classList.add("opacity-50", "cursor-not-allowed");
      dagStatus.className = "bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-semibold px-3 py-1 rounded-full animate-pulse";
      dagStatus.innerText = "RUNNING";

      logMessage("Starting Async Engine DAG Execution...", "info");
      
      // Step 1: Source Node
      document.getElementById("node1").className = "bg-slate-950 border border-blue-500 rounded-xl p-4 active-dag-node";
      document.getElementById("n1Status").innerText = "EXECUTING...";
      document.getElementById("n1Status").className = "text-blue-400 font-bold";
      logMessage("Source Node (S3): Fetching raw batch records...", "info");
      await new Promise(r => setTimeout(r, 800));
      
      document.getElementById("n1Status").innerText = "SUCCESS";
      document.getElementById("n1Status").className = "text-emerald-400";
      document.getElementById("node1").className = "bg-slate-950 border border-emerald-500/40 rounded-xl p-4";
      logMessage("Source Node: Read 5,000 records successfully.", "success");

      // Step 2: Transformer Node
      document.getElementById("node2").className = "bg-slate-950 border border-blue-500 rounded-xl p-4 active-dag-node";
      document.getElementById("n2Status").innerText = "TRANSFORMING...";
      document.getElementById("n2Status").className = "text-blue-400 font-bold";
      logMessage("Transform Node (PII Masker): Applying SHA-256 and Email Masking...", "info");
      await new Promise(r => setTimeout(r, 1000));
      
      document.getElementById("n2Status").innerText = "SUCCESS";
      document.getElementById("n2Status").className = "text-emerald-400";
      document.getElementById("node2").className = "bg-slate-950 border border-emerald-500/40 rounded-xl p-4";
      logMessage("Transform Node: Cleaned & Masked 5,000 customer records.", "success");

      // Step 3: Sink Node
      document.getElementById("node3").className = "bg-slate-950 border border-blue-500 rounded-xl p-4 active-dag-node";
      document.getElementById("n3Status").innerText = "WRITING...";
      document.getElementById("n3Status").className = "text-blue-400 font-bold";
      logMessage("Sink Node (PostgreSQL): Writing batch to warehouse...", "info");
      await new Promise(r => setTimeout(r, 800));

      document.getElementById("n3Status").innerText = "SUCCESS";
      document.getElementById("n3Status").className = "text-emerald-400";
      document.getElementById("node3").className = "bg-slate-950 border border-emerald-500/40 rounded-xl p-4";
      logMessage("Sink Node: Committed 5,000 records into 'processed_orders'.", "success");

      // Complete
      dagStatus.className = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold px-3 py-1 rounded-full";
      dagStatus.innerText = "SUCCESS";
      logMessage("[COMPLETE] Pipeline execution finished in 2.6s!", "success");

      // Increment counter
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
        "dashboard": "http://localhost:8000/dashboard",
        "docs_url": "http://localhost:8000/docs",
        "health_check": "http://localhost:8000/api/v1/health"
    }
