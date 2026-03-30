# Sandstorm — Customer & Market Research Report
## Primary Research Summary | January 2025 | Confidential

**File:** sandstorm_customer_research_jan2025.pdf
**Purpose:** Primary qualitative research summarizing 60 customer discovery interviews and 120 survey responses. Used for product-market fit validation, GTM strategy, and investor diligence.

---

## TABLE OF CONTENTS

1. Research Objective
2. Methodology
3. Interview Sample Profile
4. Customer Segments
5. Pain Points (Ranked)
6. Buying Triggers
7. Budget Insights
8. Competitive Perceptions
9. Adoption Blockers
10. Key Implications for Product & GTM

---

## 1. RESEARCH OBJECTIVE

This research was commissioned by Priya Anand (CEO) and Amara Diallo (Head of Product) to answer four questions before committing to a product architecture and go-to-market:

1. **Is the problem real and acute?** Do AI engineering teams genuinely struggle with agent sandbox infrastructure, or is it a minor inconvenience?
2. **Who suffers most?** Which company type, roles, and use cases represent the highest-pain, highest-willingness-to-pay segment?
3. **What does a winning solution look like?** What capabilities are must-haves vs. nice-to-haves? What does good feel like?
4. **What will prevent adoption?** What security, compliance, economic, or workflow objections will we face?

