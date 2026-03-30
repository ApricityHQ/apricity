# GTM Experiment Log

*Custom Section — Go-to-Market Experiment Tracker*

This section documents Sandstorm's go-to-market experiments from launch to present. It is maintained as a living document and shared with investors quarterly as a leading indicator of GTM velocity and learning agility. Each experiment is logged with hypothesis, methodology, results, and decision/next step.

---

## GTM Philosophy

Sandstorm's GTM is developer-led, community-first, and experiment-driven. We do not invest in channels until we have evidence that they produce qualified pipeline. Every channel is treated as a hypothesis to be tested before scaling. We track CAC, conversion rate, and time-to-value for every acquisition source.

**Current stage:** Private beta (8 design partners). GA launch: June 2025.

**Primary GTM question as of Q2 2025:** What is the lowest-CAC acquisition channel for self-serve accounts that convert at ≥22% within 30 days?

---

## Experiment Log

### Experiment 001: Hacker News "Show HN" Launch
- **Date:** November 4, 2024
- **Hypothesis:** A technical "Show HN" post featuring live benchmarks (boot time, snapshot resume latency) vs. competitors will generate 500+ signups and 10+ qualified design partner conversations.
- **Method:** Priya authored a 1,200-word technical post with measured benchmarks, posted at 8:00 AM PST on a Monday. No paid promotion. Thread moderated live for 6 hours.
- **Results:**
  - Reached HN front page #4 by 10:00 AM, trending for 14 hours.
  - 847 unique signups to waitlist within 48 hours.
  - 23 inbound emails requesting design partner access.
  - Of 23, 8 converted to active design partners (35% conversion rate on inbound).
  - Post reached 412 upvotes, 87 comments.
- **CAC:** ~$0 (founder time only; estimated at 8 hours of preparation + 6 hours of live engagement). Blended CAC including design partner onboarding: ~$1,100/account.
- **Decision:** ✅ **Validated.** HN "Show HN" is an efficient launch channel for technically sophisticated developer tools. Plan 2 more HN posts in 2025 (GA launch, snapshot branching feature launch).
- **Learning:** Comments were 70% about technical benchmarking methodology — our community skews deeply technical. Documentation and benchmark reproducibility are critical trust signals.

---

### Experiment 002: LangChain Discord "Office Hours" Presence
- **Date:** December 2024–January 2025 (ongoing)
- **Hypothesis:** Participating in LangChain's Discord server (#tools-and-integrations channel) will generate 5+ qualified leads per month from developers already working with agent frameworks.
- **Method:** Ryo Tanaka (SDK engineer) joined the LangChain Discord as a verified contributor. He answers questions related to tool execution and environment management 3–4 times per week. He does not pitch Sandstorm proactively but links to our docs when directly relevant.
- **Results (first 8 weeks):**
  - 18 unique DMs from developers asking about Sandstorm sandbox capabilities.
  - 11 of 18 requested waitlist access.
  - 4 of 11 converted to active pilots (2 of these are paying design partners).
  - 0 negative community sentiment ("spam" accusations) — community accepts the presence as value-adding.
- **CAC:** ~$0 direct spend. Ryo's time: ~3 hours/week. Annualized at Ryo's fully-loaded rate: ~$3,500/month cost → ~$875/converted account.
- **Decision:** ✅ **Validated.** Continue. Scale by adding AutoGen, CrewAI, and LlamaIndex Discord/Slack communities by Q2 2025 (Ryo to identify 1–2 community managers per community).
- **Learning:** Developer community presence requires genuine helpfulness, not promotion. The accounts that convert via Discord are among our highest NPS design partners — they arrive with pre-built trust.

---

