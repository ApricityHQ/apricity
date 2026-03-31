# Problem Statement

## The Problem

**What pain point or gap exists in the market?**

Farmers markets are one of the most beloved institutions in American cities — but they are structurally inaccessible to the majority of people who want to shop at them. They happen once a week, on Saturday or Sunday morning, between 8am and 1pm. If you have a soccer game, a sleeping toddler, a work shift, or simply a bad back that makes 45 minutes of walking and carrying heavy bags unappealing, you miss it. You go back to the grocery store and buy the same industrially-grown tomatoes shipped from Salinas you were trying to avoid.

The result: farmers market vendors cap out at whatever foot traffic their single weekly slot can produce. A small vegetable farm that draws 120 customers on a good Saturday could serve 400 households in that same ZIP code if ordering were not time-and-place-dependent. The product is there. The demand is there. The logistics layer connecting the two does not exist.

**What is broken today?**

The core failure modes fall on both sides of the transaction:

1. **Vendor-side: no digital storefront.** The average farmers market vendor is a small farm, a cottage baker, or an artisan producer with zero e-commerce infrastructure. They run a table with a card reader, handwritten price signs, and whatever they loaded into the truck that morning. They have no way to take advance orders, communicate what's available that week, or reach customers who couldn't make it in person.

2. **Customer-side: time-place lock-in.** Attending a farmers market requires showing up at a specific location during a narrow window on a weekend morning. For working parents, shift workers, people with mobility limitations, or anyone who travels regularly, this is simply incompatible with their schedule. Surveys consistently show that 60–70% of people who express a preference for locally-grown food do not regularly buy it — the barrier is access, not intent.

3. **Fragmented discovery.** Even customers who can make it to a market don't know what vendors will be there or what they'll have in stock. Inventory is weather-dependent, season-dependent, and entirely analog. There is no way to browse, plan a purchase, or know ahead of time that the mushroom farm you love will have hen-of-the-woods this week.

4. **No aggregated cart.** Farmers markets have 20–60 vendors. Buying a full week of groceries means visiting 6–8 stalls, carrying items between them, and doing arithmetic in your head across multiple transactions. There is no unified basket.

5. **Existing online grocery fails this use case entirely.** Instacart, Amazon Fresh, and DoorDash stock the same national brands from the same regional distribution centers. Their "local" shelves are stocked by regional distributors, not farmers. The actual farmers market experience — knowing the farm by name, buying what is in season this week, talking to the grower — is not replicable through these platforms.

**Why is this a significant problem?**

Local food is the fastest-growing segment of the US food market. The USDA's most recent agricultural census counted 8,700+ farmers markets operating in the US, generating approximately $12B in annual direct-to-consumer sales. Yet that figure has barely moved in five years — not because demand has plateaued, but because the distribution channel is stuck in an analog model that limits throughput. The addressable market is constrained by access, not appetite.

On the vendor side, the economics are punishing. A small produce farm earning $1,800/week at a single market is paying 8–12% of gross in market stall fees, spending 6–8 hours on setup/teardown, and absorbing unsold perishable inventory at end of day. Adding a second market requires another truck, another Saturday. Adding online orders through Porch requires nothing — the vendor lists their weekly inventory Thursday night from the farm, and Porch routes the fulfillment.

---

## Who Experiences This?

**Describe your target user in detail.**

Our primary customer is a **35–55 year old urban or near-suburban household** that already values local, seasonal food but cannot reliably attend their farmers market. They typically have household income above $85K, shop at Whole Foods or similar natural/specialty grocers as their baseline, and have purchased from a farmers market at least twice in the past year. They think of themselves as "someone who goes to the farmers market" even if, in practice, they make it only once a month. They feel mild guilt about this.

Secondary customers include:
- **Households with young children** where Saturday morning logistics make market attendance nearly impossible.
- **Remote workers who moved to suburbs** during and after 2020 — they have local farms nearby but fewer walkable markets and no habit of going.
- **Older adults and people with mobility limitations** who love farmers markets but find them physically difficult to navigate.
- **Restaurants and specialty food buyers** in cities without dedicated wholesale local farm channels.

