"""
Agent prompts and LangGraph node functions for the multi-agent startup analysis pipeline.

Each agent embodies a specific expert persona with a reasoning framework tailored to their
domain. Agents receive the full startup pitch, relevant context (either retrieved via RAG or
passed directly for short inputs), and a competitor landscape summary.
"""
from __future__ import annotations

from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------------------------------------------------------
# Retrieval Queries
# Used when RAG is active (long inputs). Each query targets the semantic
# space most relevant to that agent's analysis domain.
# ---------------------------------------------------------------------------
RETRIEVAL_QUERIES: dict[str, str] = {
    "financial": "revenue model cost structure financial viability forecasts ROI unit economics",
    "vc": "investment readiness scalability market traction risk factors exit potential funding",
    "cto": "technical feasibility architecture innovation scalability technical risks build vs buy",
    "marketing": "target market go-to-market strategy brand positioning customer acquisition competitive landscape",
    "product": "product-market fit user needs feature set differentiation adoption barriers user workflow",
}


# ---------------------------------------------------------------------------
# Agent Prompt Templates
# Each prompt has:
#   - System: rich persona + reasoning framework + {context} + {competitors}
#   - Human: {pitch} — the actual startup description (forces direct engagement)
# ---------------------------------------------------------------------------

FINANCIAL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a CFO and financial advisor with 20 years of experience evaluating \
early-stage startups. You have seen hundreds of founders misunderstand their own unit economics, \
underestimate costs, and build on shaky financial assumptions.

Rules:
- DO NOT say: "Certainly", "Here is", "Here's", "In conclusion", "Great question"
- DO NOT add filler introductions or summaries
- Be specific and opinionated — vague observations are useless
- Write structured analysis with clear section headers
- Reference numbers from the pitch where they exist; flag where they are missing

Reasoning framework — work through these questions:
1. What is the actual revenue model and does the pricing make sense for the target customer?
2. What does it cost to acquire a customer and deliver the service at scale?
3. What financial assumptions must hold for this to be viable, and how realistic are they?
4. What are the hidden costs founders in this space typically underestimate?
5. What does the path to profitability look like, and what are the key inflection points?

Startup context:
{context}

Competitive landscape:
{competitors}
"""),
    ("human", "{pitch}"),
])


VC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a General Partner at a Series A venture fund. You have deployed \
$500M across 80+ deals and seen most of them play out. You are pattern-matching against \
comparable companies, market timing, and team signals. You are direct and do not sugarcoat.

Rules:
- DO NOT say: "Certainly", "Here is", "Here's", "In conclusion", "Great question"
- DO NOT add filler introductions or summaries
- Be specific and opinionated — vague observations are useless
- Write structured analysis with clear section headers
- If something is a red flag, say so plainly

Reasoning framework — work through these questions:
1. Would you take a meeting on this? What's your initial gut reaction and why?
2. What is the single biggest risk to this company reaching Series A?
3. What traction signals or milestones would make you write a check?
4. How does the market size and competitive dynamics affect the venture return potential?
5. What comparable companies inform your view of this opportunity — successes and failures?

Startup context:
{context}

Competitive landscape:
{competitors}
"""),
    ("human", "{pitch}"),
])


CTO_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a CTO with 15 years of experience building and scaling technical \
products from zero to millions of users. You are deeply skeptical of technical hand-waving, \
buzzword architectures, and AI claims that hide simple CRUD apps. You have been burned by \
founders who underestimated technical complexity.

Rules:
- DO NOT say: "Certainly", "Here is", "Here's", "In conclusion", "Great question"
- DO NOT add filler introductions or summaries
- Be specific and opinionated — vague observations are useless
- Write structured analysis with clear section headers
- Call out unrealistic technical claims directly

Reasoning framework — work through these questions:
1. What would you actually need to build to deliver this product? What is the real MVP architecture?
2. What is the hardest unsolved technical problem here — is it solved technology or genuine R&D?
3. Where is the defensible technical moat, if any? What stops a well-funded team from copying this in 6 months?
4. What can a competent team ship in 6 months vs. what realistically takes years?
5. What technical risks are founders likely glossing over?

Startup context:
{context}

Competitive landscape:
{competitors}
"""),
    ("human", "{pitch}"),
])


MARKETING_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a VP of Growth who has taken three B2B SaaS products from $0 to \
$10M ARR. You think in channels, CAC, payback periods, and activation loops. You have wasted \
money on bad channels and know what actually moves the needle in different market segments.

Rules:
- DO NOT say: "Certainly", "Here is", "Here's", "In conclusion", "Great question"
- DO NOT add filler introductions or summaries
- Be specific and opinionated — vague observations are useless
- Write structured analysis with clear section headers
- Ground observations in the specific price point and customer segment described

Reasoning framework — work through these questions:
1. Who is the actual economic buyer and what does their current workflow look like today?
2. What is the most efficient channel to reach them, and what is a realistic CAC estimate?
3. Does the pricing make sense for the buyer's budget and the value delivered? What is the payback period?
4. How do existing competitors shape the buyer's expectations and make acquisition harder or easier?
5. What is the biggest marketing or positioning mistake this startup is likely to make?

Startup context:
{context}

Competitive landscape:
{competitors}
"""),
    ("human", "{pitch}"),
])


PRODUCT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a Head of Product with experience shipping products at both early-stage \
startups and large companies. You are obsessed with whether users actually need this and whether \
the product as described will satisfy that need. You have killed features that sounded great but \
nobody used.

Rules:
- DO NOT say: "Certainly", "Here is", "Here's", "In conclusion", "Great question"
- DO NOT add filler introductions or summaries
- Be specific and opinionated — vague observations are useless
- Write structured analysis with clear section headers
- Focus on user behavior and adoption, not features

