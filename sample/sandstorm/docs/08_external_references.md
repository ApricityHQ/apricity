# External References

A curated set of diligence sources for the Sandstorm investment thesis. Each reference is categorized by type and annotated with its relevance and key takeaway.

---

## Research Reports & Industry Studies

### 1. Andreessen Horowitz — "AI Infrastructure: The $50 Billion Market"
- **Type:** VC Research Report (publicly available)
- **URL:** a16z.com/ai-infrastructure-market-2025
- **Why it matters:** Top-tier VC market map that validates the AI infrastructure spend thesis. Directly cited in Sandstorm's market sizing ($52B TAM for AI infrastructure). Identifies "agent runtime compute" as an emerging subcategory.
- **Key takeaway:** AI infrastructure spend is growing at 65% YoY. The "stack" is consolidating around compute, orchestration, and observability layers — exactly the three layers Sandstorm targets at the compute end.

### 2. IDC — "Worldwide AI Infrastructure Market Forecast, 2024–2028"
- **Type:** Analyst Report (licensed; available via IDC subscription)
- **Why it matters:** Quantitative basis for the $14B agent-compute TAM estimate by 2027. IDC is the most frequently cited source in enterprise security and infrastructure RFPs — citing IDC builds credibility with InfoSec buyers.
- **Key takeaway:** AI workload compute spend grows from $52B (2025) to $142B (2028). Agentic AI is the fastest-growing subcategory.

### 3. GitHub — "The State of AI in Software Development" (Octoverse 2024)
- **Type:** Annual industry report (public)
- **URL:** github.com/octoverse
- **Why it matters:** Documents the explosion of AI-related repositories, open-source agent frameworks, and developer tool adoption. Data point: AI agent repositories grew 312% on GitHub between 2023 and 2024. Direct validation of the demand signal.
- **Key takeaway:** AI agent tooling is now the fastest-growing category on GitHub. LangChain alone has 87,000 stars.

