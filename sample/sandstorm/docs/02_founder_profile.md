# Founder Profile

## Background

**Share your journey — what led you here?**

I'm Priya Anand, CEO and co-founder of Sandstorm. I spent six years at AWS, the last three as a Principal Engineer on the AWS Lambda team, where I worked directly on Firecracker — the open-source microVM technology that powers AWS Lambda and AWS Fargate. I wrote the original implementation of Lambda's snapshot-and-restore mechanism (the feature that dramatically reduced Lambda cold starts in 2022), and I led the team that reduced Lambda's p50 cold start from 350ms to 85ms between 2021 and 2023. Before that, I was a software engineer at Dropbox building distributed storage infrastructure.

My co-founder is Marcus Webb, CTO. Marcus was the founding infrastructure engineer at Cohere, where he built the compute orchestration layer that ran Cohere's fine-tuning and inference pipelines from Series A through Series C (0 to ~$200M ARR). After Cohere, he spent 18 months at Modal as a Staff Engineer, working on the serverless infrastructure product. Marcus left Modal when we decided to start Sandstorm together in mid-2024.

**What is your personal connection to the problem?**

While on the Lambda team, I watched AWS customers — particularly early AI startups — try to abuse Lambda as an agent sandbox. They would jam Python dependencies into Lambda layers, fight against the 15-minute execution limit, and hack around the read-only filesystem with `/tmp` mounting tricks. I understood viscerally why they were doing this: Lambda was the closest thing to an "instant compute environment" that existed, but it was fundamentally wrong for the job. After I left AWS, I joined a seed-stage AI startup as a founding engineer for four months to understand the buyer perspective. In that role I personally built, maintained, and eventually threw away a Docker-based agent sandbox — spending three weeks on infrastructure that should have been a two-line API call. That experience crystallized the product vision.

**What were you doing before this?**

Immediately before Sandstorm, I took a deliberate three-month sabbatical to travel Southeast Asia and write a detailed technical memo on the architecture of agent sandboxing. That memo became our internal design document and was the basis of the angel pitch deck. Marcus left Modal in June 2024 and we co-authored the architecture together between July and September 2024. We incorporated Sandstorm in Delaware in August 2024, moved to San Francisco, and closed our pre-seed round in October 2024.

---

## Why This Problem?

**What makes you uniquely positioned to solve this?**

My unfair advantage is combinatorial: I have deep, production-hardened experience with the exact technology stack (Firecracker, KVM, Linux kernel namespaces, cgroups, seccomp) required to build fast microVM sandboxes; I have spent time on both sides of the problem (infrastructure builder at AWS, infrastructure consumer at an AI startup); and I have long-standing relationships with the AWS Firecracker team, which gives us early access to upstream patches and performance data that competitors cannot see.

Marcus's complementary advantage is on the orchestration and go-to-market side: he has deep relationships across the AI developer community from his time at Cohere and Modal, and he understands the production requirements of LLM inference and agent orchestration workloads at scale.

Together, our backgrounds cover: microVM internals, Linux kernel hacking, distributed systems, LLM inference infrastructure, developer tool go-to-market, and enterprise AI platform sales.

**Why are you the right person for this?**

There are perhaps 20 engineers in the world who have shipped production microVM snapshotting at scale. I am one of them, and I am building Sandstorm. The technical depth required to deliver sub-second snapshot-and-resume across heterogeneous agent workloads is the single highest barrier to entry in this market. That barrier is our moat.

Additionally, the agent sandbox market is at an inflection point where the founders who have both the technical credibility and the enterprise network to land early design partners will define the category. My AWS pedigree opens doors at Fortune 500 accounts (AWS enterprise relationships); Marcus's Cohere and Modal relationships open doors at AI-native Series A–C companies. We have the right network for the right moment.

**What is your unfair advantage?**

1. **Proprietary kernel patch:** We have developed a custom Linux kernel patch (building on Linux's CRIU checkpoint/restore infrastructure) that reduces snapshot delta size by 65% compared to a naive Firecracker snapshot. This is non-trivial IP that took four months to develop and is not published. Competitors would need to replicate this independently.
2. **AWS Firecracker insider access:** I co-maintain two open-source modules in the Firecracker project. This gives us a direct communication channel with the AWS team that builds the most widely-deployed microVM runtime in the world.
3. **Design partner pipeline:** Before writing a line of product code, Marcus and I ran 60 customer discovery calls. We have 8 design partners (including one Series B AI-native company, one Fortune 500 financial services AI lab, and four seed-stage AI startups) signed on paid pilots at $2,500–$8,000/month, generating $31K MRR from pilots alone.
4. **Pre-seed capital from operators:** Our $2.1M pre-seed was led by Gradient Ventures (Google's AI-focused seed fund) with participation from Elad Gil, Zack Kanter, and four founders of developer tool companies (including a co-founder of Vercel and a co-founder of Fly.io). These are not just checks — they are a validation network and a door-opener to their portfolio companies.