### Experiment 003: "Agent Sandbox Benchmark" Open-Source Report
- **Date:** January 2025
- **Hypothesis:** Publishing an open-source benchmarking framework for comparing agent sandbox platforms (including e2b, Modal, Lambda, and Sandstorm) will generate 1,000+ GitHub stars and establish Sandstorm as the authoritative voice on agent sandbox performance.
- **Method:** Ryo and Marcus built `sandstorm-bench` — a reproducible benchmarking suite (Python, published to GitHub under MIT license) that measures cold start latency, snapshot operations, and code execution throughput for Sandstorm, e2b, Modal, and GitHub Actions. Results published to a hosted dashboard at bench.sandstorm.dev.
- **Results:**
  - GitHub stars: 612 in first 3 weeks (target was 1,000; revised to longer horizon).
  - 3 tech blog posts citing the benchmark (including one from the Modal engineering blog, which acknowledged our faster cold start).
  - 4 inbound design partner conversations directly attributable to the benchmark report.
  - e2b responded by publishing their own latency numbers (which validated our benchmark methodology by implicitly accepting our framing).
- **CAC from experiment:** ~$6,500 (3 weeks of Ryo's time, Marcus's review time). 4 design partner conversations → assuming 50% close rate = 2 accounts. CAC/account: ~$3,250.
- **Decision:** ⚠️ **Partially validated.** The benchmark is establishing category leadership (SEMrush shows "agent sandbox benchmark" as a top-3 keyword driving our site traffic). CAC is higher than Experiment 001–002, but the brand equity is durable. No further investment in the benchmark suite until we have headcount for content/DevRel.
- **Learning:** Benchmarks work as a trust signal but require ongoing maintenance. We need a Developer Advocate hire (planned Q2 2025) to maintain the benchmark suite and publish quarterly updates.

---

### Experiment 004: Cold Email Outreach to AI Engineering Leads
- **Date:** February 2025
- **Hypothesis:** Personalized cold email to 200 AI engineering leads (identified via LinkedIn, GitHub contribution data, and LangSmith usage data) will generate a 15% reply rate and 5% meeting conversion.
- **Method:** Priya authored a 3-sentence cold email referencing each recipient's specific GitHub repository or public project. Emails sent from `priya@sandstorm.dev` (founder email for credibility). 200 emails over 3 weeks.
- **Results:**
  - Open rate: 61% (strong; suggests subject line resonance)
  - Reply rate: 18% (36 replies; exceeded 15% target)
  - Meeting conversion: 8% (16 meetings booked; exceeded 5% target)
  - Of 16 meetings: 3 active design partner conversations, 1 signed pilot ($2,500/month)
  - 12 "not right now" responses with permission to follow up
- **CAC:** Priya's time (~40 hours total) + sales tools (Clay, Apollo: $180/month). Per-signed-account cost: ~$8,200 (high due to founder time cost).
- **Decision:** ✅ **Validated for enterprise pipeline.** Cold email generates enterprise pipeline efficiently, but at high founder cost. Next step: Hand off to AE once hired (Q3 2025). Do not scale cold email without AE to run it.
- **Learning:** Personalization is mandatory (we A/B tested a generic version at 4% reply rate vs. 18% personalized). GitHub contribution data is the highest-quality personalization signal — targeting people who have committed to LangChain or AutoGen repos with agent tools yields the best engagement.

---

### Experiment 005: Twitter/X Technical Thread Series
- **Date:** March 2025–ongoing
- **Hypothesis:** A biweekly thread from @PriyaAnandDev covering technical deep-dives (Firecracker internals, CRIU snapshots, agent infrastructure patterns) will grow her following to 5,000 and drive 100+ waitlist signups per thread.
- **Method:** Priya publishes a 10–15 tweet technical thread every other Monday at 9:00 AM PT. Topics so far: "How Lambda cold starts really work" (Thread 1), "The engineering behind sub-second snapshots" (Thread 2), "Why agents need a different sandbox than developers" (Thread 3).
- **Results (3 threads):**
  - Followers: 1,200 → 3,100 (+1,900 in 6 weeks)
  - Avg thread impressions: 82,000
  - Waitlist signups per thread: Thread 1: 147, Thread 2: 203, Thread 3: 181
  - Signups with highest intent (clicked "request access" within 24hrs): 31% of signups (about 170 total)
