# Sandstorm — Product & Technical Architecture
## Series A Investor Materials | Confidential | March 2025

**File:** sandstorm_technical_architecture_march2025.pdf
**Purpose:** Technical deep-dive for investor technical diligence and design partner evaluation.

---

## TABLE OF CONTENTS

1. Product Overview
2. User Workflow (End-to-End)
3. System Architecture
4. Core Components
5. Data Flow
6. AI/ML Systems
7. Security & Compliance Architecture
8. Scalability Design
9. Technical Roadmap
10. Technical Risks & Mitigations

---

## 1. PRODUCT OVERVIEW

Sandstorm is an **agent sandbox platform** — a cloud infrastructure service that provides isolated, ephemeral, reproducible Linux environments for AI agent workloads. The three-line pitch: any AI agent, any tool call, any environment — in under 800 milliseconds.

**Product surface area:**
- **REST API** (primary interface for non-SDK integrations and custom orchestrators)
- **Python SDK** (`pip install sandstorm-sdk`) — wraps REST API with async-first, Pythonic interface
- **TypeScript/Node SDK** (`npm install @sandstorm/sdk`) — identical capabilities
- **Framework integrations:** LangChain tool, LangGraph node, AutoGen agent, CrewAI tool, LlamaIndex query tool
- **Web Dashboard** (at app.sandstorm.dev) — account management, usage metrics, billing, environment logs; NOT for running environments (environments are API-only)

**Core product primitives:**

| Primitive | API Method | Latency | Description |
|---|---|---|---|
| Create environment | `POST /env` | <800ms | Boot a fresh Firecracker microVM from template or custom image |
| Run command | `POST /env/{id}/run` | <50ms + cmd duration | Execute shell command, stream stdout/stderr |
| Write file | `PUT /env/{id}/files/{path}` | <30ms | Write content to file in environment |
| Read file | `GET /env/{id}/files/{path}` | <30ms | Read file content from environment |
| Open browser | `POST /env/{id}/browser` | <2s | Launch Chromium, return CDP (Chrome DevTools Protocol) endpoint URL |
| Create snapshot | `POST /env/{id}/snapshot` | 200–450ms | Create filesystem + memory snapshot ("Timepoint") |
| Restore snapshot | `POST /env/restore/{snapshot_id}` | <800ms | Boot new environment from existing snapshot |
| Pause environment | `POST /env/{id}/pause` | <100ms | Suspend environment (zero compute billing while paused) |
| Resume environment | `POST /env/{id}/resume` | <800ms | Resume paused environment from suspended state |
| Destroy environment | `DELETE /env/{id}` | <200ms | Terminate and clean up all resources |

---

## 2. USER WORKFLOW (END-TO-END)

### 2.1 Simple Code Execution Agent

```python
import sandstorm
from langchain.tools import tool

client = sandstorm.Client(api_key="sk-...")

@tool
def run_python_code(code: str) -> str:
    """Execute Python code in an isolated sandbox and return the output."""
    with client.environment(template="python-3.11") as env:
        env.write_file("/workspace/script.py", code)
        result = env.run("python /workspace/script.py", timeout=30)
        return result.stdout

# LangChain agent uses the tool transparently
# Each tool call creates a fresh, isolated environment
# Environment is destroyed on context manager exit
```

**What happens under the hood (timeline):**
- T+0ms: `client.environment()` calls `POST /env`
- T+0→780ms: Control plane selects host with pre-warmed slot; MVM boots from Python-3.11 snapshot
- T+780ms: Environment live; `write_file` and `run` calls execute inside the microVM
- T+(780ms + cmd duration): `run()` returns stdout/stderr as structured result
- T+end: Context manager calls `DELETE /env/{id}`; resources released; billing stops

### 2.2 Multi-Step Agent with Snapshot Branching

