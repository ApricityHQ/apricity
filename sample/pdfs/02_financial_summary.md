# Sandstorm — Financial Summary
## Series A Investor Materials | Confidential | March 2025

**File:** sandstorm_financial_summary_march2025.pdf
**Purpose:** Detailed financial model and assumptions for Series A diligence.

---

## 1. EXECUTIVE FINANCIAL SUMMARY

**Snapshot (March 31, 2025):**

| Metric | Value |
|---|---|
| MRR | $31,000 |
| ARR (run rate) | $372,000 |
| Gross Margin | 62% (modeled at GA scale; currently 7% due to infra sized for growth) |
| Monthly Burn | $148,000 |
| Cash Balance | $1,870,000 |
| Runway | 12.6 months |
| Paying Accounts | 8 (design partners) |
| Avg Revenue/Account | $3,875/month |

**Series A financing (in process):**

| Metric | Value |
|---|---|
| Round Size | $12,000,000 |
| Pre-money Valuation | $28,000,000 |
| Post-money Valuation | $40,000,000 |
| Lead Investor | Accel Partners (term sheet signed Mar 2025) |
| Target Close | June 2025 |

**24-Month Target (March 2027):**

| Metric | Target |
|---|---|
| MRR | ~$900,000 |
| ARR | ~$10,800,000 |
| Gross Margin | 72%+ |
| Paying Accounts | ~1,100+ |
| Net Revenue Retention | 115% |

---

## 2. REVENUE MODEL & PRICING ARCHITECTURE

### Revenue Streams

**Stream 1: Usage-Based Compute (Primary — 85% of revenue)**

| Resource | Unit | Price |
|---|---|---|
| vCPU | Per second | $0.000048 |
| RAM | Per GB-second | $0.000008 |
| Snapshot storage | Per GB-month | $0.025 |
| Egress | Per GB (10GB free/month) | $0.090 |

*Minimum billing unit: 100ms. No monthly minimums on self-serve tier.*

**Common workload pricing (fully loaded):**

| Workload | Duration | vCPU | RAM | Cost |
|---|---|---|---|---|
| Quick code eval | 30 seconds | 2 | 4GB | $0.007 |
| Coding agent session | 5 minutes | 2 | 4GB | $0.070 |
| Research agent (with browser) | 15 minutes | 2 | 8GB | $0.194 |
| Data pipeline agent | 60 minutes | 4 | 16GB | $1.338 |
| Eval run (pre-warmed snapshot) | 90 seconds | 2 | 4GB | $0.021 |

**Stream 2: Enterprise Platform Fee (Secondary — 15% of revenue)**

| Plan | Platform Fee | Key Features |
|---|---|---|
| Team | $1,000/month minimum | Standard SLA, email support |
| Business | $2,500/month minimum | SSO/SAML, priority support, audit logs |
| Enterprise | $5,000–$10,000/month | 99.95% SLA, dedicated Slack, SOC 2, custom MSA |

### Pricing Rationale vs. Competitors

| Provider | Effective rate (vCPU-hour) | Notes |
|---|---|---|
| Sandstorm | $0.1728 | Bare-metal, agent-native, snapshotting |
| Modal | $0.1944 | No snapshotting, no persistent FS |
| GitHub Actions | $7.20 effective | 1-min minimum; not designed for agent sessions |
| AWS Lambda | Not comparable | Stateless; 15-min limit; no FS |
| e2b | ~$0.12–0.19/hr flat | Code execution only; no snapshotting |

---

## 3. 24-MONTH REVENUE FORECAST (BASE CASE)

### Monthly Forecast Table