On the vendor side, our primary partner is a **small-to-mid-size farm or artisan producer** doing $80K–$600K/year in direct-to-consumer revenue, operating at 2–6 markets per week. They have 1–3 employees, limited administrative bandwidth, and no technical resources to build or maintain their own e-commerce.

**What is their current workflow?**

A typical customer who wants farmers market produce today:
1. Checks whether Saturday is free — it usually isn't.
2. Considers driving to the market anyway — decides against it given the time commitment.
3. Opens Instacart or goes to Whole Foods — buys conventional produce. Feels mild disappointment.
4. Resolves to "make it next week."

A typical vendor today:
1. Harvests Thursday–Friday. Estimates what will sell based on last week's weather and foot traffic.
2. Loads the truck Saturday at 5am. Sets up by 7am.
3. Sells until 1pm. Packs up unsold inventory — often 15–25% of what they brought.
4. Returns to the farm. Adds up the day's take by hand or on a basic POS.
5. Has no visibility into which customers bought from them, what they want next week, or how to reach them again.

---

## Current Alternatives

**How do people solve this problem today?**

- **CSA (Community Supported Agriculture) boxes:** Customers subscribe to a weekly share from a single farm. Popular but inflexible — you receive whatever the farm harvests, in whatever quantities they pack. No vendor choice, no product selection, no multi-farm variety. Churn is high when households receive 3 weeks of kohlrabi in a row.
- **Good Eggs (San Francisco only):** The closest model to Porch. Delivers local/organic groceries including farm-direct produce. However, Good Eggs is a retailer — they warehouse inventory and act as the merchant of record. Vendors sell wholesale to Good Eggs. Farmers receive 40–50 cents on the dollar. Good Eggs exited most markets (Chicago, New York, LA) due to unit economics.
- **Imperfect Foods / Misfits Market:** National-scale "ugly produce" subscription services. Products are sourced from regional distributors, not local farms. Not a farmers market alternative in any meaningful sense.
- **Local Facebook groups / Instagram DMs:** Many vendors have developed informal online order systems through social media — a post on Friday, DMs to reserve, Venmo at pickup. Technically functional, operationally painful, not scalable.
- **UNFI / KeHE local lines:** Regional distributors that carry some local products for grocery retailers. High minimums, slow cycles, and a 40–60% margin take that is unworkable for small farms.

**Why are existing solutions inadequate?**

CSAs require commitment and sacrifice choice — the two things customers are least willing to give up. Good Eggs demonstrated the demand but collapsed under warehouse-model unit economics; their mistake was taking inventory risk. Porch does not warehouse inventory — vendors bring what they've committed to, fulfillment happens on delivery day, and Porch never touches unsold stock. The local Instagram DM ecosystem proves the demand is real but is limited to the most motivated customers of the most digitally-savvy vendors. There is no aggregated, multi-vendor, discovery-first experience for local food online.

---

## Why Now?

**What has changed that makes this the right time?**

1. **Post-pandemic local food preference is permanent.** Consumer preference surveys in 2023–2025 consistently show that 58–65% of grocery shoppers say "buying from local farms" is important or very important to them — up from 41% in 2019. This is not a trend; it is a baseline shift in consumer values following supply chain disruptions and the visibility they created.

2. **Gig delivery infrastructure is mature and cheap.** The cost of same-day last-mile delivery has dropped 40% since 2021 as DoorDash Drive, Uber Direct, and regional courier networks reached density in most metro areas. A startup building a local food delivery product in 2019 had to internalize driver costs that are now available as API calls.

3. **Vendor payment and inventory tooling is finally accessible.** Square, Toast, and Shopify have reached >70% penetration among small food vendors. Most farmers market vendors already have a smartphone and some form of digital payment. The technical ask of "list your inventory every Thursday" is now plausible where it wasn't five years ago.

4. **Wholesale local food channel is drying up.** Several regional produce distributors (including two in our pilot market) have closed or reduced local farm lines due to post-pandemic cost pressures. Farms that previously relied on wholesale are actively looking for direct-to-consumer channels.