### 4. LangSmith / LangChain — "State of AI Agents" (Q4 2024)
- **Type:** Product analytics report (public)
- **URL:** blog.langchain.dev/state-of-agents-q4-2024
- **Why it matters:** LangSmith (LangChain's observability tool) tracks production agent deployments. Data: 8× growth in traced agent runs from Q1 to Q4 2024. Real-world demand validation from the agent orchestration framework used by >60% of design partners.
- **Key takeaway:** Production agent runs exceeded 500 million in Q4 2024. The "hello world" phase is definitively over.

### 5. NIST — "Artificial Intelligence Risk Management Framework (AI RMF 1.0)"
- **Type:** Regulatory Framework (public)
- **URL:** nist.gov/aiRmf
- **Why it matters:** The NIST AI RMF is becoming the de facto standard for enterprise AI governance. Section 3.4 (Measure) and Section 3.5 (Manage) both recommend isolation, auditability, and reproducibility for AI system testing — requirements that map directly to Sandstorm's core capabilities.
- **Key takeaway:** NIST recommends that AI systems undergoing evaluation be run in isolated environments with full audit logging. Sandstorm is the only purpose-built commercial solution that satisfies these recommendations out of the box.

---

## Competitor References

### 6. e2b — Product Documentation & GitHub Repository
- **Type:** Competitor technical analysis (public)
- **URL:** e2b.dev/docs; github.com/e2b-dev/e2b
- **Why it matters:** e2b is Sandstorm's closest direct competitor. Technical analysis of their architecture (gVisor-based, Python/JS SDK only, no snapshotting) informs our differentiation narrative. Their open GitHub issues (particularly issue #847: "Implement environment snapshots") confirm they are behind us on this feature.
- **Key takeaway:** e2b's current architecture caps them at "code execution sandbox" — they cannot support full OS environments, persistent filesystem state, or snapshot-based branching without a fundamental architecture rethink.

### 7. Firecracker — Technical Documentation & GitHub
- **Type:** Open-source project (public)
- **URL:** github.com/firecracker-microvm/firecracker
- **Why it matters:** Firecracker is the open-source microVM runtime that powers Sandstorm's core. Understanding its capabilities and limitations (including snapshot API design) is essential for evaluating Sandstorm's technical claims. Priya Anand is listed as a contributor in the git log.
- **Key takeaway:** Firecracker v1.6.0 (current) supports snapshot creation in ~200ms and restore in ~400ms for standard memory footprints. Sandstorm's custom patch reduces snapshot delta sizes by 65%, enabling faster S3 uploads and faster remote restores.

### 8. Modal Labs — Pricing Page & Technical Blog
- **Type:** Competitor reference (public)
- **URL:** modal.com/pricing; modal.com/blog
- **Why it matters:** Modal is a comparable infrastructure product in terms of price point and developer-tool positioning. Their blog post on serverless GPU economics ("Why serverless GPU pricing is hard") is directly relevant to our infrastructure cost modeling. Modal's pricing page gives us a market anchor for compute pricing.
- **Key takeaway:** Modal prices compute at $0.000054/vCPU-second. Sandstorm prices at $0.000048/vCPU-second, ~11% cheaper. The more important differentiator is non-price: Modal does not offer persistent stateful environments or snapshotting.

---

## Regulatory References

### 9. EU AI Act — Corrigendum (Official Journal of the EU, 2024)
- **Type:** Regulatory Document (public)
- **URL:** eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202401689
- **Why it matters:** The EU AI Act entered into force August 1, 2024. Articles 9, 17, and 72 require high-risk AI systems to have audit logs, testing in isolated environments, and reproducible validation. EU customers (a key growth market for Sandstorm) will need compliance-grade sandbox infrastructure.
- **Key takeaway:** "High-risk AI systems shall be tested before being put into service" (Article 9.5). Sandstorm's isolated environments with full audit logging are a direct compliance answer for EU enterprise customers.

### 10. US Executive Order on AI — "Safe, Secure, and Trustworthy AI" (Oct 2023)
- **Type:** US Government Policy (public)
- **URL:** whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/
- **Why it matters:** Directionally aligns US federal policy with isolation, testing, and auditability requirements for AI systems — creating tailwind for infrastructure products like Sandstorm.
- **Key takeaway:** Section 4 of the EO mandates evaluation frameworks for AI systems. Sandstorm's reproducible eval environments are a direct implementation vehicle.

---

## Customer Interview Themes

The following themes emerged from 60 customer discovery interviews conducted between September–December 2024 by Priya and Marcus. Interviewees included: 22 AI infrastructure engineers (Series A–C companies), 14 AI startup founders, 12 enterprise AI lab leads, 12 ML platform engineers at Fortune 500 companies.

### 11. Internal Theme Report: "Why Teams Build Their Own Sandbox" (Sandstorm, Dec 2024)
- **Type:** Primary qualitative research (internal, shared with investors under NDA)
- **Why it matters:** Documents the specific reasons design partner teams chose to build internally rather than use existing solutions. Top reasons: e2b doesn't support their framework (33%); cold start latency too high for their eval loop (28%); security requirements block existing cloud solutions (22%); need for snapshot/branching (17%).
- **Key takeaway:** The top 4 pain points above are exactly what Sandstorm solves — strong product-market fit signal from first principles.

### 12. Internal Theme Report: "Enterprise Buying Criteria for AI Infrastructure" (Sandstorm, Feb 2025)
- **Type:** Primary qualitative research (internal)
- **Why it matters:** Documents the InfoSec and compliance requirements that block enterprise AI infrastructure purchases. Finding: SOC 2 Type II is a hard requirement for 85% of enterprise prospects; ISO 27001 is required for 40% of EU-based prospects.
- **Key takeaway:** Security certification is the #1 enterprise sales unlocker. Sandstorm's SOC 2 audit (in progress) is not optional — it is the enterprise revenue gate.

---

## Datasets & Market Maps

### 13. Crunchbase — AI Infrastructure Funding Landscape (2024)
- **Type:** Funding database (licensed)
- **URL:** crunchbase.com
- **Why it matters:** Documents competitive funding rounds, valuations, and investor syndicates in the agent infrastructure space. Confirms Sandstorm's $40M Series A post-money valuation is reasonable relative to e2b ($8M pre-seed, ~$30M post-money) and Modal ($30M Series B, ~$160M pre-money).
- **Key takeaway:** No well-funded direct competitor exists at the "full OS agent sandbox" level. e2b is the only VC-backed close competitor and is at seed stage.

### 14. Electric Capital — "Developer Activity in AI" (2024 Report)
- **Type:** Open-source ecosystem analysis (public)
- **URL:** developerreport.com
- **Why it matters:** Electric Capital tracks monthly active developers across AI open-source ecosystems. Shows LangChain, AutoGen, and LlamaIndex each with >10,000 monthly active contributors. Sandstorm's SDK integration strategy targets exactly these communities.
- **Key takeaway:** The AI developer ecosystem is larger and more active than any prior web3 or cloud developer wave at the same maturity point. Brand investment in this community now has outsized long-term returns.

### 15. Sequoia Capital — "AI Agents: The Third Wave" (Scout Report, 2024)
- **Type:** VC Analysis (public)
- **URL:** sequoiacap.com/article/ai-agents-2024
- **Why it matters:** Validates the agent wave thesis at a category level from a top-tier investor. Directly cited in Sandstorm investor pitch materials to establish shared vocabulary with VC audiences.
- **Key takeaway:** Sequoia projects that AI agents will handle >30% of enterprise software workflows by 2027. This demand is the direct driver of the agent infrastructure market that Sandstorm serves.