| Month | New Accounts | Total Active | MRR (Self-serve) | MRR (Enterprise) | MRR (Total) | Notes |
|---|---|---|---|---|---|---|
| Apr 2025 | 0 | 8 | $8,000 | $23,000 | $31,000 | Design partners only |
| May 2025 | 20 | 27 | $19,000 | $27,000 | $46,000 | Pre-GA waitlist |
| Jun 2025 | 60 | 82 | $38,000 | $27,000 | $65,000 | GA launch |
| Jul 2025 | 45 | 121 | $55,000 | $27,000 | $82,000 | Post-launch norm. |
| Aug 2025 | 40 | 153 | $72,000 | $32,000 | $104,000 | Enterprise pipeline |
| Sep 2025 | 40 | 186 | $88,000 | $62,000 | $150,000 | 3 enterprise accounts |
| Oct 2025 | 38 | 216 | $104,000 | $75,000 | $179,000 | SOC 2 Type I |
| Nov 2025 | 42 | 248 | $122,000 | $90,000 | $212,000 | |
| Dec 2025 | 42 | 280 | $140,000 | $120,000 | $260,000 | Year-end target |
| Jan 2026 | 45 | 315 | $160,000 | $140,000 | $300,000 | |
| Feb 2026 | 48 | 352 | $182,000 | $155,000 | $337,000 | |
| Mar 2026 | 52 | 392 | $206,000 | $194,000 | $400,000 | |
| Apr 2026 | 52 | 433 | $230,000 | $220,000 | $450,000 | |
| May 2026 | 55 | 476 | $258,000 | $250,000 | $508,000 | EU GA |
| Jun 2026 | 55 | 520 | $286,000 | $274,000 | $560,000 | |
| Jul 2026 | 58 | 566 | $316,000 | $290,000 | $606,000 | |
| Aug 2026 | 58 | 613 | $348,000 | $308,000 | $656,000 | |
| Sep 2026 | 60 | 662 | $380,000 | $340,000 | $720,000 | 10 enterprise accounts |
| Oct 2026 | 62 | 714 | $414,000 | $366,000 | $780,000 | |
| Nov 2026 | 62 | 766 | $450,000 | $388,000 | $838,000 | |
| Dec 2026 | 62 | 820 | $486,000 | $394,000 | $880,000 | Series B target |

### Key Forecast Assumptions

| Assumption | Value | Basis |
|---|---|---|
| Free trial → paid conversion | 22% within 30 days | Fly.io (24%), Render (24%), Railway (19%) |
| Monthly logo churn | 2.5% | Developer tool benchmarks |
| Net Revenue Retention | 115% | Usage-based infra typical range |
| Avg self-serve ACV | $620/month | Design partner consumption data × segment discount |
| Avg enterprise ACV | $6,200/month | $5K min + avg usage overage |
| GA new account rate | 45–62/month | HN (847 signups → 22% trial), organic |
| CAC (self-serve) | $800 | Twitter, Discord, framework integrations |
| CAC (enterprise) | $18,000 | Founder + AE time, 6-month sales cycle |
| Blended CAC | $4,200 | 85% self-serve + 15% enterprise |

---

## 4. CUSTOMER ACQUISITION COST (CAC) ANALYSIS

### CAC by Channel (Current)

| Channel | Accounts Sourced | Total Cost | CAC |
|---|---|---|---|
| HN Show HN | 8 | $8,800 | $1,100 |
| Discord/Community | 6 | $5,250 | $875 |
| Twitter/X threads | 12 (projected) | $660 | $55 |
| Framework integrations | 4 | $13,000 | $3,250 |
| Cold email (founder) | 1 | $8,200 | $8,200 |
| **Total / Blended** | **31** | **~$35,910** | **$1,158** |

*Current low CAC reflects founder-led, zero-spend GTM. Will increase post-GA as paid channels and AE added.*

### LTV:CAC Summary

| Scenario | Gross Margin | Avg ACV | LTV (30-month) | CAC | LTV:CAC |
|---|---|---|---|---|---|
| Current (early) | 62% | $750 | $13,950 | $1,158 | 12.0× |
| GA target | 65% | $750 | $14,625 | $4,200 | 3.5× |
| Mature (72% GM) | 72% | $800 | $17,280 | $3,500 | 4.9× |

---

## 5. GROSS MARGIN ANALYSIS

### Cost of Revenue Breakdown (at $65K MRR / GA launch)

| Item | Monthly Cost |
|---|---|
| Colocation (power, space, cross-connect) | $14,400 |
| Server depreciation | $8,000 |
| S3 storage (snapshots) | $3,200 |
| Bandwidth (egress) | $1,400 |
| Cloud monitoring (Datadog) | $1,800 |
| **COGS subtotal** | **$28,800** |

**Gross Margin at $65K MRR: 56%**

**Gross Margin Trajectory:**

| MRR Level | COGS | Gross Margin | Utilization Driver |
|---|---|---|---|
| $65K (GA) | $28,800 | 56% | ~45% avg utilization |
| $150K (Q3 2025) | $35,000 | 77% | 53% utilization |
| $260K (Dec 2025) | $55,000 | 79% | 62% utilization |
| $560K (Jun 2026) | $108,000 | 81% | 71% utilization |
| $880K (Dec 2026) | $165,000 | 81% | 74% utilization |

*Key lever: Every 10pp improvement in server utilization improves gross margin by ~3–4pp.*

---

## 6. BURN RATE & RUNWAY

### Current Monthly Burn (March 2025)