```python
client = sandstorm.Client(api_key="sk-...")

# Boot base environment
env = client.create_environment(template="python-3.11")

# Install shared dependencies (once)
env.run("pip install pandas numpy matplotlib")

# Snapshot the prepared state
base_snapshot = env.snapshot()  # 320ms

# Now run 50 eval branches in parallel — each from the same snapshot
import asyncio

async def run_eval(prompt: str) -> dict:
    branch_env = client.restore(base_snapshot)
    result = branch_env.run(f"python eval.py --prompt '{prompt}'")
    branch_env.destroy()
    return {"prompt": prompt, "output": result.stdout}

prompts = load_eval_prompts()   # 50 prompts
results = await asyncio.gather(*[run_eval(p) for p in prompts])
```

**Key observation:** Without snapshots, each of the 50 branches would re-run `pip install` (adding ~45 seconds per branch). With snapshot branching: each branch pays only the restore cost (<800ms). Total time for 50 parallel evals: limited by parallelism of the fleet, not by per-branch setup time.

### 2.3 Browser Agent Workflow

```python
env = client.create_environment(template="ubuntu-22.04-browser")

# Open browser, get CDP endpoint
browser = env.open_browser()  # Returns CDP websocket URL

# Connect Playwright to the CDP endpoint
from playwright.async_api import async_playwright
async with async_playwright() as p:
    browser_conn = await p.chromium.connect_over_cdp(browser.cdp_url)
    page = await browser_conn.new_page()
    await page.goto("https://example.com")
    content = await page.content()

# Close browser, snapshot for replay
snap = env.snapshot()
env.destroy()
```

---

## 3. SYSTEM ARCHITECTURE

Sandstorm's architecture consists of four tiers:

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT TIER                              │
│  Python SDK  │  TypeScript SDK  │  REST API  │  Web Dashboard   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS / WebSocket
┌──────────────────────────▼──────────────────────────────────────┐
│                      CONTROL PLANE TIER                         │
│  API Gateway (Kong)  │  Environment Manager (Go)               │
│  Auth Service        │  Billing Metering (Go)                  │
│  Scheduler (Go)      │  Webhook Service (Go)                   │
│  Secret Injector     │  Fleet Monitor                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ gRPC
┌──────────────────────────▼──────────────────────────────────────┐
│                       HOST AGENT TIER                           │
│  Host Agent (Go) per bare-metal server                         │
│  Pre-warm Pool Manager  │  MVM Supervisor                      │
│  Snapshot Delta Engine  │  Firecracker process manager         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ virtio / KVM
┌──────────────────────────▼──────────────────────────────────────┐
│                    MICROVM TIER (per environment)               │
│  Firecracker MicroVM  │  Guest Linux kernel 6.8                │
│  Guest filesystem     │  Agent process(es)                     │
│  Network namespace    │  Chromium (if browser env)             │
└─────────────────────────────────────────────────────────────────┘
                           │ NVMe / S3
