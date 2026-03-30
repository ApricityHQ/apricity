# Market Notes

## Competitive Landscape

**Who else is in this space? How are you different?**

The agent sandbox market sits at the intersection of three adjacent markets: developer infrastructure, AI tooling, and cloud compute. No single incumbent owns it. The closest players, their positioning, and our differentiation:

| Competitor | Stage | What They Do | What They Miss |
|---|---|---|---|
| **e2b** | Seed (~$10M raised) | Python/TypeScript SDK for code execution in gVisor sandboxes | No full OS sandbox, no persistent filesystem, no snapshotting, no browser, API depth limited |
| **Daytona** | Seed (~$3M raised) | Open-source developer workspace manager | Human-facing (SSH/IDE), no agent-native API, no millisecond boot |
| **Modal** | Series B (~$30M raised) | Serverless GPU/CPU for ML workloads | Not designed for persistent stateful agent sessions; no snapshotting |
| **AWS Lambda** | GA (Hyperscaler) | Serverless compute | 15-min limit, read-only FS, no agent abstractions, 100ms min billing |
| **GitHub Codespaces** | GA (Microsoft) | Cloud dev environments | Human-facing, no agent API, 30-sec+ boot |
| **Fly.io / Railway / Render** | Series A–B | PaaS deployment | Designed for web services, not agent sessions; no snapshotting |
| **Google Vertex AI (Code Interpreter)** | Beta | Managed code execution within Gemini | Locked to Gemini ecosystem, no SDK, walled garden |
| **Cloudflare Workers** | GA | Edge serverless | V8 isolates only, no Linux environment, extreme resource constraints |

**What are the incumbents missing?**

The hyperscalers (AWS, GCP, Azure) are missing the use-case recognition. Lambda, Cloud Functions, and Azure Functions were designed for event-driven microservices. They have not invested in the agent-centric primitives (snapshotting, millisecond resume, agent-native APIs) because their primary customers are still building serverless web backends. AI agent infrastructure is a rounding error in their roadmaps.

The developer tools (Codespaces, Daytona) are missing the machine-consumer orientation. Their UX is built for human developers: browser-based IDEs, SSH tunnels, git integrations. These are the wrong abstractions for an LLM orchestrator.

**Who are the new entrants?**

- **e2b** is our most direct competitor and the one we watch most closely. They are moving from code execution toward a broader "cloud sandbox" pitch, but remain limited by their gVisor architecture (no full OS, no snapshotting) and their small engineering team.
- **Anthropic and OpenAI** could build native sandboxes for their own agents (Anthropic already has "computer use" with some cloud execution). We view this as a risk and a validation signal. Our bet: the market will remain multi-model and AI teams will want provider-agnostic infrastructure.
- **Large infrastructure companies (HashiCorp, Pulumi)** could reorient toward this use case, but their organizational incentives favor broad IaC platforms, not deep, specialized agent sandboxes.

---

## Market Sizing

### TAM — Total Addressable Market

The TAM is the global market for **AI agent compute infrastructure**, which we define as compute, storage, and networking spending specifically attributable to AI agent workloads (as opposed to training or inference serving).

- AI infrastructure spend (all categories): $52B in 2025 (IDC estimate), growing at ~65% YoY.
- Agent-specific compute: We estimate agent workloads represent ~8% of AI infrastructure spend today, growing to ~22% by 2027 as agents proliferate. This yields a 2025 agent-compute TAM of ~**$4.2B**, growing to ~**$14B by 2027**.
- Sandstorm's TAM includes self-hosted alternatives (teams that would otherwise build internally) — that engineering labor is also TAM we are capturing.

**TAM: $4.2B (2025) → $14B (2027)**

### SAM — Serviceable Addressable Market

We serve software companies that:
1. Have at least one engineering team building AI agents in production.
2. Are willing to use a managed cloud service (vs. self-host).
3. Are headquartered in North America or Western Europe (our initial geo).

Based on: ~18,000 companies with active AI engineering teams in NA/EU (LinkedIn, Crunchbase, YC alumni data), average infrastructure spend of $50K–$400K/year per team on cloud compute for agents, and a managed-service adoption rate of ~40%:

**SAM: ~$720M (2025) → ~$2.4B (2027)**

### SOM — Serviceable Obtainable Market

Realistic 3-year market share for Sandstorm given our GTM motion, team size, and competitive dynamics:

- Year 1 (2025): 40 paying customers, $1.2M ARR → **SOM: ~0.17% of SAM**
- Year 2 (2026): 180 paying customers, $6.8M ARR → **SOM: ~0.9% of SAM**
- Year 3 (2027): 500 paying customers, $22M ARR → **SOM: ~0.9% of SAM (growing)**