- **CAC:** 2–3 hours/thread (Priya). Signups: 531 across 3 threads. Of 531, estimated 117 will convert to paid (22% rate). Cost: ~8 hours of Priya's time → ~$0 direct spend. Opportunity cost: ~$6,400 (8 hours × fully-loaded CTO-equivalent rate).
- **Decision:** ✅ **Strong validation.** Twitter/X is our highest-ROI organic channel. Priya to continue biweekly cadence. No paid promotion; organic reach is sufficient. Marcus to start a parallel thread series on agent orchestration patterns (first post: April 2025).
- **Learning:** Threads that lead with a counterintuitive technical claim ("Lambda is actually bad for agents — here's why") outperform informational threads by 2.3× on engagement and 1.8× on signups.

---

### Experiment 006: Partnership with LangChain (Native Integration)
- **Date:** February–March 2025 (in progress)
- **Hypothesis:** Co-authoring an official `langchain-sandstorm` integration package (available as `pip install langchain-sandstorm`) will generate passive inbound from 20%+ of new LangChain users evaluating sandbox tools.
- **Method:** Ryo engaged LangChain's integration team directly (via personal relationship from his LangChain tenure). Proposed a co-maintained integration package. LangChain agreed to feature it in their documentation and newsletter. Integration went live February 28, 2025.
- **Results (first 4 weeks post-launch):**
  - `pip install langchain-sandstorm` downloads: 4,800 in first 4 weeks
  - GitHub stars (langchain-sandstorm repo): 623
  - Signups from LangChain docs referral: 89 unique accounts
  - Team tier trials started: 14
  - Paid conversions so far: 2 ($1,200/month and $3,500/month)
- **CAC:** ~6 weeks of Ryo's time (partial, alongside other duties) = ~$15,000 equivalent. 2 closed accounts so far = $7,500/account. But: the integration is durable and will produce compounding inbound. Expected CAC over 12 months as integration matures: ~$800/account.
- **Decision:** ✅ **Validated as long-term channel.** Pursuing identical integrations with AutoGen (in progress), CrewAI (outreach sent), and LlamaIndex (planned Q3 2025). This is our highest long-term leverage GTM channel.
- **Learning:** Framework integrations require a champion inside the framework team (Ryo's LangChain tenure was the key). Without an insider champion, integration proposals are deprioritized. Our framework partnerships are a network-effect moat dependent on team tenure.

---

## Channel Summary & CAC by Source

| Channel | Accounts Sourced | CAC (Blended) | Status |
|---|---|---|---|
| Hacker News "Show HN" | 8 design partners | ~$1,100 | Active (planned 2 more launches) |
| Discord community presence | 6 accounts | ~$875 | Active (scaling to 4 communities) |
| Benchmark open-source report | 4 accounts | ~$3,250 | Paused (need DevRel hire to scale) |
| Cold email outreach | 1 account + 12 in pipeline | ~$8,200 | Active (founder-led; hand off to AE Q3) |
| Twitter/X technical threads | 117 projected conversions | ~$55 (projected) | Active (highest ROI organic channel) |
| LangChain integration | 2 accounts + growing | ~$800 (12-month projected) | Active (scaling to 4 frameworks) |

**Overall blended CAC (current):** $2,100 (weighted average across all sources, early pilot accounts only)
**Target blended CAC at GA (June 2025):** $4,200 (will increase as paid channels and AE costs are added)
**Target blended CAC at Series A deployment:** $3,500 (scale improves efficiency on community channels)

---

## Next GTM Experiments (Planned Q2–Q3 2025)

| Experiment | Hypothesis | Method | Success Metric |
|---|---|---|---|
| GA Product Hunt launch | Top 3 product of the day | Coordinated community upvote campaign + HN cross-post | 1,000+ upvotes, 500+ signups |
| Paid search (Google) | "agent sandbox" keyword CPC < $8 with ≥3% conversion | $5K test budget, 30-day run | ≥15 qualified trials from paid |
| AI conference speaking (LangChain Conf) | 1 technical talk → 300+ signups | Submit CFP for LangChain Conference (April 2025) | 300+ signups, 10+ enterprise conversations |
| Content SEO ("agent sandbox" cluster) | Rank top 3 for "agent sandbox python" within 6 months | 8 long-form technical blog posts + backlink outreach | 500 organic signups/month by Q4 2025 |
| AWS Marketplace listing | AWS marketplace drives 50+ inbound accounts in first 90 days | Submit listing application; complete AWS ISV Accelerate | 50+ accounts, $75K ARR from marketplace |
