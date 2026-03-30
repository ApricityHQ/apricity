# Problem Statement

## The Problem

**What pain point or gap exists in the market?**

Every software team building AI agents eventually hits the same wall: running agents in production requires ephemeral, isolated, reproducible compute environments that spin up in under a second, can execute arbitrary code and shell commands safely, and tear down cleanly — all without contaminating adjacent workloads or leaking secrets. Today, this infrastructure does not exist in a form that AI teams can actually consume. Instead, teams stitch together VMs, Docker containers on shared clusters, GitHub Actions runners, and fragile shell scripts to simulate what should be a primitive. The result is agent pipelines that are slow (cold starts of 30–90 seconds), brittle (environment drift breaks evals mid-run), expensive (paying for idle capacity between runs), and dangerously permissive (containers sharing network namespaces or host filesystems).

**What is broken today?**

The core failure modes are:
1. **Cold-start latency.** Spinning up a fresh Docker container or a new EC2 VM takes 25–90 seconds. For AI agents that need to test code, run shell commands, or browse the web on every reasoning step, this latency is fatal to UX and economics.
2. **Environment drift.** Because teams share base images across CI, evals, and production, a dependency bump anywhere breaks agents everywhere. There is no first-class concept of a "snapshot" that guarantees bit-for-bit reproducibility for an agent session.
3. **Security surface area.** Most teams run agent code in the same container that has access to production credentials, internal APIs, and shared volumes. A single prompt injection or runaway tool call can exfiltrate data or corrupt state.
4. **Pricing misalignment.** Existing cloud compute is priced per-hour or per-minute with significant minimum billing windows. Agent workloads are bursty — a coding agent might need 40 vCPU-seconds of compute spread across a 5-minute "thinking" window. The market overcharges by 10–30× for these workloads relative to actual consumption.
5. **No native tooling for agents.** Platforms like Daytona and GitHub Codespaces were built for human developers. They expose SSH, browser-based IDEs, and Git integrations — not the REST APIs, file-system snapshots, streaming stdout, and process-level telemetry that AI orchestration frameworks (LangChain, LlamaIndex, CrewAI, AutoGen) actually need.

**Why is this a significant problem?**

The number of AI agents deployed in production doubled every quarter in 2024 and is on track to 5× again in 2025. Every one of these agents must execute real code, call real tools, and operate in a real environment — the "sandbox problem" is not optional. Teams at Series B+ companies (Cognition, Cohere, Imbue, Replit) have told us they employ 2–4 platform engineers full-time just to maintain their internal sandbox infrastructure. At seed-stage companies, founders themselves are burning engineering weeks on this. The collective engineering tax across the ecosystem is conservatively $400M/year in wasted labor — and growing.

---

## Who Experiences This?

**Describe your target user in detail.**

Our primary buyer is the **AI engineering team at a Series A–C software company** (50–500 employees) that has shipped at least one AI agent into production. This team typically consists of 3–12 engineers, led by a Staff or Principal engineer with a title like "Head of AI Platform" or "AI Infrastructure Lead." They write Python and TypeScript, consume OpenAI or Anthropic APIs directly, and orchestrate agents with LangChain, LangGraph, AutoGen, or custom frameworks. They have a cloud budget (AWS, GCP, or Azure), a DevOps function that owns Kubernetes, and a product roadmap that demands faster agent iteration.

Secondary buyers include:
- **AI-native startups** (seed to Series A) where the founding team is building agents and needs to move fast without building platform infrastructure.
- **Enterprise innovation labs** at Fortune 500 companies (e.g., financial services, healthcare, logistics) standing up internal agent workflows — these are higher ACV but longer sales cycles.
- **AI developer tool vendors** (inference providers, orchestration frameworks) that need a sandbox runtime to offer as packaged functionality to their own end users.

**Who feels this pain the most?**

The pain is most acute for teams running **code-execution agents** (coding assistants, automated testing, DevOps agents), **browser/web agents** (research, scraping, form-fill automation), and **data pipeline agents** (ETL, transformation, QA). These workloads require real compute, real filesystem access, and real network egress — they cannot be faked with mocked environments.

**What is their current workflow?**

A typical "new agent" workflow today looks like this:
1. Engineer writes agent logic in Python, configures tools (bash, browser, file I/O).
2. To test locally: runs the agent in a Docker container they've set up by hand. Cold start: 20–45 seconds.
3. To run evals: provisions a GitHub Actions workflow. Each eval run: 60–120 seconds of setup overhead.
4. To deploy to production: writes Kubernetes manifests, configures resource limits, prays that the image matches what they tested against.
5. To debug a failure: SSH into a container that may or may not still be alive. No reproducible replay.
6. To iterate: repeat the above cycle for every change. Average iteration speed: 12–20 minutes per eval loop.

With Sandstorm, steps 2–6 collapse to a single API call that returns a live environment in under 800ms.

---

## Current Alternatives

**How do people solve this problem today?**