These are conservative estimates based on comparable infrastructure companies' early growth rates (e.g., Modal reached $5M ARR in 18 months; Fly.io reached $10M ARR in 24 months).

---

## Pricing Benchmarks

Current market pricing for comparable compute:
- **AWS Lambda:** $0.0000166667/GB-second + $0.20/1M requests. Minimum billing: 1ms. But: cannot run persistent stateful agent sessions.
- **Modal:** ~$0.000054/vCPU-second + $0.000009/GB-second. No snapshot pricing.
- **e2b:** $0.10–$0.19/hour flat rate per sandbox. No granular billing.
- **GitHub Actions:** $0.008/minute (Linux, 2-core). Minimum: 1 minute. $0.48/hour effective.
- **Render:** $0.000231/vCPU-second ($0.0139/minute). General PaaS.

**Sandstorm pricing:**
- **Compute:** $0.000048/vCPU-second (2 vCPU default: $0.000096/second, $0.346/hour). Competitive with Modal, 60% cheaper than GitHub Actions effective rate for agent workloads.
- **Memory:** $0.000008/GB-second (4GB default: $0.000032/second).
- **Snapshots:** $0.025/GB stored/month (snapshot deltas; our compression makes average snapshot delta ~40MB = $0.001/snapshot/month). Free to create and restore.
- **Bandwidth:** $0.09/GB egress (waived for first 10GB/month per account).
- **Minimum billing unit:** 100ms. No monthly minimums.

Blended effective rates for common workloads:
- 1-minute coding agent run (2 vCPU, 4GB): ~$0.014
- 10-minute research agent with browser (2 vCPU, 8GB): ~$0.12
- 24-hour persistent dev environment (2 vCPU, 8GB, paused 16hr): ~$0.69

---

## Buyer Behavior

**Purchase process:** Sandstorm is a developer-led, bottom-up product. Initial adoption is driven by an individual engineer (Staff+ or Senior) trying the free tier on a personal project or a small eval pipeline. Paid conversion happens when the team moves a production agent workflow onto Sandstorm. Enterprise agreements ($5K+/month) require a legal review and security questionnaire from the InfoSec team. Average time from first API call to paid: 11 days. Average time from paid to expansion: 3 months.

**Budget owner:** Initially the individual engineer's AWS credit card or the team's cloud budget. For accounts above $1K/month: Engineering VP or Head of AI Platform. For enterprise accounts ($5K+/month): CTO or VP Engineering with InfoSec sign-off.

**Evaluation criteria:** Latency (cold start and snapshot resume), API completeness (does it support our framework?), security posture (network isolation, secret management), pricing predictability, SLA, and support responsiveness.

**Willingness to pay:** Our design partner interviews surfaced clear willingness-to-pay signals at $2,500–$8,000/month for mid-size teams. Extrapolating from compute usage in pilots, these teams are replacing $400–$1,200/month of AWS spend + ~$8,000–$25,000/month of engineering labor (amortized over the year). The ROI story is strongly positive.

---

## Category Trends

1. **Agents in production are the new normal.** YC W25 had 42% of companies describe themselves as building agents. The cohort from two years ago: ~5%. Agent infrastructure is now a standard line item.
2. **LLM providers are democratizing model access, creating demand for everything else.** As the model layer commoditizes (OpenAI, Anthropic, Google competing on API price), the value migrates to infrastructure (orchestration, sandboxing, observability) and applications. Sandstorm is positioned exactly in this migration zone.
3. **Security regulation is tightening.** EU AI Act (in force Aug 2024) and US Executive Order on AI (Oct 2023) both require audit trails and isolation for AI systems touching sensitive data. Sandstorm's full isolation and audit logging are a compliance answer out of the box.
4. **Benchmark-driven development is emerging.** Teams now run 100s–1000s of agent evals per day to measure quality. Each eval requires a fresh, reproducible environment. Sandstorm's snapshot primitive is the only way to run reproducible evals at scale.

---

## Market Timing Rationale

**Why 2025 and not 2022 or 2028?**

**Too early in 2022:** AI agents were not in production. LangChain launched in October 2022 and did not reach 10K GitHub stars until early 2023. There were no paying customers for this product.

**Too late in 2028:** The hyperscalers will have noticed this market and will have shipped sandboxed execution environments as part of their AI platform offerings (AWS Bedrock Agents, GCP Vertex AI Agents, Azure AI Studio). Category definition becomes much harder. The window for an independent infrastructure company to win category leadership closes as hyperscaler bundling kicks in.

**Right now in 2025:** Agents are in production but the infrastructure has not caught up. AWS has not shipped a purpose-built agent sandbox. The community of AI engineers is large enough to drive bottom-up adoption but small enough to target efficiently. The open-source infrastructure (Firecracker, containerd, gVisor) is mature enough to build on. The regulatory tailwinds are nascent but real. This is the window.
