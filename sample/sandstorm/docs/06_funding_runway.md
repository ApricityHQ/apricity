# Funding & Runway

## Use of Funds

**How will you allocate the next round?**

Sandstorm is raising a **$12M Series A** to execute the following allocation over 18 months (Q2 2025–Q4 2026):

| Category | Amount | % of Round | Rationale |
|---|---|---|---|
| Engineering headcount | $5.4M | 45% | 8 engineering hires (infra, security, backend, SDK) |
| Infrastructure (bare-metal) | $2.4M | 20% | Double fleet to 96 servers; expand to AWS `us-east-1` PoP for latency coverage |
| Sales & Marketing | $1.8M | 15% | 2 AEs, 1 developer advocate, 1 marketing manager, demand-gen budget |
| Product & Design | $0.6M | 5% | 1 PM hire (Amara scales to VP Product), 1 designer, user research budget |
| G&A (legal, finance, HR, ops) | $0.6M | 5% | Part-time CFO, HR platform, legal (SOC 2 audit, contracts) |
| Buffer / Contingency | $1.2M | 10% | 3 months of operating buffer against plan variance |

**What are the key hires?**

Priority 1 (Q2–Q3 2025): Senior Infrastructure Engineer (bare-metal ops), Security Engineer, Developer Advocate.
Priority 2 (Q3–Q4 2025): Account Executive (Enterprise), Senior Backend Engineer (control plane), Product Designer.
Priority 3 (Q1–Q2 2026): Data Engineer, Senior SDK Engineer (Go), Second AE (East Coast or London), DevOps/SRE.

Total planned headcount by end of Series A deployment: 22 FTE (up from 6 today).

**What are the product milestones?**

With the Series A, Sandstorm will:
1. **GA Launch (June 2025):** Remove waitlist; open self-serve sign-up with Stripe billing; publish pricing page. Target: 300 self-serve accounts by end of Q2 2025.
2. **SOC 2 Type I (Q3 2025):** Complete audit; publish trust report; unlock enterprise sales.
3. **Windows/macOS sandbox environments (Q3 2025):** Expand beyond Linux to support agents that need browser automation on Windows or macOS testing — a top requested feature from design partners.
4. **Persistent Workspaces (Q4 2025):** Long-running environments that survive across agent sessions, with background snapshot-on-idle. Unlocks the "persistent dev assistant" use case.
5. **Multi-region GA (Q1 2026):** Expand to EU (Frankfurt already soft-launched) and ap-southeast-1 (Singapore). Required for GDPR-compliant enterprise accounts.

---

## Milestones

**What will you achieve with this funding?**

| Milestone | Target Date | Metric |
|---|---|---|
| GA launch | June 2025 | 300 self-serve accounts |
| $150K MRR | September 2025 | ~$1.8M ARR run rate |
| SOC 2 Type I | October 2025 | Audit complete |
| First enterprise account ($5K+/month) | Q3 2025 | Signed contract |
| $400K MRR | March 2026 | ~$4.8M ARR run rate |
| Series B fundraise ready | Q4 2026 | $800K MRR, 3× YoY growth |

**What is the next valuation inflexion point?**