┌─────────────────────────────────────────────────────────────────┐
│                      STORAGE TIER                               │
│  NVMe hot cache (snapshots, logs)  │  S3 cold store            │
│  PostgreSQL (environment metadata) │  Redis (ephemeral state)  │
└─────────────────────────────────────────────────────────────────┘
```

**Infrastructure summary:**
- 48 bare-metal servers (current fleet): 2× Equinix SV5 (San Jose), 1× Equinix DA2 (Dallas), 1× Equinix FR5 (Frankfurt)
- Each server: AMD EPYC 7763 (64 cores), 512GB DDR4 ECC RAM, 4TB NVMe SSD, 25GbE networking
- Host OS: Ubuntu 22.04 LTS, Linux kernel 6.8 with Sandstorm custom CRIU patch
- Maximum environments per host: 48 (1 per CPU core; mem-limited to 10GB/env max)
- Active pre-warm slots: 4–8 per host, maintained by pre-warm pool manager

---

## 4. CORE COMPONENTS

### 4.1 Environment Manager (Control Plane)

The central coordination service, written in Go. Responsibilities:
- Receives `POST /env` requests from API gateway
- Selects optimal host via the Scheduler (minimizes latency + balances load)
- Issues `CREATE_ENV` gRPC call to selected host's Host Agent
- Maintains environment lifecycle state in PostgreSQL
- Orchestrates snapshot creation (multi-step: pause → serialize → compress → upload)
- Routes file I/O and command execution calls to correct host

**Key implementation detail:** Environment Manager maintains a soft-state in Redis for active environments (TTL: 30 seconds). If a client loses the environment ID, they can list environments via `GET /envs`. PostgreSQL is the source of truth for all persistent state.

### 4.2 Scheduler

A Go service that implements a modified bin-packing algorithm for environment placement:
- Inputs: Available hosts (memory, CPU, pre-warm slots), requested environment specs (CPU, memory, template)
- Algorithm: First-fit decreasing (FFD) bin packing with locality preference (routes to same datacenter as previous environments in the same session when possible)
- Pre-warm awareness: If a pre-warm slot matching the requested template exists on any host, prefer that host (eliminates cold start)
- SLA awareness: Enterprise accounts are routed to hosts with reserved capacity (5 hosts reserved for enterprise workloads in SV5)

### 4.3 Host Agent

A Go daemon running on every bare-metal host. Responsibilities:
- Maintain Firecracker process pool (per-environment process lifecycle)
- Manage pre-warm pool: creates N pre-booted microVMs per template, refreshes on claim
- Snapshot operations: pause → filesystem + memory serialization → delta compression → upload to NVMe cache + async S3
- Execute agent commands inside microVMs (via Firecracker's microVM serial console or vsock)
- Stream stdout/stderr to control plane via chunked HTTP/2 responses

### 4.4 Snapshot Delta Engine (Custom IP)

The proprietary component that differentiates Sandstorm's snapshot system from a naive Firecracker snapshot implementation.

**Naive Firecracker snapshot:** Captures full memory dump (~4–8GB for a Python environment) + full disk image (~2–5GB). Total snapshot size: 6–13GB. S3 upload at 10Gbps: 5–10 seconds. Impractical for frequent snapshotting.

**Sandstorm Snapshot Delta Engine:**
1. Tracks dirty pages since last snapshot using Linux `userfaultfd` and `/proc/PID/pagemap` APIs (custom kernel module)
2. On `snapshot()` call: serializes only dirty pages since last snapshot
3. Applies LZ4-level-1 compression to dirty page set (40–60% compression ratio on typical agent workloads)
4. Stores delta as: `{base_snapshot_id, delta_object_key, page_map}`
5. On restore: fetches base snapshot from NVMe, applies delta pages in order, boots microVM from resulting state

**Result:** Average snapshot delta size for a typical Python agent workload after 2–5 minutes of activity: **38MB** (vs. 8–13GB for naive full snapshot). Upload time: **<200ms** over 25GbE internal network.

**The custom kernel patch** (the proprietary IP): Our modification to Linux's CRIU infrastructure extends the `userfaultfd` mechanics with a generational page tracking system. Each generation can track up to 4M dirty pages independently, enabling multi-level delta chains (snapshot A → snapshot B → snapshot C) without exploding snapshot metadata storage.

### 4.5 Network Manager

Each microVM receives:
- A dedicated `veth` pair (one end in host namespace, one in microVM network namespace)
- A private IP from a `/28` block allocated per host (e.g., `10.32.1.0/28` → 14 usable addresses per block)
- An optional public egress via a shared NAT gateway (configurable; can be disabled for air-gapped environments)
- An optional inbound VPN endpoint (WireGuard) for enterprise customers who need their environments to speak to private VPCs

DNS and egress filtering are configurable per-environment via the API (`network_policy` parameter on `POST /env`).

---

## 5. DATA FLOW

### 5.1 Environment Creation Flow

```
Client SDK
  → POST /env (api.sandstorm.dev)
  → API Gateway (Kong) — auth check, rate limit
  → Environment Manager — validate spec, call Scheduler
  → Scheduler — select host, check pre-warm pool
  → Host Agent (gRPC: CREATE_ENV)
  → Host Agent:
      if pre-warm slot available:
        → claim slot, update IP assignment, inject secrets
        → return env ID + connection details in <800ms
      else:
        → launch new Firecracker process
        → boot from template snapshot
        → return env ID + connection details in <3s
  → Environment Manager — write to Postgres (env_id, host_id, status=RUNNING)
  → Return 201 {env_id, status, ws_url, ssh_key} to client
