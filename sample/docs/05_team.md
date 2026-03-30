# Team

## Founders

### Priya Anand — CEO & Co-Founder
- **Background:** 6 years at AWS; Principal Engineer on the Lambda team; co-designed Firecracker snapshot-restore mechanism (shipped 2022); reduced Lambda p50 cold start from 350ms to 85ms (2021–2023); Software Engineer at Dropbox (distributed storage, 2015–2019).
- **Education:** B.S. Computer Science, MIT (2015); no graduate degree.
- **Superpower:** Deep kernel-level systems expertise combined with enterprise sales credibility from her AWS tenure. Has existing relationships with Fortune 500 enterprise accounts (AWS enterprise customers she worked with directly).
- **References:** Publicly verifiable through AWS Lambda changelog, Firecracker GitHub contributions (handle: `priya-anand-aws`), MIT alumni directory.

### Marcus Webb — CTO & Co-Founder
- **Background:** Founding infrastructure engineer at Cohere (Series A through C, built compute orchestration from 0 to production at scale); Staff Engineer at Modal (2023–2024, serverless infrastructure product); previously SWE at Stripe (infrastructure reliability team, 2018–2020) and Google (Site Reliability Engineering, London, 2016–2018).
- **Education:** M.Eng. Computing, Imperial College London (2016).
- **Superpower:** Production ML infrastructure at scale, deep relationships in the AI developer ecosystem (Cohere, Modal alumni networks), and full-stack systems knowledge from Google SRE through bespoke AI platform engineering.
- **References:** Cohere engineering blog (Marcus quoted in 3 posts), Modal LinkedIn, Imperial alumni directory.

---

## Key Employees

