# Risks & Unknowns

## Open Questions

**Things you're still figuring out:**

1. **Enterprise security compliance velocity.** We know enterprise accounts with InfoSec teams need SOC 2 before signing, but we don't yet know how long our SOC 2 audit will take or if additional certifications (ISO 27001, FedRAMP Moderate) will be blocking requirements for financial services accounts. We're 3 weeks into the audit process.
2. **Optimal pricing for the enterprise tier.** Our design partner pricing ($2,500–$8,000/month) is not yet informed by a full competitive analysis. We do not know the price elasticity curve well enough to set enterprise minimums confidently. We are running pricing experiments in Q2 2025.
3. **Windows/macOS sandbox architecture.** The Linux microVM approach is clean. Supporting Windows or macOS agents requires either a macOS host node (Apple silicon, legally murky in colocated data centers) or a Windows-on-Firecracker approach that is technically immature. We have not yet committed to an architecture.
4. **Hyperscaler partnership vs. independence.** We're exploring an AWS Marketplace listing (which could drive significant inbound) but are concerned about strategic lock-in. We have not decided whether to pursue AWS as a distribution channel or to stay fully independent through Series A.
5. **Community vs. enterprise-first GTM.** We are currently 100% community/PLG (no AEs). We need to decide at what ARR threshold to invest in enterprise sales motion and how much founder time it takes. We currently have no empirical data on our enterprise sales cycle length.
6. **Long-running environments economics.** Our pricing model today is optimized for short-burst agent runs (seconds to minutes). We do not yet know the unit economics of 24/7 persistent environments. The "always-on agent" use case may require a different infrastructure architecture (hot pools vs. on-demand). We are running infrastructure experiments in Q2 2025.

**What are known unknowns?**

- **Churn by segment:** We have only 8 paying customers and zero churn data. The 2.5% monthly churn assumption in our model is derived from comparable developer tools, not our own data.
- **Competitor roadmaps:** We know e2b's current capabilities but not their 12-month roadmap. We suspect they are working on snapshotting based on a GitHub issue (open since November 2024). We do not know how close they are.
- **Regulatory specifics:** The EU AI Act mandates human oversight for high-risk AI systems, but the specific compliance requirements for agent sandboxes are not yet clarified by regulators. We may need legal opinion before selling to EU financial services.
- **Cost of bare-metal scaling:** We have a 3-year colocation agreement with Equinix but the per-server capex will change as we scale. We do not yet know our unit economics beyond 200 servers.

**What experiments do you need to run?**

| Experiment | Hypothesis | How to Test | Timeline |
|---|---|---|---|
| Freemium tier | Free accounts that hit a usage cap will convert to paid at 22%+ | Track cohort of 100 free accounts through May 2025 GA launch | Q2 2025 |
| Enterprise pricing | $5K/month minimum is achievable for accounts >10 running environments | Offer enterprise plan to 5 design partners, measure objection rate | Q2 2025 |
| Windows sandbox demand | >30% of RFPs from design partners mention Windows environment need | Survey 20 current/prospective customers | Q2 2025 |
| Developer advocacy | 1 keynote at an AI conference generates 500+ signups | Submit to LangChain Conference, PyCon, GTC; track CAC by channel | Q3 2025 |
| Long-running env economics | Pause-on-idle reduces infrastructure cost of persistent environments by 60%+ | Run 30-day pilot with 3 design partners on "always-on" plan | Q2–Q3 2025 |

---

## Assumptions

**What must be true for this to work?**

1. AI agent adoption continues to grow at current rate or faster through 2026. If agents are a fad or adoption plateaus, the market is smaller than modeled.
2. Teams building agents prefer a managed sandbox over building their own. If the "build vs. buy" calculus shifts (e.g., open-source self-hosted solution becomes trivial to set up), demand for Sandstorm declines.
3. Our infrastructure performance advantage (sub-800ms boot, sub-800ms snapshot resume) is a sustainable differentiator for at least 18 months before competitors catch up.
4. Usage-based pricing drives expansion revenue in a way that makes NRR > 110%. If customers hit their use cases and don't expand, the business requires constant new-logo acquisition.
5. We can hire the engineering talent needed (bare-metal infra, kernel engineers) in the SF Bay Area labor market. These roles are rare and competitive.
6. Enterprise buyers will accept a startup as their infrastructure vendor if we achieve SOC 2 Type I/II certification. Security objections go away with certification.

**What is the riskiest assumption?**

The riskiest assumption is #3 (performance advantage is sustainable). If e2b or an open-source project ships snapshotting for Firecracker-based sandboxes, our primary technical differentiator is at risk. We are mitigating this through additional moats (bare-metal fleet, SDK ecosystem, data flywheel) but the technical lead is a time-limited advantage.

**What are you taking for granted?**

- Open-source projects (Firecracker, CRIU, containerd) remain actively maintained and do not introduce breaking changes to our patch surface.
- Equinix colocation pricing remains stable over our 3-year lease term.
- The Sandstorm team remains intact (no co-founder departure, no critical hire attrition).
- AWS does not acquire e2b or a competitor in the next 12 months (which would give AWS a purpose-built agent sandbox overnight).

---

## Top 5 Risks

### Risk 1: Hyperscaler Entry
**Description:** AWS, GCP, or Azure ships an agent-native sandbox product that leverages their existing compute infrastructure. AWS already has Firecracker internally; shipping an external agent sandbox product is an architectural choice, not a technical hurdle.
**Probability:** Medium (35% within 24 months). **Impact:** High (could halve our SAM).
**Mitigation:** Accelerate ecosystem integrations and enterprise sales to create switching costs before hyperscalers move. Build on AWS Marketplace (distribution leverage) while maintaining AWS-agnostic architecture. Invest in community and open-source presence to establish brand before AWS enters.