Series B readiness at $800K+ MRR ($9.6M+ ARR) with 3× YoY growth and 3+ enterprise design partners at $10K+/month. Expected to command a $60–80M pre-money valuation based on comparable infrastructure companies at similar ARR milestones (Modal's Series B: $16M ARR, ~$240M valuation; Railway: ~$10M ARR, ~$100M valuation — though both are at different growth inflexion points).

**What is the timeline?**

Series A close: June 2025 (currently in process; term sheet from Accel signed; co-lead from Gradient Ventures participating pro-rata).
Deployment period: 18 months (June 2025–December 2026).
Series B raise: Q1 2027 (targeting $20M–$30M on $70M+ pre-money).

---

## Financial Summary

### Amount Raised to Date

**Pre-Seed:** $2.1M total raised (closed October 2024)
- Lead: Gradient Ventures ($1.0M)
- Angels: Elad Gil ($300K), Zack Kanter ($200K), co-founder of Vercel ($200K), co-founder of Fly.io ($150K), other angels ($250K combined)
- Instrument: SAFE, $8M post-money cap, MFN

**Series A:** $12M targeted (in process; Accel term sheet signed March 2025)
- Lead: Accel ($8M)
- Co-lead: Gradient Ventures pro-rata ($2M)
- Syndicate ($2M remaining; conversations with Bessemer, General Catalyst)

### Current Burn

Monthly burn rate (March 2025): **$148,000/month**
- Payroll (6 FTE + benefits): $94,000
- Infrastructure (colocation, hardware amortization, S3): $32,000
- G&A (legal, accounting, tools, office): $14,000
- Sales & Marketing: $8,000

Projected burn post–Series A close (July 2025): **$620,000/month**
- Payroll (14 FTE): $380,000
- Infrastructure: $120,000
- Sales & Marketing: $70,000
- G&A: $50,000

### Cash Balance

Current cash (March 2025): **$1.87M**

### Runway

At current burn ($148K/month): **12.6 months** (through ~April 2026) — independent of Series A close.
Post–Series A ($12M raised, burn ramps to $620K/month): **~22 months** runway from Series A close.

### Revenue Model

Sandstorm monetizes through **usage-based compute consumption** (primary) and **enterprise seat licensing** (secondary, planned Q4 2025).

**Primary (Usage):** Customers pay per vCPU-second and per GB-RAM-second consumed by running environments. Charges also apply for snapshot storage (per GB) and egress (per GB). No monthly minimum on self-serve tier. Minimum monthly commitment of $1,000 on team tier; $5,000 on enterprise tier.

**Secondary (Enterprise SLA Seats):** Enterprise accounts pay a monthly platform fee ($2,500–$10,000/month depending on seats) in addition to usage charges. This fee covers: dedicated support SLA, SSO/SAML, audit logging export, SOC 2 report access, SLA uptime guarantee (99.95%).

### Pricing (Current)

| Resource | Rate |
|---|---|
| vCPU (per second) | $0.000048 |
| RAM (per GB-second) | $0.000008 |
| Snapshot storage (per GB-month) | $0.025 |
| Egress (per GB, 10GB free/month) | $0.090 |
| Team tier (minimum) | $1,000/month |
| Enterprise platform fee | $2,500–$10,000/month |

### 24-Month Revenue Forecast

| Month | MRR | Accounts | Notes |
|---|---|---|---|
| Apr 2025 (today) | $31K | 8 | Design partner pilots only |
| Jun 2025 | $65K | 75 | GA launch, self-serve opens |
| Sep 2025 | $150K | 220 | First enterprise close |
| Dec 2025 | $260K | 380 | SOC 2 complete; 3 enterprise accounts |
| Mar 2026 | $400K | 550 | Series B prep begins |
| Jun 2026 | $560K | 720 | EU GA, multi-region |
| Sep 2026 | $720K | 900 | 10+ enterprise accounts |
| Dec 2026 | $880K | 1,100 | Target for Series B raise |

### Forecast Assumptions

1. **Average revenue per self-serve account:** $620/month (based on pilot consumption data; design partners average $3,875/month but are heavier users than typical self-serve).
2. **Enterprise accounts:** Defined as $5,000+/month commitment. Target: 3 by Dec 2025, 10+ by Dec 2026.
3. **Self-serve conversion rate from free trial to paid:** 22% (based on comparable developer tools: Fly.io: 18%, Render: 24%).
4. **Monthly account churn:** 2.5% (early assumption; need 6+ months of cohort data to validate).
5. **Net revenue retention:** 115% (expansion within accounts outpaces churn — consistent with usage-based infrastructure products).
6. **Gross margin:** 62% at current scale; targeting 72% at $5M ARR as infrastructure utilization improves.
7. **CAC:** $4,200 blended (self-serve: $800 via community/content; enterprise: $18,000 via founder-led sales).

### Planned Round

- **Size:** $12M Series A
- **Instrument:** Priced equity round (Series A Preferred stock)
- **Pre-money valuation:** $28M (Accel term sheet)
- **Post-money valuation:** $40M
- **Lead:** Accel Partners
- **Co-lead:** Gradient Ventures (pro-rata)
- **Close target:** June 2025
- **Use of proceeds:** Per allocation table above (18-month deployment)

### Scenario Planning

**Bear Case (60% probability assigned):** Self-serve conversion is 15% (not 22%); enterprise sales cycle takes 6 months instead of 3; churn is 4%/month. Result: $400K MRR by Dec 2026. Series B still achievable but at lower valuation ($50M pre-money vs. $80M).

**Base Case (25% probability):** As forecast above. $880K MRR by Dec 2026.

**Bull Case (15% probability):** One hyperscaler partner agreement (e.g., AWS Marketplace listing drives 200 inbound accounts); enterprise sales velocity doubles. $1.4M MRR by Dec 2026.

### Break-Even Discussion

Sandstorm reaches **contribution margin break-even** on a per-account basis at account spend of ~$480/month (covers marginal infrastructure cost + allocated CAC amortized over 24 months). The median paying account is well above this level.

Full **operating break-even** (covering all fixed overhead) is not projected until ~$2.2M MRR, which is a post–Series B milestone. Sandstorm is intentionally not optimizing for break-even in the Series A period; the priority is market share and category definition while the competitor landscape is still fragmented.

### Key Financial Risks

1. **Infrastructure cost overruns:** Bare-metal capex is front-loaded. If utilization ramps slower than planned, per-unit infrastructure costs remain high and gross margin suffers.
2. **Enterprise sales cycle length:** Enterprise deals at $5K+/month take 3–9 months to close. If the cycle is consistently 6+ months, our revenue ramp lags forecast.
3. **Hyperscaler response:** If AWS ships a purpose-built agent sandbox with Firecracker internals in 2025–2026, pricing pressure intensifies and CAC rises. This is the tail risk.
4. **Key person risk:** Seo-Yeon Park (sole kernel engineer) is a single point of failure for the core runtime. Losing her would delay the roadmap by 6+ months.