| Category | Monthly | Annual |
|---|---|---|
| Payroll + benefits (6 FTE) | $94,000 | $1,128,000 |
| Infrastructure (CoLo + hardware) | $32,000 | $384,000 |
| G&A (legal, tools, office) | $14,000 | $168,000 |
| Sales & Marketing | $8,000 | $96,000 |
| **Total** | **$148,000** | **$1,776,000** |

**Cash:** $1,870,000 → **Runway: 12.6 months** (through April 2026)

### Post-Series A Burn Ramp

| Period | Monthly Burn | Cumulative (from July 2025) |
|---|---|---|
| Jul 2025 | $380,000 | $380,000 |
| Aug–Dec 2025 | $480,000 | $2,780,000 |
| Jan–Jun 2026 | $580,000 | $6,260,000 |
| Jul–Dec 2026 | $640,000 | $10,100,000 |

**$12M Series A − $10.1M = $1.9M buffer at Dec 2026** before revenue contribution.
By Dec 2026: $880K MRR × 81% GM = $713K gross profit/month → series B fully funded by operations.

---

## 7. HIRING PLAN & HEADCOUNT COST

| Role | Start | Base | Fully-Loaded (1.25×) |
|---|---|---|---|
| Sr. Infra Eng. (bare-metal) | Q2 2025 | $190K | $237,500 |
| Developer Advocate | Q2 2025 | $155K | $193,750 |
| Account Executive | Q3 2025 | $140K + $80K OTE | $275,000 |
| Product Designer | Q3 2025 | $145K | $181,250 |
| Security Engineer | Q3 2025 | $195K | $243,750 |
| Sr. Backend Engineer | Q4 2025 | $185K | $231,250 |
| Data Engineer | Q1 2026 | $170K | $212,500 |
| Sr. SDK Engineer (Go) | Q1 2026 | $190K | $237,500 |
| AE #2 | Q2 2026 | $140K + $80K OTE | $275,000 |
| DevOps/SRE | Q2 2026 | $185K | $231,250 |
| Marketing Manager | Q3 2026 | $145K | $181,250 |
| Sr. Infra Engineer #2 | Q3 2026 | $190K | $237,500 |
| **Full run rate (all 12 new hires)** | | | **$2,737,500/yr** |

*Current team (6 FTE): $1,128,000/yr. Total at 22 FTE: ~$3,865,000/yr = $322,000/month.*

---

## 8. SCENARIO PLANNING

| Metric | Bear (30%) | Base (50%) | Bull (20%) |
|---|---|---|---|
| Conversion rate | 15% | 22% | 28% |
| Monthly churn | 4% | 2.5% | 1.8% |
| Enterprise sales cycle | 6 months | 3 months | 2 months |
| Dec 2025 MRR | $155K | $260K | $420K |
| Dec 2026 MRR | $420K | $880K | $1,600K |
| Series B pre-money | $50M | $70M+ | $120M+ |
| Series B timing | Q3 2027 | Q1 2027 | Q3 2026 |

**Bear case action plan:** Reduce headcount plan by 4 hires, extend Series B to Q3 2027, focus GTM on community-driven self-serve only, defer enterprise AE hire.

---

## 9. BREAK-EVEN ANALYSIS

**Contribution margin break-even (per account):**
- Avg revenue: $750/month
- Variable COGS/account: ~$130/month
- Amortized CAC/month: $4,200 / 30 = $140/month
- **Net contribution from Month 1: $480/month positive — every account above $480 ACV is contribution-positive.**

**EBITDA break-even (all fixed costs):**
- Fixed costs at 22 FTE: $830,000/month
- Required MRR at 72% GM: $830,000 / 0.72 = **$1,153,000 MRR**
- Projected timing: **mid-2027** (post–Series B milestone, not Series A target)

---

## 10. KEY FINANCIAL RISKS

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Infra utilization miss (<50% for 6+ months) | 40% | GM compressed to <55%; $2M capital shortfall | Pause expansion capex; dynamic pre-warm optimization |
| Enterprise sales cycle >6 months | 35% | $300K revenue shortfall in 2025 | Use Team tier ($1K/month) as enterprise on-ramp |
| CAC increases as organic channels saturate | 50% | LTV:CAC falls to 2.0–2.5× | Invest in content SEO and framework integrations (durable channels) |
| Revenue concentration in top 3 accounts | Current reality | 28–52% MRR at risk from single churn | GA launch diversifies across 300+ accounts |
| Series A closes >3 months late | 15% | Must cut burn to $90K/month; delay hires | 12.6 months runway independent of Series A |