### Risk 2: e2b Ships Snapshotting
**Description:** e2b is the most direct competitor. If they close the snapshotting capability gap, our primary USP narrows to bare-metal performance (which is harder to communicate) and ecosystem depth (which takes time to build).
**Probability:** High (60% within 12 months). **Impact:** Medium (increases competitive intensity; requires us to accelerate ecosystem moat).
**Mitigation:** We are 3–4 months ahead on snapshotting technical capability. Accelerate GA launch, build SDK integrations, and create lock-in before e2b ships. Monitor their GitHub repository (they have an open "snapshot" issue with high activity). If they ship snapshots, differentiate on: full OS environment (not just code execution), bare-metal performance, and enterprise compliance.

### Risk 3: Infrastructure Cost Overrun
**Description:** Our gross margin model depends on high server utilization (target: 70%+ average utilization). If demand ramps slower than forecast, utilization stays low (currently ~45%) and gross margin compresses to <40%, making the business economically fragile.
**Probability:** Medium (40%). **Impact:** High (could require additional capital raise earlier than planned).
**Mitigation:** Pre-warm pool manages utilization actively. Dynamic pricing (surge pricing for peak hours) adds another lever. If utilization stays below 50% for 60 days post-GA, we review bare-metal expansion capex.

### Risk 4: Key Person Risk (Seo-Yeon Park)
**Description:** Seo-Yeon is the only engineer with kernel-level expertise capable of maintaining and advancing our custom snapshot compression patch. Her departure (voluntary or involuntary) would halt core technical development.
**Probability:** Low (15% annual). **Impact:** Very High.
**Mitigation:** Detailed technical documentation of all kernel patches (currently at 70% coverage; target 95% by Q3 2025). Hire second kernel/infra engineer by Q3 2025. Equity vesting cliff passed in November 2024; 4-year vest on 1-year cliff (she is 5 months vested). Competitive compensation: $195K base + 1.2% equity (unvested balance ~$480K at $40M post-money valuation).

### Risk 5: AI Agent Adoption Slowdown
**Description:** If AI agents prove less capable than expected (model quality plateau, hallucination issues in production), enterprise buyers slow or reverse their agent deployment plans, reducing demand for agent infrastructure.
**Probability:** Low-Medium (25%). **Impact:** High (forces pivot or significant downsizing).
**Mitigation:** Sandstorm's product works for any sandboxed code execution, not only AI agents (CI/CD, security research, code education). If the agent market softens, pivot GTM toward generic cloud sandbox use cases. This is a partial hedge, not a complete one.

---

## Mitigations Summary

| Risk | Primary Mitigation | Secondary Mitigation |
|---|---|---|
| Hyperscaler entry | Enterprise lock-in via SOC 2 + ecosystem integrations | Build AWS Marketplace presence for distribution |
| e2b snapshotting | Accelerate GA launch; build SDK lock-in | Full OS advantage vs. gVisor; bare-metal performance |
| Infra cost overrun | Dynamic pre-warm pool management | Pause expansion capex if utilization < 50% for 60 days |
| Key person (Seo-Yeon) | Document kernel patches; hire second kernel engineer | Competitive equity + compensation retention |
| Agent adoption slowdown | Generic sandbox GTM as fallback | Diversify beyond LLM agents to CI/CD and dev tooling |

---

## Leading Indicators to Watch

| Indicator | Target | Frequency | Owner |
|---|---|---|---|
| Weekly API calls | >50% MoM growth in private beta | Weekly | Amara (Product) |
| Trial-to-paid conversion | ≥22% within 30 days | Monthly | Amara |
| Net Revenue Retention | ≥110% | Monthly | Priya |
| Snapshot API usage rate | >40% of environments use at least 1 snapshot | Monthly | Marcus |
| GitHub stars (sandstorm-sdk) | >1,000 by GA launch | Weekly | Ryo |
| Server utilization | ≥65% avg by Q4 2025 | Weekly | Yemi |
| Enterprise pipeline value | $150K+ qualified pipeline by Q3 2025 | Monthly | Priya |
| Churn rate | <3%/month | Monthly | Amara |

---

## Dependencies That Could Break the Plan

1. **Equinix colocation uptime:** Our SLA with Equinix guarantees 99.9% power uptime. A colocation failure could result in an extended outage affecting all customers. Mitigation: We run active-active across SV5 and DA2; an SV5 failure shifts load to DA2 within 60 seconds.
2. **Firecracker upstream compatibility:** A breaking change in Firecracker's API surface could invalidate our control plane integration. Mitigation: We pin to Firecracker v1.6.0 and test against upstream main weekly. Priya's relationship with the upstream team gives us advance warning of breaking changes.
3. **AWS S3 for snapshot storage:** We use S3 as our cold snapshot store. A regional S3 outage would prevent snapshot restore. Mitigation: Hot-tier snapshot cache on NVMe attached to host; 95% of snapshot resumes are served from hot cache without touching S3.
4. **Series A close timing:** If the round closes later than June 2025 (e.g., delayed to September 2025), we operate on pre-seed cash ($1.87M / $148K burn = 12.6 months). At October 2025, we would need to cut burn dramatically. This is an existential dependency on the Series A closing on schedule.
5. **LangChain/AutoGen API stability:** Our SDK integrations depend on stable public APIs from LangChain and Microsoft AutoGen. Both projects have a history of breaking changes. Ryo maintains a compatibility matrix and we run integration tests on every upstream release.