Research was conducted between September 15 and December 20, 2024. All interviewees were recruited via personal network (Priya and Marcus's combined networks at AWS, Cohere, Modal, LangChain, Stripe, Google) with a deliberate effort to include participants outside the first-degree network to avoid confirmation bias.

---

## 2. METHODOLOGY

### Phase 1: Qualitative Interviews (Primary)

- **Format:** 30–45 minute semi-structured video calls (Zoom or Google Meet)
- **Interviewers:** Priya Anand (33 interviews), Marcus Webb (27 interviews)
- **Sample:** 60 interviews total
- **Recording:** All sessions recorded with participant consent; transcribed via Whisper + manual review
- **Analysis:** Thematic coding using Dovetail (affinity mapping, frequency analysis)
- **Bias mitigation:** 25 interviews were conducted with participants who had never heard of Sandstorm (they were told it was general AI infrastructure research)

### Phase 2: Quantitative Survey (Secondary)

- **Format:** 22-question online survey (Typeform)
- **Distribution:** Shared in LangChain Discord, AI engineering Slack communities, LinkedIn (Priya and Marcus's combined audience)
- **Sample:** 120 valid responses (screened for: working on AI agents in a professional context, at least one agent deployed or in active development)
- **Analysis:** Descriptive statistics + cross-tabulation by company stage and role

### Phase 3: Design Partner Workshops (Validation)

- **Format:** 90-minute working sessions with 8 design partners
- **Purpose:** Validate specific product decisions (API design, pricing, template library), not general discovery
- **Output:** Feature prioritization matrix and API naming conventions (not in scope for this report)

---

## 3. INTERVIEW SAMPLE PROFILE

### By Role

| Role | Count | % |
|---|---|---|
| AI Infrastructure Engineer / Platform Engineer | 22 | 37% |
| ML Engineer / AI Engineer | 14 | 23% |
| Engineering Manager / Head of AI Platform | 12 | 20% |
| Founder / CTO (AI startup) | 8 | 13% |
| Enterprise AI Lab Lead | 4 | 7% |

### By Company Stage

| Stage | Count | % |
|---|---|---|
| Seed / Pre-seed | 10 | 17% |
| Series A | 16 | 27% |
| Series B | 14 | 23% |
| Series C+ | 8 | 13% |
| Fortune 500 / Enterprise | 12 | 20% |

### By Industry (Top 5)

| Industry | Count | % |
|---|---|---|
| AI-native software | 28 | 47% |
| Financial services | 10 | 17% |
| Healthcare / biotech | 6 | 10% |
| Enterprise software / SaaS | 8 | 13% |
| Logistics / operations | 4 | 7% |
| Other | 4 | 7% |

### By Agent Type (Primary Use Case)

| Agent Type | Count | % |
|---|---|---|
| Coding / code generation agents | 20 | 33% |
| Data pipeline / ETL agents | 14 | 23% |
| Research / web scraping agents | 12 | 20% |
| Customer support / NLP agents | 8 | 13% |
| Internal operations / HR/Finance agents | 6 | 10% |

---

## 4. CUSTOMER SEGMENTS

From the qualitative analysis, three distinct customer archetypes emerged. Each has a different pain intensity, buying motion, and willingness to pay.

### Segment A: "The Scaling Builders" (37% of interviews)

**Profile:** AI-native startup, Series A–B, 3–8 AI engineers. Has shipped at least one agent to production. Is actively scaling the number of agents and the eval pipeline. Hit the sandbox wall hard — currently spending significant engineering time on infrastructure.

**Representative quote:**
> *"We have a senior engineer who basically owns our eval infrastructure. It's become his full-time job. Every time we change a dependency or update a model, something breaks. We've spent probably 400 engineering hours on this in the last 6 months."*
> — Head of AI Platform, Series B coding agent startup

**Pain intensity:** Highest. Every eval loop is bottlenecked by sandbox performance. Every new agent requires infrastructure work.

**WTP:** $3,000–$10,000/month. Decision maker is Head of AI Platform or CTO, no procurement process required. Pays on a personal or team credit card initially.

**Key jobs to be done:** Fast eval loops, reproducible environments, minimal infrastructure maintenance.

### Segment B: "The Enterprise Adopters" (33% of interviews)

**Profile:** Fortune 500 or Series C+ company with a dedicated AI innovation lab or internal AI platform team. Has 1–3 agents in pilot phase; moving cautiously toward production. Has extensive security, compliance, and vendor review requirements.

**Representative quote:**
> *"We can't just plug in a vendor API to our production systems without going through our security review. That takes 3–6 months. But if you're SOC 2 certified, that process moves much faster. It's table stakes."*
> — AI Lab Lead, Fortune 500 financial services company

**Pain intensity:** Medium. The pain exists, but they tolerate it better because they have more engineering resources. The blocker is often security/compliance, not purely technical.

**WTP:** $5,000–$20,000/month. Procurement process required; legal review of MSA; InfoSec review mandatory.

**Key jobs to be done:** Security compliance (SOC 2, ISO 27001), audit logging, data residency, SLA guarantees.

### Segment C: "The Indie AI Engineers" (30% of interviews)

**Profile:** Individual developer or very small team (2–3 people) building an AI product. Using off-the-shelf frameworks (LangChain, LlamaIndex). Constraints: low budget, no infrastructure expertise, high time sensitivity.

**Representative quote:**
> *"I'm building a product by myself and I spend way too much time on environment management. I just want something that works. I'm not going to build my own dockerfile for every eval."*
> — Founder, solo-founder AI startup

**Pain intensity:** High individually, but lower willingness to pay and shorter eval loop requirements.

**WTP:** $50–$500/month. Self-service, no sales required. Extremely price-sensitive.

**Key jobs to be done:** Zero-setup, just works, cheap for low-volume use, great documentation.

**GTM implication:** Segment C drives adoption (volume) and word-of-mouth, but Segment A drives revenue and growth. Segment B is the enterprise expansion play post–SOC 2.

---

## 5. PAIN POINTS (RANKED BY FREQUENCY AND INTENSITY)

*Based on affinity mapping of 60 interviews. Frequency = % of interviews where this theme appeared unprompted. Intensity = average 1–5 rating when prompted.*

| Rank | Pain Point | Freq. | Intensity (1–5) | Representative Quote |
|---|---|---|---|---|
| 1 | Slow environment boot / eval loop latency | 92% | 4.7 | *"45 seconds per eval run means I can't iterate fast enough. I run 200 evals a day. That's 2.5 hours of waiting."* |
| 2 | Reproducibility — environment drift between runs | 83% | 4.5 | *"We had an eval pipeline that passed for 3 weeks then started failing. Turned out a dependency auto-updated in the base image. Took a week to debug."* |
| 3 | Maintenance burden of internal sandbox infra | 78% | 4.3 | *"I built our sandbox in 3 weeks. I've spent 2× that maintaining it. It's a tax I pay every sprint."* |
| 4 | No snapshot / replay capability for debugging | 68% | 4.1 | *"When an agent fails in production, I can't replay it. The environment is gone. I'm debugging from logs, which is horrible."* |
| 5 | Security concerns (agent running in same env as production secrets) | 67% | 4.4 | *"Our agents have access to our production database for testing. That terrifies me but it's the path of least resistance."* |
| 6 | Cost of idle compute between agent runs | 58% | 3.9 | *"I'm paying for 24/7 EC2 instances that are used maybe 20% of the time. But I can't afford the cold start of spinning them up fresh."* |
| 7 | No native API for agent orchestration frameworks | 52% | 3.7 | *"I had to write a custom wrapper to get LangChain to talk to our Docker setup. It's 300 lines of glue code."* |
| 8 | Difficulty running browser / UI agents | 44% | 3.8 | *"Running Playwright inside a container that's inside Kubernetes is a nightmare. Three layers of networking problems."* |
| 9 | Multi-step agent state management | 40% | 3.6 | *"If my agent fails on step 7 of a 10-step process, I have to restart from step 1. There's no checkpoint/resume."* |
| 10 | Compliance and audit logging for agent actions | 38% | 3.9 | *"Our InfoSec team wants a full audit trail of every command our agents run. I have to build that by hand today."* |

---

## 6. BUYING TRIGGERS

From the 60 interviews, the following events were identified as the most reliable triggers that move an engineering team from "tolerate the pain" to "actively evaluate solutions":

### Trigger 1: Eval Pipeline Becomes a Blocker (60% of Segment A)
Teams start evaluating solutions the moment their evaluation loop becomes the bottleneck on their product iteration speed. The specific tipping point: when the team's dev cycle is constrained by "waiting for evals" rather than "writing code."

**Signal to watch for in sales:** Ask "how long does your eval loop take?" If answer is >10 minutes: high intent. If >30 minutes: very high intent.

### Trigger 2: Production Incident Caused by Environment Issue (45% of all segments)
A production failure directly attributable to the internal sandbox (environment drift, dependency conflict, shared-state contamination) is a reliable forcing function. Teams that have experienced such an incident are 3× more likely to evaluate external solutions within 30 days.

**Sales implication:** Ask about recent production incidents. "Have you had a failure you couldn't replay or debug?"

### Trigger 3: New AI Engineer Hire Complains (38% of Segment A)
When a new hire (especially a senior engineer) joins and immediately identifies the internal sandbox as "terrible" relative to what they used at their previous employer, leadership pays attention. New hires are more likely to have context from companies that have already solved this with Sandstorm or similar tools.

### Trigger 4: Security or Compliance Review (72% of Segment B)
Enterprise teams only start the vendor evaluation process after receiving a security review request from their InfoSec team or an audit finding related to agent isolation. The compliance event creates organizational urgency that individual engineering pain cannot.

### Trigger 5: Competitor Mentions Using Better Infrastructure (30% of all)
When a competitor publishes a blog post or social media content mentioning their agent eval speed (e.g., "we run 1,000 evals in 10 minutes"), teams feel pressure to match. This is an indirect trigger for Sandstorm.

---

## 7. BUDGET INSIGHTS

### Monthly Willingness to Pay (WTP) by Segment

| Segment | Min WTP | Max WTP | Median WTP | Decision Maker |
|---|---|---|---|---|
| A: Scaling Builders | $1,000 | $12,000 | $3,800 | Head of AI Platform / CTO |
| B: Enterprise Adopters | $5,000 | $25,000 | $9,500 | VP Engineering / CTO + InfoSec |
| C: Indie AI Engineers | $0 | $500 | $120 | Individual engineer |

**Key finding:** WTP correlates strongly with team eval run volume, not company size. A 10-person startup running 500 evals/day has higher WTP than a 200-person company running 50 evals/day.

### Existing Infrastructure Spend (What They're Currently Paying)

When asked about their current monthly spend on agent-related compute infrastructure:

| Spend Range | % of Respondents |
|---|---|
| <$500/month | 22% |
| $500–$2,000/month | 30% |
| $2,000–$8,000/month | 28% |
| $8,000–$25,000/month | 14% |
| >$25,000/month | 6% |

**Key finding:** 48% of interviewees spend more than $2,000/month on agent infrastructure today. The opportunity to replace or supplement this spend is large.

### Engineering Time Spent on Sandbox Infrastructure

When asked to estimate engineering hours per month spent maintaining internal sandbox infrastructure (self-reported, all segments):

| Hours/Month | % of Respondents |
|---|---|
| <5 hours | 18% |
| 5–20 hours | 32% |
| 20–80 hours | 30% |
| >80 hours (near full-time) | 20% |

**Cost of engineering time (median $185K/yr fully-loaded SF engineer):**
- Median respondent: 20–30 hours/month = ~$2,150–$3,200/month in engineering labor
- At a $300/month Sandstorm bill, the ROI argument is ~7–10×

---

## 8. COMPETITIVE PERCEPTIONS

### Awareness of Existing Solutions

When asked "what do you currently use for agent sandboxing?":

| Solution | % Using | Satisfaction (1–5) |
|---|---|---|
| Docker + Kubernetes (self-managed) | 62% | 2.8 |
| GitHub Actions / GitLab CI | 48% | 2.4 |
| AWS Lambda | 22% | 2.1 |
| e2b | 18% | 3.4 |
| Modal | 12% | 3.6 |
| Nothing structured / ad hoc | 15% | N/A |

**Key finding:** e2b has the highest satisfaction score among existing solutions (3.4/5), which validates the space but also shows significant room for improvement (no one is "delighted"). Docker + Kubernetes is the most common but least satisfying solution.

### Perceptions of e2b (Primary Competitor)

| Perception Theme | Frequency |
|---|---|
| "Limited to Python/JS only" | 63% of e2b users |
| "Can't run a full OS environment" | 58% |
| "No snapshotting / can't replay sessions" | 52% |
| "Good for simple code execution, not complex agents" | 71% |
| "Pricing is reasonable but unpredictable" | 44% |
| "API is clean and easy to use" (positive) | 80% |

**Sandstorm positioning implication:** e2b's API is respected. Our API design must match or exceed e2b's developer experience. Our differentiation is in capability (full OS, snapshotting, browser) and performance (sub-800ms boot), not API design.

### Perception of AWS Lambda for Agent Sandboxing

| Perception Theme | Frequency |
|---|---|
| "15-minute limit is a real problem for long agents" | 78% |
| "Read-only filesystem is a deal-breaker" | 70% |
| "Not designed for this use case" | 88% |
| "We use it anyway because it's familiar" | 45% |

---

## 9. ADOPTION BLOCKERS

These are the objections that will delay or prevent a team from adopting Sandstorm, ranked by frequency:

### Blocker 1: Security / Trust (62% of Segment B, 28% overall)

*"You're asking me to run my agents — which may have access to our production data — on a third-party infrastructure. Before I do that, I need to see your SOC 2 report."*

**Implication:** SOC 2 Type I is a hard gate for enterprise adoption. Without it, Segment B accounts will not sign. Timeline: Sandstorm's SOC 2 Type I is targeted for Q3 2025.

### Blocker 2: Pricing Uncertainty (44% overall)

*"I love the usage-based model in principle, but I need to be able to budget. If my agents go haywire, do I get a massive unexpected bill?"*

**Implication:** Need a spend cap feature (alert + automatic pause at a configurable monthly spend limit). This is on the Q2 2025 roadmap. Currently mitigated with per-account egress limits.

### Blocker 3: Vendor Lock-In (38% overall)

*"I don't want to rewrite all my agent code when I switch providers in the future."*

**Implication:** Sandstorm's API must allow easy egress — we should publish migration guides to/from e2b and self-hosted Docker. Paradoxically, reducing vendor lock-in perception increases adoption (trust signal).

### Blocker 4: "We're already too far invested in our internal solution" (32% of Segment A)

*"We've spent 3 months building our sandbox. It's not perfect but it works. I can't justify switching now."*

**Implication:** The migration story matters. We need a clear migration path (e.g., drop-in LangChain tool replacement) that lets teams test Sandstorm on a subset of workloads without a full commitment.

### Blocker 5: Data Residency / Sovereignty (28% of Segment B, especially EU)

*"We handle customer data in our agents. That data cannot leave the EU."*

**Implication:** EU data residency (Equinix FR5 with strict data residency configuration) is a prerequisite for EU enterprise accounts. Currently available in soft launch; GA in Q2 2025.

### Blocker 6: "What if Sandstorm shuts down?" (24% overall)

*"You're a seed-stage startup. What happens to my production agents if you run out of money?"*

**Implication:** Escrow the source code with a third-party (GitHub + Escrow.com). Publish an explicit shutdown playbook. After Series A close, the "startup risk" objection will have less weight — investors provide implicit endorsement of viability.

---

## 10. KEY IMPLICATIONS FOR PRODUCT & GTM

### Product Implications

**P0 — Must ship by GA:**
1. **Spend cap / budget alerts:** Hard limit feature to prevent bill shock (Blocker #2). Every account needs configurable monthly spend maximum with automated pause.
2. **Data residency UI:** Self-serve ability to select data residency region at environment creation (required for EU accounts, Blocker #5).
3. **Migration guides:** LangChain and AutoGen migration guides from Docker/k8s and e2b.

**P1 — Ship by Q3 2025:**
4. **SOC 2 report availability:** Available in-dashboard for enterprise accounts (Blocker #1).
5. **Audit log export:** SIEM integration for enterprise (Blocker #1 for highly-regulated industries).
6. **Multi-step agent checkpoint UI:** Dashboard view of snapshot tree for debugging failed multi-step agent runs (Pain Point #4).

**P2 — Roadmap:**
7. **Browser agent templates:** Pre-configured Ubuntu + Chromium template with one-click setup (Pain Point #8).
8. **Egress whitelist UI:** GUI for configuring network egress policy (security-conscious Segment B).

### GTM Implications

**Target Segment A first.** The "Scaling Builder" segment has the highest pain intensity, the fastest buying cycle (no procurement), and the strongest product-market fit signal. They also generate the word-of-mouth that attracts Segment C (indie engineers) and puts Sandstorm on Segment B's radar.

**Use eval speed as the hook.** Every outbound message, every blog post, every conference talk should lead with the eval loop speed story. "500 evals in 10 minutes instead of 4 hours" is the most visceral, quantitative value proposition. Pain Point #1 (slow eval loops) is the door. Everything else is the room.

**Community before paid.** All three segments trust peer recommendations overwhelmingly more than vendor marketing. The LangChain Discord, Twitter/X, and Hacker News are the acquisition channels that cost least and convert best. Prioritize community presence + framework integrations over paid advertising until $500K MRR.

**SOC 2 is the enterprise unlock.** Do not invest heavily in enterprise sales motions until Q3 2025 SOC 2 completion. Before SOC 2, enterprise conversations will stall at InfoSec review. After SOC 2, Segment B becomes fully accessible and ACV rises from $3,800 (Segment A median) to $9,500 (Segment B median).

**Pricing transparency reduces friction.** The pricing uncertainty blocker (Blocker #2) is addressable with product features (spend caps) and clear documentation. Every interviewee who said "pricing is uncertain" relaxed immediately when we explained the spend cap feature. This means the objection is real but the mitigation is easy — ship it at GA.

**The Migration Story is a Sales Tool.** Teams who are "too invested in their internal solution" (Blocker #4) often have significant tribal knowledge embedded in their internal infrastructure. The answer is not to ask them to rip out their existing system — it is to offer a side-by-side trial ("run 20% of your eval traffic through Sandstorm, 80% on your existing stack, compare results"). This lowers the cost of experimentation and generates the internal evidence teams need to justify switching.

---

## APPENDIX: REPRESENTATIVE VERBATIM QUOTES

*Selected for breadth across segments, pain points, and objections.*

> *"The thing that kills me is that when an agent fails in a weird way, I can't replay it. The environment is gone. I'm debugging from logs and it's like trying to solve a crime from a witness description."*
> — AI Infrastructure Engineer, Series B startup

> *"We ran a test where we measured eval latency. Our fastest eval takes 47 seconds. 40 of those seconds are environment setup. That's insane. We're spending 85% of eval time on infrastructure."*
> — ML Engineer, Series A company

> *"Our InfoSec team asked us to provide a full trace of every shell command our coding agent executed last week. I had to admit we don't log that. The look on their face was not good."*
> — CTO, Series A AI startup

> *"I tried e2b. It's great for simple code execution but the moment I needed to install system packages or run a browser, I hit a wall. Their gVisor sandbox just doesn't support it."*
> — Developer, indie AI product

> *"Our agents cost $4/hour to run on our current infrastructure. If a Sandstorm equivalent costs $0.30/hour and is faster, that's a 13× cost reduction. At our eval volume, that's $40K/year in savings."*
> — Engineering Manager, Series B company

> *"The thing I'm most scared of isn't cost or latency. It's a security incident. My agents have API keys. If one of them gets compromised, I need to know exactly what it did. Right now, I couldn't tell you."*
> — Head of AI Platform, Fortune 500 financial services lab

> *"When I saw the benchmark showing sub-800ms boot vs. 45 seconds for Docker, my first reaction was disbelief. My second was 'how did we not have this already?'"*
> — Staff Engineer, Series B AI-native company (now a design partner)