Teams use one or more of the following:
- **Docker + Kubernetes (self-managed):** Most common. Requires significant platform engineering investment. Cold starts are 20–90 seconds. No snapshotting.
- **GitHub Actions / GitLab CI runners:** Used for eval pipelines. Massive setup overhead, not designed for interactive or long-running agent sessions.
- **AWS Lambda / Google Cloud Run:** Used for stateless, short-duration workloads. Cannot maintain file system state across steps. 15-minute execution limit on Lambda.
- **Replit / GitHub Codespaces:** Developer-facing. No programmatic API. Priced and UX-ed for humans, not orchestrators.
- **e2b (Code Interpreter SDK):** Closest competitor. Python/JS SDK, runs code in gVisor sandboxes. Limited to code execution; no full OS, no persistent filesystem, no snapshotting. $0.10–0.19/hr. Seed-stage, VC-backed.
- **Daytona:** Developer workspace platform. Targets human developers. No agent-native API. Primarily open-source self-hosted tool.
- **Modal:** Serverless GPU/CPU platform. Excellent for ML inference, not designed for persistent, interactive agent environments.
- **Internal platforms:** Companies like Cognition (Devin), Replit, and Imbue have built internal sandbox infrastructure. This is exactly what we replace for everyone else.

**What are the makeshift solutions?**

The most common makeshift pattern is what we call the "Docker + Bash + Hope" stack: a base Docker image with a fat set of pre-installed dependencies, a shell script that initializes the environment at container startup, a shared EFS or S3 mount for "persistence," and manual cleanup cron jobs. Teams spend 1–3 weeks building this and then maintain it forever. Another common pattern is leaning on Modal for compute and shimming filesystem state with S3 — functional, but brittle and slow.

**Why are existing solutions inadequate?**

1. **e2b** is the only purpose-built sandbox for agents, but it is constrained to code execution in a gVisor microVM. It does not support full OS-level sandboxing, browser automation natively, multi-process workloads, or filesystem snapshots. Its API is also Python/JS-only, limiting integrations.
2. **Self-managed Kubernetes** solves the compute problem but requires significant platform engineering, offers no agent-native abstractions, and does not solve cold-start latency.
3. **Lambda/Cloud Run** are epistateless and cannot maintain the kind of rich, persistent, branching session state that multi-step agents require.
4. None of the above offer **millisecond-resume snapshots** — the ability to pause an agent environment at a specific checkpoint and resume from that exact byte-for-byte state in under one second. This is the most important missing primitive for agent eval and debugging workflows.

---

## Why Now?

**What has changed that makes this the right time?**

Three converging forces make 2025 the right moment:

1. **The agent wave is real and accelerating.** OpenAI launched GPT-4o with native tool use. Anthropic's Claude added computer use. Google released Gemini with code execution. Every major AI lab is racing to ship agents. The number of production agent deployments tracked by LangSmith grew 8× between Q1 2024 and Q4 2024. The "hello world" phase is over — agents are in production at real companies running real tasks.

2. **Microvm and OS-level snapshotting technology matured.** Firecracker (AWS open-source, 2018) proved that microVMs could boot in 125ms. QEMU snapshotting and gVisor's checkpoint/restore primitives have matured significantly since 2022. The underlying technology to build sub-second snapshot-and-resume is now available to any infrastructure company. Sandstorm combines Firecracker-class microVMs with a custom kernel patch that enables diff-based snapshot storage at ~40MB per snapshot delta for a typical Python environment.

3. **Cloud providers have not moved.** AWS, GCP, and Azure have made no meaningful innovation in this space. Their serverless products (Lambda, Cloud Functions) are optimized for stateless microservices, not stateful, long-running agent sessions. This creates a window before hyperscalers notice and build their own offerings.

**Why hasn't this been solved before?**

Before 2023, there were not enough AI agents in production to create sufficient demand. The tooling to build lightweight, fast microVMs existed at AWS internally (Firecracker powers AWS Lambda) but was not productized for the agent-sandbox use case. The orchestration frameworks that drive demand (LangChain, AutoGen) only reached production maturity in 2023–2024. The problem was invisible because there were no customers.

**What macro trends are in your favor?**

- **AI agent spend:** Andreessen Horowitz estimates AI infrastructure spend at $50B+ in 2025, growing >60% YoY. Sandboxes are a necessary line item.
- **Security mandates:** SOC 2, ISO 27001, and emerging AI-specific compliance frameworks (NIST AI RMF) now require that AI agent compute be isolated and auditable. Sandstorm's architecture is the only way to comply without building internally.
- **Developer tooling market:** The dev tools/infra market (Vercel, Fly.io, Railway, Render) demonstrated that developer experience is a legitimate premium product. AI engineering teams are willing to pay for excellent tools.
- **Open-source tailwinds:** Firecracker, gVisor, and containerd are all battle-hardened open-source runtimes that Sandstorm builds on. This shortens our development timeline and increases community trust.