### Seo-Yeon Park — Staff Engineer, Kernel & Virtualization
- **Joined:** November 2024 (employee #3, first hire)
- **Background:** 4 years at Red Hat (Linux kernel, KVM virtualization team); contributed to upstream Linux CRIU project; lead developer of the Sandstorm custom kernel patch. PhD in Operating Systems, ETH Zürich (2020).
- **Role:** Owns the core microVM runtime, snapshot engine, and host kernel. This is the most technically critical role in the company after the founders.

### Amara Diallo — Head of Product
- **Joined:** January 2025 (employee #4)
- **Background:** 4 years at Segment (Product Manager, developer tools); 2 years at Vercel (Senior PM, Edge Network and SDK). Deep developer-tool product instincts. No technical background but strong user research skills and a quantitative approach to feature prioritization.
- **Role:** Owns product strategy, roadmap, customer discovery, and pricing. Runs the monthly design partner review process.

### Ryo Tanaka — Software Engineer, SDK & Integrations
- **Joined:** February 2025 (employee #5)
- **Background:** 3 years at LangChain (early employee, built the LangChain tools and agents abstraction layer); 2 years at Replit (SDK developer experience). Knows every major agent framework from the inside. Author of `langchain-sandstorm` integration (600+ GitHub stars in first week).
- **Role:** Owns Python SDK, TypeScript SDK, and all framework integrations (LangChain, AutoGen, CrewAI, LangGraph).

### Yemi Okafor — Infrastructure Engineer, Control Plane
- **Joined:** March 2025 (employee #6)
- **Background:** 5 years at Cloudflare (infrastructure engineer, Workers KV and Durable Objects teams); strong background in distributed systems, global state management, and edge networking.
- **Role:** Owns the Go-based control plane: environment lifecycle management, resource scheduling, billing metering, and the fleet operations tooling.

---

## Advisors

### David Haber — GTM Advisor
- Co-founder of Kandji (MDM SaaS, raised $100M+). Deep expertise in developer tool sales motion, bottom-up to enterprise. Weekly office hours with Priya on GTM strategy.

### Christina Ou — Security & Compliance Advisor
- Former CISO at Plaid; led Plaid through SOC 2 Type II, PCI DSS, and FedRAMP authorization. Advising on Sandstorm's security architecture and compliance roadmap. Holds advisory equity.

### Dr. Anastasia Voronova — Technical Advisor (Kernel Systems)
- Researcher at VMware Research (formerly); author of 6 peer-reviewed papers on microVM performance. Provides formal technical review of Sandstorm's kernel patches and snapshot architecture.

### Nadia Karim — Developer Relations Advisor
- Head of Developer Relations at Stripe (2018–2022). Advising on community strategy, developer advocacy, and documentation standards.

---

## Open Roles (Q2 2025)

| Role | Team | Level | Priority |
|---|---|---|---|
| Senior Infrastructure Engineer (bare-metal ops) | Infrastructure | Senior | High |
| Developer Advocate | GTM | Mid-level | High |
| Account Executive (Enterprise) | Sales | Senior | Medium |
| Product Designer | Product | Mid-level | Medium |
| Security Engineer | Infrastructure | Senior | Medium |
| Data Engineer (telemetry/analytics) | Engineering | Mid-level | Low |

---

## Team Structure

**Current:** 6 FTE, fully co-located in San Francisco (SoMa office, 2,200 sq ft).

```
CEO (Priya Anand)
├── CTO (Marcus Webb)
│   ├── Staff Eng – Kernel (Seo-Yeon Park)
│   ├── Eng – SDK/Integrations (Ryo Tanaka)
│   └── Eng – Control Plane (Yemi Okafor)
└── Head of Product (Amara Diallo)
```

No sales team yet. Priya leads enterprise design partner relationships; Amara leads product discovery. All customer success is handled by engineers directly (a feature, not a bug — we learn from every production incident).

---

## Hiring Plan

**Q2 2025 (current quarter):** +2 hires
- Senior Infrastructure Engineer (bare-metal ops, on-site)
- Developer Advocate (remote-ok)

**Q3 2025:** +3 hires
- Account Executive (Enterprise, San Francisco)
- Product Designer
- Senior Infrastructure Engineer (networking, on-site)

**Q4 2025:** +3 hires
- Security Engineer
- Data Engineer
- Second Account Executive (New York or London)

**By December 2025:** Team of 14. Engineering:GTM ratio of 8:4 through 2025 (engineering-led growth phase).

---

## Capability Gaps

1. **No dedicated security engineer.** Our security posture is strong architecturally (microVM isolation, network namespaces, no shared FS) but has not been formally audited. Christina Ou (advisor) provides guidance, but a dedicated hire is needed before we pursue enterprise accounts above $10K/month. Target hire: Q3 2025.
2. **No dedicated sales motion.** We have no quota-carrying AEs. Enterprise pipeline is entirely founder-led. This is manageable today (8 design partners) but will bottleneck growth post–Series A. We plan to hire an AE in Q3 2025.
3. **Thin on DevOps/SRE.** Yemi owns control plane and fleet operations. A single point of failure for a 24/7 infrastructure product. We have on-call rotation with all engineers, but need a dedicated infra ops hire by Q3 2025.
4. **No marketing function.** Today, discovery is entirely community-driven (Twitter/X, Hacker News, LangChain Discord). Ryo (SDK engineer) doubles as community liaison. No dedicated marketing hire planned until post–Series A.

---

## 12-Month Org Priorities

1. **Close the security gap:** Hire Security Engineer by Q3 2025; complete SOC 2 Type I audit by Q4 2025.
2. **Build the sales muscle:** Hire first AE by Q3 2025; close 3 enterprise accounts ($5K+/month) by end of 2025.
3. **Scale the fleet:** Double bare-metal capacity from 48 to 96 servers by Q3 2025 to support projected load.
4. **Launch GA:** Exit private beta, open self-serve sign-up with credit card, by June 2025.
5. **Raise Series A:** Target $12M raise by Q4 2025; use the $1.8M pre-seed runway to get to $150K MRR as leverage.
