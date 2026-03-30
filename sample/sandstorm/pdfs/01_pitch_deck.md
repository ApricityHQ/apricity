# Sandstorm — Pitch Deck
## Series A Fundraise | Confidential | March 2025

**File:** sandstorm_pitch_deck_series_a_march2025.pdf
**Purpose:** Primary investor presentation for the $12M Series A round.

---

## SLIDE 1 — Title

**SANDSTORM**
*The Agent Sandbox Platform*

**Series A | $12M**
March 2025 | Confidential

Priya Anand, CEO — priya@sandstorm.dev
Marcus Webb, CTO — marcus@sandstorm.dev

sandstorm.dev | @sandstorm_dev

[VISUAL: Dark background, gradient from deep navy (#0A0F2E) to midnight blue (#151B3D). The Sandstorm wordmark is in white with a subtle grain texture. A single abstract microVM grid pattern is rendered in low-opacity on the right half of the slide — suggesting compute at scale. No clip art, no stock photos.]

---

## SLIDE 2 — Problem

**AI agents are only as fast as their sandbox.**

Today, spinning up an isolated environment for an AI agent takes 30–90 seconds.
That's 4,000× too slow.

[VISUAL: A horizontal timeline bar showing the lifecycle of one agent "step":
- Model call: 1.2s
- Tool invocation: 0.4s
- ❌ Sandbox boot: 45s ← labeled "THE BOTTLENECK"
- Code execution: 3.1s
- Result processing: 0.8s
Total step time: 50.5s. With Sandstorm: 6.3s.]

**The result:**

- 🐢 Agent eval loops take 30+ minutes instead of 3 minutes
- 💸 Teams pay for idle compute between agent runs
- 🔥 Platform engineers spend 2–4 weeks building internal sandbox infrastructure
- 🔓 Agent code runs in insecure, shared environments

> *"We have 3 engineers maintaining our sandbox infrastructure. It's a full-time job." — Head of AI Platform, Series B company (design partner)*

---

## SLIDE 3 — Why Now

**Three forces are colliding in 2025:**

[VISUAL: Three columns, each with an icon and headline.]

**1. Agents are in production**
Production agent deployments grew 8× in 2024 (LangSmith). The "hello world" phase is over. Every team running agents is hitting the sandbox wall.

**2. Microvm technology is mature**
Firecracker (AWS open-source) proved microVMs can boot in 125ms. CRIU checkpoint/restore matured in Linux 6.x. The stack is ready to build on.

**3. Hyperscalers haven't moved**
AWS Lambda, GCP Cloud Run, and Azure Functions were built for stateless microservices. None have shipped an agent-native sandbox API. The window is open.

**The "agent infrastructure gap" exists right now. It will close within 24 months.**

---

## SLIDE 4 — Solution

**Sandstorm: Environments for agents, not developers.**

```python
import sandstorm

# Boot an isolated Linux environment in <800ms
env = sandstorm.create(template="python-3.11")

# Run code, commands, and tools
result = env.run("pip install pandas && python analysis.py")

# Freeze state. Resume anywhere, anytime.
snap = env.snapshot()  # 200–450ms
env2 = sandstorm.restore(snap)  # <800ms resume
```

**Three primitives that change agent economics:**

| Primitive | What It Does | Why It Matters |
|---|---|---|
| `create()` | Boots a full Linux microVM in <800ms | Eliminates cold-start bottleneck |
| `snapshot()` | Freezes environment state in <450ms | Enables reproducible evals, branching, undo |
| `restore()` | Resumes from any snapshot in <800ms | Zero cold start for warm pools; replay any failure |

[VISUAL: A three-panel diagram showing (1) a microVM spinning up, (2) a snapshot branching into two parallel environments, (3) a restored environment. Clean, minimal line-art style.]

---

## SLIDE 5 — Product Workflow

**From agent call to running environment in one API call.**

[VISUAL: Horizontal flow diagram with 5 steps, connected by arrows.]

**STEP 1: Agent Triggers Environment**
LangChain/AutoGen/CrewAI agent calls `sandstorm.create(template="python-3.11")` with optional secret injection and network policy.

**STEP 2: Sandstorm Control Plane Routes Request**
Go control plane selects nearest bare-metal host with pre-warmed microVM slot. If pre-warm slot available: environment live in <800ms. If fresh boot: environment live in <1.5s.

**STEP 3: Environment Executes**
Agent calls `env.run(cmd)`, `env.write_file()`, `env.read_file()`, `env.open_browser()`. All calls stream real-time stdout/stderr + structured JSON metadata.

**STEP 4: Snapshot on Demand**
Agent (or orchestrator) calls `env.snapshot()`. Delta compressed and written to NVMe cache + S3. Snapshot ID returned in <450ms.

**STEP 5: Restore / Destroy**
Agent resumes from snapshot (<800ms) or calls `env.destroy()`. Billing stops at destroy. Paused environments (idle > 60 seconds with `pause_on_idle=True`) accumulate zero compute spend.

---

## SLIDE 6 — Market Size

**A $4.2B market today growing to $14B by 2027.**

[VISUAL: Concentric rings — TAM (outer), SAM (middle), SOM (inner). Each ring labeled with dollar amount and description.]

**TAM — $4.2B (2025), $14B (2027)**
Global AI agent compute infrastructure spend. Agent workloads = 8% of AI infrastructure today, growing to 22% by 2027. Source: IDC AI Infrastructure Forecast 2024–2028.

**SAM — $720M (2025), $2.4B (2027)**
Software companies in NA + EU with active AI engineering teams, willing to use managed cloud service. ~18,000 companies × $50K–$400K/yr cloud spend × 40% managed-service adoption.

**SOM — $1.2M ARR (2025) → $22M ARR (2027)**
Conservative capture rate: 0.17% of SAM in Year 1, scaling to 0.9% of SAM by Year 3.

---

## SLIDE 7 — Business Model

**Usage-based pricing aligned with agent economics.**

[VISUAL: Side-by-side comparison table and pricing card.]

**Pricing:**

| Meter | Rate |
|---|---|
| vCPU-second | $0.000048 |
| GB RAM-second | $0.000008 |
| Snapshot storage (per GB-month) | $0.025 |
| Egress (per GB, 10GB free) | $0.090 |

**Example bills:**
- Coding agent, 1-min run (2 vCPU, 4GB): **~$0.014**
- Research agent, 10-min browser session (2 vCPU, 8GB): **~$0.12**
- Eval pipeline, 500 runs/day (1 min each, pre-warmed from snapshot): **~$7.00/day**

**Enterprise tier:** $2,500–$10,000/month platform fee + usage.

**Why usage-based wins:** NRR naturally exceeds 100% as agent adoption grows within accounts. Customers who run more agents pay more — our revenue grows without new logo acquisition.

**Target gross margin:** 62% today → 72% at $5M ARR (infrastructure utilization improving).

---

## SLIDE 8 — Traction

**31K MRR from 8 design partners. Pre-revenue, pre-GA.**

[VISUAL: Metrics displayed in large bold numbers with trend arrows.]

**$31K MRR** — 8 paying design partners (private beta, no marketing spend)
**8× growth** — in production agent runs on LangSmith (industry benchmark, Q1→Q4 2024)
**<800ms** — p50 environment boot time (benchmark: 45s for Docker/k8s)
**60 interviews** — customer discovery calls before building (zero guesswork)
**4,800 downloads** — langchain-sandstorm in first 4 weeks
**612 GitHub stars** — sandstorm-bench open-source benchmark suite

**Design partners include:**
- 1 Series B AI-native company (agent coding assistant; $8,000/month pilot)
- 1 Fortune 500 financial services AI lab ($4,500/month pilot; under NDA)
- 4 YC W24/S24 AI startups ($1,500–$3,000/month pilots)
- 2 individual developers ($500–$1,000/month pilots)

**Waitlist:** 1,847 companies (847 from HN "Show HN" launch + 1,000 from organic channels)

---

## SLIDE 9 — Go-to-Market

**Developer-led, community-first, experiment-driven.**

[VISUAL: Funnel diagram with 3 acquisition stages and 2 expansion stages.]

**Stage 1: Awareness (Community)**
- Twitter/X technical threads (Priya: 3,100 followers, 82K avg impressions/thread)
- HN "Show HN" launches (847 signups from first post)
- Framework integrations (LangChain, AutoGen, CrewAI, LlamaIndex)
- Open-source benchmark suite (612 GitHub stars, organic SEO)

**Stage 2: Trial (Self-serve)**
- Free tier: 1,000 compute-seconds/month (no credit card required)
- GA launch: June 2025 via Product Hunt + HN cross-post
- Target: 300 accounts in Month 1 of GA; 22% conversion to paid within 30 days

**Stage 3: Expand (Accounts)**
- Usage-based billing drives organic expansion as agents scale
- Target NRR: 115%

**Stage 4: Enterprise**
- Founder-led sales → AE hire Q3 2025
- Sales cycle trigger: SOC 2 Type I completion (Q3 2025)
- ICP: Head of AI Platform, 100–500 person company, 3+ agents in production

**Target CAC:**
- Self-serve: $800 (community channels)
- Enterprise: $18,000 (founder/AE sales)
- Blended at GA: $4,200

---

## SLIDE 10 — Competition

**No one else does what we do. Here's the landscape.**

[VISUAL: 2×2 matrix. X-axis: "Code execution only ← → Full OS sandbox." Y-axis: "Human-facing ← → Agent-native API." Competitors placed on the matrix.]

**Bottom-left (code execution, human-facing):** GitHub Codespaces, Daytona, Replit
**Top-left (code execution, agent-native):** e2b ← "closest competitor; no snapshotting, no full OS"
**Bottom-right (full OS, human-facing):** AWS EC2, GCP Compute Engine
**Top-right (full OS, agent-native):** **SANDSTORM** ← "the only player here"

**Why incumbents can't just copy us:**
- **AWS/GCP:** Architectural inertia; Lambda/Cloud Run built for stateless services; would cannibalize existing revenue
- **e2b:** gVisor architecture limits them to code execution; snapshotting requires a full rewrite
- **Modal:** Positioned for ML inference, not agent sessions; different ICP and infrastructure design

---

## SLIDE 11 — Technology

**Purpose-built infrastructure, not repurposed cloud services.**

[VISUAL: Architecture diagram — three horizontal tiers: Infrastructure Layer, Control Plane Layer, API/SDK Layer.]

**Infrastructure Layer (bare-metal)**
- 48 bare-metal servers, Equinix SV5 (San Jose), DA2 (Dallas), FR5 (Frankfurt)
- Linux 6.8 host kernel with custom CRIU patches (proprietary snapshot delta compression — 65% size reduction vs. naive Firecracker snapshot)
- Firecracker microVMs (AWS open-source) for hardware-level isolation
- NVMe SSD hot-tier snapshot cache: 95% of snapshot resumes served in <800ms without S3 roundtrip

**Control Plane Layer (Go)**
- Environment lifecycle management (create, pause, restore, destroy)
- Resource scheduling across bare-metal fleet
- Millisecond-precision billing metering
- Secret injection (environment variables + Vault integration)
- Webhook delivery for environment events

**API/SDK Layer**
- REST API (100% of functionality)
- Python SDK + TypeScript SDK
- Native integrations: LangChain, LangGraph, AutoGen, CrewAI, LlamaIndex
- One-line OpenAI Code Interpreter replacement

**Key technical differentiators:**
- Sub-800ms cold start (vs. 30–90s for Docker/k8s)
- Sub-800ms snapshot resume (vs. not available elsewhere)
- Full Linux OS (vs. gVisor code execution only for e2b)
- Per-100ms billing (vs. per-minute minimum for GHA)

---

## SLIDE 12 — Team

**The founders who built Lambda's snapshot-restore are building Sandstorm.**

[VISUAL: Two founder headshots (professional, dark background). Below, compact team grid.]

**Priya Anand — CEO & Co-Founder**
Principal Engineer, AWS Lambda (Firecracker snapshot-restore author). 6 years AWS infrastructure. Built the system that runs 100M+ Lambda functions/day. MIT CS 2015.

**Marcus Webb — CTO & Co-Founder**
Founding Infrastructure Engineer, Cohere (0 → Series C). Staff Engineer, Modal. Stripe, Google SRE. Imperial College London M.Eng. 2016.

**Key Team:**
- **Seo-Yeon Park** — Staff Engineer, Kernel. Red Hat KVM team. PhD ETH Zürich.
- **Amara Diallo** — Head of Product. Segment, Vercel. Deep dev-tool PM.
- **Ryo Tanaka** — SDK/Integrations. Early LangChain employee. `langchain-sandstorm` author.
- **Yemi Okafor** — Control Plane. Cloudflare Workers KV and Durable Objects.

**Advisors:** David Haber (Kandji co-founder), Christina Ou (ex-CISO Plaid), Dr. Anastasia Voronova (VMware Research), Nadia Karim (ex-Head of DevRel, Stripe)

---

## SLIDE 13 — Financial Highlights

**Strong early signal. Raising to scale.**

[VISUAL: Two charts side by side — (1) 24-month MRR forecast bar chart, (2) burn vs. revenue line chart showing break-even trajectory.]

**Revenue trajectory (MRR):**
- Today (April 2025): $31K
- GA launch (June 2025): $65K
- 12 months (April 2026): $400K
- 24 months (April 2027): ~$900K

**Unit economics:**
- Gross margin (current): 62%
- Gross margin (target, $5M ARR): 72%
- LTV (blended): $18,700 (30-month retention × avg $620/month)
- LTV:CAC (blended at GA): 4.5×

**Current financials:**
- Burn: $148K/month
- Cash: $1.87M (12.6 months runway, pre-Series A)
- Revenue: $31K MRR (design partners only)

**Forecast note:** Based on 22% trial-to-paid conversion, 2.5% monthly churn, $620/month avg self-serve ACV, $6,200/month avg enterprise ACV.

---

## SLIDE 14 — Fundraising Ask

**Raising $12M Series A to become the category-defining agent sandbox.**

[VISUAL: Use-of-funds donut chart + milestone timeline.]

**Round details:**
- **Size:** $12M Series A
- **Instrument:** Priced equity, Series A Preferred
- **Pre-money:** $28M
- **Lead:** Accel Partners ($8M; term sheet signed)
- **Co-lead:** Gradient Ventures — pro-rata ($2M)
- **Remaining:** $2M (open; conversations with Bessemer, General Catalyst)

**Use of proceeds (18 months):**
- Engineering headcount (8 FTE): $5.4M (45%)
- Infrastructure expansion (bare-metal x2): $2.4M (20%)
- Sales & Marketing: $1.8M (15%)
- Product & Design: $0.6M (5%)
- G&A: $0.6M (5%)
- Buffer: $1.2M (10%)

**Key milestones this round unlocks:**
- GA launch + self-serve (June 2025)
- SOC 2 Type I (Q3 2025)
- $150K MRR (Q3 2025)
- First enterprise account (Q3 2025)
- Series B readiness at $800K MRR (Q4 2026)

---

## SLIDE 15 — Vision

**Every AI agent in the world runs in a Sandstorm.**

The way Vercel became the obvious place to deploy a web app, Sandstorm becomes the obvious place to run an AI agent. Not because we're the cheapest — because we're the only option that was built for agents from day one.

In five years: Sandstorm is the compute layer underneath 30% of all AI agents in production. We are the AWS Lambda for agent compute — but with millisecond snapshots, full OS isolation, and an API designed for machines, not developers.

The agent wave is here. The infrastructure is not. We're building it.

**sandstorm.dev/investors**
priya@sandstorm.dev | +1 (415) 555-0147

*This presentation is confidential and intended for accredited investors only. Forward-looking statements involve risks and uncertainties. Past traction is not a guarantee of future results.*