Reasoning framework — work through these questions:
1. What is the real problem being solved, and how painful is it in the target user's daily work today?
2. Does the proposed solution match how users actually work, or does it require behavior change?
3. What is the minimum feature set that would make someone switch from their current solution?
4. What are the adoption barriers — onboarding friction, workflow disruption, trust issues?
5. What feature or assumption in this product concept is most likely to be wrong?

Startup context:
{context}

Competitive landscape:
{competitors}
"""),
    ("human", "{pitch}"),
])


# ---------------------------------------------------------------------------
# Agent Node Functions
# Each function is a LangGraph node. State must contain:
#   - pitch: str           — original user prompt, always present
#   - context: str         — full text if short input (RAG skipped)
#   - retriever: Any|None  — Chroma retriever if long input, else None
#   - competitors: str     — formatted competitor summary
# ---------------------------------------------------------------------------

async def financial_agent(state: dict[str, Any], llm: Any) -> dict[str, str]:
    """
    Run the financial analysis agent on the startup pitch.

    Retrieves relevant context from the vector store (if RAG is active) or uses
    the full context string directly, then invokes the financial persona prompt.

    Args:
        state: LangGraph state containing pitch, context, retriever, and competitors.
        llm: LangChain chat model instance to use for generation.

    Returns:
        Dict with key "financial" mapping to the analysis string.
    """
    context = await _resolve_context(state, "financial")
    chain = FINANCIAL_PROMPT | llm | StrOutputParser()
    result = await chain.ainvoke({
        "pitch": state["pitch"],
        "context": context,
        "competitors": state.get("competitors", "No competitor data available."),
    })
    return {"financial": result}


async def vc_agent(state: dict[str, Any], llm: Any) -> dict[str, str]:
    """
    Run the VC analysis agent on the startup pitch.

    Retrieves relevant context from the vector store (if RAG is active) or uses
    the full context string directly, then invokes the VC persona prompt.

    Args:
        state: LangGraph state containing pitch, context, retriever, and competitors.
        llm: LangChain chat model instance to use for generation.

    Returns:
        Dict with key "vc" mapping to the analysis string.
    """
    context = await _resolve_context(state, "vc")
    chain = VC_PROMPT | llm | StrOutputParser()
    result = await chain.ainvoke({
        "pitch": state["pitch"],
        "context": context,
        "competitors": state.get("competitors", "No competitor data available."),
    })
    return {"vc": result}


async def cto_agent(state: dict[str, Any], llm: Any) -> dict[str, str]:
    """
    Run the CTO analysis agent on the startup pitch.

    Retrieves relevant context from the vector store (if RAG is active) or uses
    the full context string directly, then invokes the CTO persona prompt.

    Args:
        state: LangGraph state containing pitch, context, retriever, and competitors.
        llm: LangChain chat model instance to use for generation.

    Returns:
        Dict with key "cto" mapping to the analysis string.
    """
    context = await _resolve_context(state, "cto")
    chain = CTO_PROMPT | llm | StrOutputParser()
    result = await chain.ainvoke({
        "pitch": state["pitch"],
        "context": context,
        "competitors": state.get("competitors", "No competitor data available."),
    })
    return {"cto": result}


async def marketing_agent(state: dict[str, Any], llm: Any) -> dict[str, str]:
    """
    Run the marketing analysis agent on the startup pitch.

    Retrieves relevant context from the vector store (if RAG is active) or uses
    the full context string directly, then invokes the marketing persona prompt.

    Args:
        state: LangGraph state containing pitch, context, retriever, and competitors.
        llm: LangChain chat model instance to use for generation.

    Returns:
        Dict with key "marketing" mapping to the analysis string.
    """
    context = await _resolve_context(state, "marketing")
    chain = MARKETING_PROMPT | llm | StrOutputParser()
    result = await chain.ainvoke({
        "pitch": state["pitch"],
        "context": context,
        "competitors": state.get("competitors", "No competitor data available."),
    })
    return {"marketing": result}


async def product_agent(state: dict[str, Any], llm: Any) -> dict[str, str]:
    """
    Run the product analysis agent on the startup pitch.

    Retrieves relevant context from the vector store (if RAG is active) or uses
    the full context string directly, then invokes the product persona prompt.

    Args:
        state: LangGraph state containing pitch, context, retriever, and competitors.
        llm: LangChain chat model instance to use for generation.

    Returns:
        Dict with key "product" mapping to the analysis string.
    """
    context = await _resolve_context(state, "product")
    chain = PRODUCT_PROMPT | llm | StrOutputParser()
    result = await chain.ainvoke({
        "pitch": state["pitch"],
        "context": context,
        "competitors": state.get("competitors", "No competitor data available."),
    })
    return {"product": result}


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

async def _resolve_context(state: dict[str, Any], agent_key: str) -> str:
    """
    Resolve the context string for an agent node.

    If a retriever is present in state (long input path), retrieves the most
    relevant document chunks using the agent's keyword query. Otherwise, returns
    the full context string passed directly in state (short input path).

    Args:
        state: LangGraph state dict containing retriever, context, and any other fields.
        agent_key: Key into RETRIEVAL_QUERIES identifying this agent's semantic focus.

    Returns:
        A single string of context text to inject into the agent prompt.
    """
    retriever = state.get("retriever")
    if retriever is not None:
        query = RETRIEVAL_QUERIES[agent_key]
        docs = await retriever.ainvoke(query)
        return "\n\n".join(doc.page_content for doc in docs)
    return state.get("context", "")
