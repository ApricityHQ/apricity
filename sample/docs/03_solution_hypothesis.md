# Solution Hypothesis

## Core Solution

**What are you building? Describe it simply.**

Sandstorm is an **agent sandbox platform** — a cloud infrastructure service that gives AI teams instant, isolated, reproducible compute environments for their agents. Developers call our REST API (or use our Python/TypeScript SDK) and get back a live environment in under 800 milliseconds. That environment is a full Linux microVM with a real filesystem, real network, and real process isolation. Agents can run bash commands, execute Python or Node.js code, open a browser, read and write files — anything they could do on a developer's laptop, but isolated, auditable, and billed by the millisecond.

The three core capabilities that differentiate Sandstorm:

1. **Millisecond-resume snapshots ("Timepoints"):** Freeze any environment at any point in time. Resume it in under 800ms — from the exact filesystem state, memory state, and process state, anywhere. Use this for: reproducible evals (always start from the same state), branching agent sessions (explore multiple decision branches in parallel), instant debugging (replay any failure from its exact pre-failure state), and cost optimization (pause an idle environment, resume when needed, pay zero while paused).

2. **Sub-second cold starts:** A fresh environment from our standard template library (Python 3.11, Node.js 20, Ubuntu 22.04, browser, etc.) is live in under 800ms. Custom environments from a user-provided Docker image are live in under 3 seconds after first boot (subsequent boots from snapshot: <800ms).

3. **Agent-native API surface:** Unlike developer workspace tools (Daytona, Codespaces), Sandstorm's API is designed for machine consumption. Key primitives: `environment.run_command(cmd)` with streaming stdout/stderr and exit code, `environment.write_file(path, content)`, `environment.read_file(path)`, `environment.snapshot()`, `environment.restore(snapshot_id)`, `environment.open_browser()` returning a live Chrome DevTools Protocol endpoint, `environment.stream_logs()` for real-time telemetry. Every call is idempotent and async-safe.

**How does it work?**

Infrastructure layer: Each Sandstorm environment is a Firecracker microVM running on bare-metal servers in our own data centers (currently colocated in Equinix SV5, Dallas DA2, and Frankfurt FR5). We chose bare-metal (not cloud VMs) because nested virtualization performance is ~30% worse on cloud VMs for our workload profile. Our host kernel runs a patched version of Linux 6.8 with our custom CRIU extensions for fast snapshot delta compression.

Snapshot layer ("Timepoints"): When a user calls `environment.snapshot()`, we pause the microVM using Firecracker's snapshot API, serialize memory and disk state, apply our delta-compression algorithm (which identifies and deduplicates page-level changes since the last snapshot), and write the delta to our object store (S3 + a hot-tier NVMe SSD cache on the host). Total snapshot operation: 200–450ms. Resume from snapshot: 400–800ms depending on memory footprint.

Networking layer: Each environment gets a dedicated veth pair and network namespace. Outbound internet access is on by default but can be disabled. Egress filtering, DNS override, and request logging are all configurable via the API. This allows teams to run agents in "airplane mode" for security-sensitive workloads.

Orchestration layer: A control plane built in Go manages environment lifecycle (create, run, snapshot, restore, destroy), resource scheduling across the bare-metal fleet, billing metering (millisecond-precision), secret injection (via environment variables with an optional Vault integration), and webhook delivery for environment events.

SDK layer: Python and TypeScript SDKs wrap the REST API. Native integrations for LangChain tools, LangGraph nodes, AutoGen agents, and Anthropic's tool_use format. A one-line integration with OpenAI's Assistants API for code interpreter replacement.

**What is the core mechanic?**

The core mechanic is `snapshot → restore`: the ability to freeze and replay any environment state in under a second. This primitive unlocks a new class of workflows that were previously impossible: parallel eval branches, deterministic replays, zero-cold-start production pools, and agent "undo" operations. Everything else in the product — the API design, the pricing model, the SDK integrations — is organized around making this mechanic as easy and cheap to use as possible.

---

## Unique Value Proposition

**Why will customers choose you over alternatives?**

Customers choose Sandstorm when they need:
1. **Speed they can't achieve elsewhere.** Sub-800ms environment boot vs. 30–90 seconds for Docker/Kubernetes. This is not a 10% improvement — it changes the economics of eval loops and the UX of interactive agent sessions.
2. **The snapshot primitive.** No competitor offers millisecond-resume snapshots across full OS environments. e2b offers gVisor-based code execution but no snapshotting. Modal offers compute but no persistent agent-state management.
3. **API-first design.** The entire product is designed for machine orchestration, not human use. Every behavior is deterministic, every response is structured JSON, every side effect is auditable.
4. **Usage-based pricing that matches agent economics.** We bill per compute-second (vCPU-second and GB-RAM-second) with no minimum billing window. An agent that boots a sandbox, runs a 3-second bash command, and destroys it pays for ~4 CPU-seconds of compute. On AWS Lambda, the minimum billing unit is 1ms but the minimum memory is 128MB, and Lambda cannot run the persistent, stateful workloads agents need. Our pricing is 60–80% cheaper than the Lambda + Docker equivalent for typical agent workloads.

**What is 10x better?**

| Dimension | Sandstorm | Best Alternative |
|---|---|---|
| Environment boot time | <800ms | 25–90 seconds (Docker on Kubernetes) |
| Snapshot + resume | <800ms | Not available |
| Billing granularity | Per CPU-second, no minimum | Per minute (GHA), per 100ms (Lambda, no persistent state) |
| Agent-native API | Yes (designed for LLM orchestration) | No (SSH, browser IDE, or Lambda handler) |
| Full OS sandbox | Yes (Firecracker microVM) | Partial (gVisor code-execution only for e2b) |
| Browser support | Yes (Chromium via CDP) | No (e2b); Limited (Playwright on Lambda, no persistence) |
| Snapshot branching | Yes | No |

**What is your moat?**

Our moat has four layers:
1. **Technical depth (kernel-level IP):** Our snapshot compression algorithm and the custom CRIU patches took 4 person-months to write and are not published. Replicating this requires rare expertise.
2. **Infrastructure investment (bare-metal fleet):** We have signed 3-year colocation leases with Equinix and deployed 48 bare-metal servers. This upfront capital investment creates a performance and cost advantage that a software-only competitor cannot match without making the same investment.
3. **Ecosystem integrations (network effects):** As we build native integrations with LangChain, AutoGen, and CrewAI, switching costs increase. Teams that have 50 agent pipelines built on the Sandstorm SDK do not switch lightly.
4. **Data flywheel:** Every environment run generates telemetry on agent workload patterns — which environments are slow, which snapshots are hot, which tool calls fail. This data trains our scheduler and our pre-warm system, making the platform faster for every new customer as the fleet grows.