```

### 5.2 Command Execution Flow

```
Client SDK: env.run("python script.py")
  → POST /env/{id}/run (api.sandstorm.dev)
  → Environment Manager — look up host_id from Redis
  → Proxy to Host Agent at correct host (gRPC: RUN_CMD)
  → Host Agent → Firecracker vsock → guest shell
  → stdout/stderr stream back via chunked HTTP/2
  → Client SDK yields lines as async generator
  → On process exit: return {exit_code, stdout, stderr, duration_ms}
```

### 5.3 Snapshot Creation Flow

```
Client SDK: env.snapshot()
  → POST /env/{id}/snapshot (api.sandstorm.dev)
  → Environment Manager → Host Agent (gRPC: CREATE_SNAPSHOT)
  → Host Agent:
      1. Sends SIGSTOP to Firecracker process (pauses microVM) — 10ms
      2. Iterates /proc/{pid}/pagemap to identify dirty pages — 80–200ms
      3. Serializes dirty pages to temp buffer — 50–100ms
      4. LZ4-compress delta — 20–50ms
      5. Write to NVMe hot cache — 10ms
      6. Async: upload to S3 cold store — background, non-blocking
      7. Sends SIGCONT to resume microVM — 5ms
      Total client-visible latency: 200–450ms
  → Return {snapshot_id, size_bytes, created_at}
```

---

## 6. AI/ML SYSTEMS

Sandstorm is an infrastructure product, not an AI model product. However, we use ML/heuristics internally in two places:

### 6.1 Predictive Pre-Warm Scheduler

**Problem:** Pre-warming environments in advance requires predicting which templates customers will request and when. Wasted pre-warms cost money; insufficient pre-warms cause cold starts.

**Approach:** A lightweight time-series model (gradient-boosted trees, updated hourly) trained on per-customer historical request patterns. Features: hour-of-day, day-of-week, recent request rate, template distribution. Inference runs in the Scheduler service. The model predicts: which templates to pre-warm on which hosts, how many slots to maintain, and which hosts should be in "hot standby" vs. "warm standby."

**Current accuracy:** Within-30-minute prediction accuracy for template distribution: 81%.

### 6.2 Anomaly Detection for Environment Abuse

**Problem:** Environments could be abused (crypto mining, DDoS, data exfiltration). Standard rate limiting catches burst patterns but not sustained low-level abuse.

**Approach:** Per-environment CPU utilization and network egress patterns are monitored against a baseline model (trained on benign agent workloads). Deviations > 3σ from per-template baseline trigger an alert and automatic throttle. Confirmed abuse results in account termination.

**Current false-positive rate:** 0.3% of environment-runs trigger alert review; of these, 8% result in actual abuse flags (0.024% of all runs).

---

## 7. SECURITY & COMPLIANCE ARCHITECTURE

### 7.1 Isolation Model

Each environment is a Firecracker microVM — a separate kernel, separate filesystem, separate network namespace from all other environments and from the host. This provides:
- **Kernel isolation:** Each microVM runs its own Linux kernel. A kernel exploit in the guest does not affect the host or other environments (unlike containers, which share the host kernel).
- **Network isolation:** veth pair per environment; no inter-environment networking by default.
- **Filesystem isolation:** No shared volumes; each environment has its own ephemeral disk.
- **Process isolation:** Complete process namespace isolation; no shared `/proc` view.

### 7.2 Secret Management

Secrets (API keys, credentials) required by agent code are injected via:
1. Environment variables (set via `POST /env` `env_vars` parameter, encrypted at rest in Postgres using AES-256-GCM, decrypted only in-memory by Host Agent at environment boot).
2. Vault integration (enterprise): A WireGuard tunnel allows enterprise environments to reach a customer-managed Vault instance for dynamic secrets.

Secrets are never written to the environment filesystem or to any Sandstorm log.

### 7.3 Network Egress Policy

By default: outbound internet allowed, inbound blocked (NAT-only). Customers can configure:
- **Egress whitelist:** Only allow outbound to specified CIDR ranges or domain names
- **Airplane mode:** No egress (environments fully air-gapped); required for highest-security workloads
- **Egress logging:** All DNS queries and TCP/UDP connections logged to customer-accessible audit stream

### 7.4 Audit Logging

Every environment event (create, run, snapshot, restore, destroy) is logged to an immutable append-only log. Logs include: timestamp, account_id, environment_id, action, parameters (secrets redacted), result, host_id (for internal traceability). Enterprise customers can stream audit logs to their own SIEM via webhook or S3 export.

### 7.5 Compliance Roadmap

| Certification | Status | Target |
|---|---|---|
| SOC 2 Type I | In progress (Vanta + auditor engaged) | Q3 2025 |
| SOC 2 Type II | Planned | Q2 2026 |
| ISO 27001 | Planned | Q4 2026 |
| GDPR (EU data residency) | Partial (FR5 datacenter live) | Q2 2025 (full data residency guarantees) |
| FedRAMP Moderate | Evaluated | Q1 2027 (required for US government) |

---

## 8. SCALABILITY DESIGN

### 8.1 Current Capacity

- 48 bare-metal servers × 48 environments/server = **2,304 simultaneous environments**
- With average env duration of 8 minutes: **~16,000 environment-starts/hour** theoretical maximum
- Current peak load: 340 simultaneous environments (design partner workloads)
- Current utilization: ~45% of theoretical maximum at peak hours

### 8.2 Horizontal Scaling

The control plane (Environment Manager, Scheduler, Billing Metering) is stateless and runs on Kubernetes (GKE) with horizontal autoscaling. It can scale to handle 10,000+ API requests/second without architectural changes.

The bare-metal fleet scales by adding servers (colocation agreement allows up to 200 servers in current Equinix commitment). Each server added: ~2–3 days for hardware delivery + 4 hours for OS + agent provisioning (automated via Ansible playbook).

**Fleet expansion plan:**
- Q2 2025: 48 → 72 servers (before GA launch)
- Q4 2025: 72 → 120 servers (driven by utilization hitting 65%+)
- Q2 2026: 120 → 200 servers (EU expansion + peak capacity)

### 8.3 Bottlenecks & Mitigations

| Potential Bottleneck | Mitigation |
|---|---|
| Pre-warm pool exhaustion (burst traffic) | Queue-based overflow: queued environments boot from scratch (<3s), not returned as failure |
| NVMe snapshot cache saturation | LRU eviction to S3; hot cache sized for 90th percentile active snapshot set (currently 800GB/host) |
| S3 upload bandwidth | Parallel upload with 5× redundant paths; NVMe cache ensures restore doesn't wait for S3 |
| Control plane DB (Postgres) | Read-replicas for environment lookups; eventual consistency for non-critical state |
| DNS / network namespace limits | Each host is limited to 240 network namespaces (kernel setting); ~5 reserved per host for system use = 235 usable |

---

## 9. TECHNICAL ROADMAP

### Q2 2025 (April–June 2025)

| Feature | Description | Priority |
|---|---|---|
| GA release | Remove waitlist, enable Stripe self-serve billing | P0 |
| Pre-warm pool v2 | ML-driven pre-warm prediction (see Section 6.1) | P0 |
| Windows sandbox (experimental) | Windows 11 microVM support via KVM/QEMU (experimental; limited templates) | P1 |
| LangGraph native node | First-class LangGraph node type (not just LangChain tool) | P1 |
| AutoGen integration | `sandstorm` as AutoGen code executor backend (replaces Docker executor) | P1 |
| Dashboard v2 | Environment metrics, snapshot browser, live log tailing in web UI | P2 |

### Q3 2025 (July–September 2025)

| Feature | Description | Priority |
|---|---|---|
| Persistent Workspaces (beta) | Long-lived environments that survive across agent sessions (pause-on-idle, resume on demand) | P0 |
| SOC 2 Type I audit completion | With Vanta + external auditor | P0 |
| Snapshot branching UI | Visual snapshot tree in web dashboard (for debugging and eval replay) | P1 |
| SAML/SSO | For enterprise accounts | P1 |
| GPU environment support (experimental) | NVIDIA GPU passthrough for GPU-accelerated agent workloads | P2 |

### Q4 2025 (October–December 2025)

| Feature | Description | Priority |
|---|---|---|
| Multi-region GA | Full GA in EU (FR5) and APAC (Singapore — new PoP) | P0 |
| Snapshot CDN | Geo-distribute popular template snapshots to all PoPs for sub-800ms cold start globally | P0 |
| Audit log SIEM export | Splunk, Datadog, Elastic native integrations | P1 |
| Windows sandbox GA | Full Windows 11 template support | P1 |

---

## 10. TECHNICAL RISKS & MITIGATIONS

### Risk 1: Firecracker Upstream Breaking Changes
**Risk:** A breaking change in Firecracker's snapshot API (our most critical dependency) invalidates our control plane integration.
**Mitigation:** We pin to Firecracker v1.6.0. We run a continuous integration pipeline that tests our agent against Firecracker's main branch weekly. Priya's relationship with the Firecracker team gives us 30–60 day advance notice of breaking API changes. We maintain a compatibility shim layer.

### Risk 2: Custom Kernel Patch Maintenance Burden
**Risk:** As upstream Linux evolves, maintaining our custom CRIU patch becomes increasingly expensive. Our patch currently applies cleanly to Linux 6.6 and 6.8. If the upstream CRIU interfaces change, we face a re-porting effort.
**Mitigation:** We are contributing our generational page tracking logic to the CRIU upstream project (draft submitted as RFC in February 2025). If accepted upstream, our maintenance burden drops to zero. If rejected, we maintain the patch independently with Seo-Yeon as the primary owner (and a second kernel engineer joining Q3 2025).

### Risk 3: Multi-Tenant Isolation Vulnerability
**Risk:** A Firecracker microVM escape vulnerability (similar to the Spectre/Meltdown class) could allow an environment to read host or neighboring-environment memory.
**Mitigation:** We run with strict memory isolation (KPTI enabled, hardware-enforced memory encryption on AMD EPYC via SEV-SNP where supported). We subscribe to Firecracker security advisories and maintain a 72-hour patch SLA. We carry cyber liability insurance covering $2M per incident.

### Risk 4: Snapshot Delta Corruption
**Risk:** A bug in our custom delta compression algorithm produces a corrupt snapshot delta. On restore, the environment boots into a broken state.
**Mitigation:** Every snapshot is verified with a SHA-256 hash of the memory + filesystem state at snapshot time. On restore, the hash is recomputed and compared before making the environment available to the client. A mismatch triggers an automatic retry from the base snapshot. We run 10,000+ synthetic round-trip snapshot tests per day in CI.

### Risk 5: Network Egress Abuse
**Risk:** A customer runs an agent that generates massive egress (DDoS amplification, exfiltration). We receive an abuse complaint and an emergency AWS bill for egress overage.
**Mitigation:** Hard egress limit of 1TB/month per account (configurable upward with enterprise tier). Real-time network monitoring flags accounts exceeding 10GB/hour; automatic environment pause pending review. Egress is billed to the customer (not absorbed), which creates natural economic deterrence.
