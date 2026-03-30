"""
Integration test for the full multi-agent analysis pipeline.

Runs a sample startup prompt through all 5 analyst agents + the aggregator
using real LLM calls. Asserts all outputs are non-empty strings and prints
the full output for inspection.

Requires: OPENAI_API_KEY env var set in backend/.env
"""
import os
import sys
import pytest
import pytest_asyncio

# Ensure backend root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

SAMPLE_PROMPT = """
We are building an AI-powered legal document review tool for small law firms.
Lawyers upload contracts and our system highlights risky clauses, suggests edits,
and benchmarks terms against industry standards. Pricing is $299/month per firm.
Target customers are solo practitioners and firms with 2-10 attorneys in the US.
We have 3 pilot customers and $50k ARR. The team has one ex-BigLaw attorney and
two ML engineers with NLP backgrounds.
"""


@pytest.mark.asyncio
async def test_full_pipeline_produces_all_outputs():
    """
    Run the full 5-agent analysis + aggregator on a sample prompt.
    Verifies all outputs are non-empty strings and prints results.
    """
    from main import build_retriever, app_graph, AGGREGATOR_PROMPT
    from langchain_openai import ChatOpenAI
    from langchain_core.output_parsers import StrOutputParser

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "OPENAI_API_KEY must be set in backend/.env"

    # Build retriever from sample prompt
    retriever, chunk_count = build_retriever(SAMPLE_PROMPT)
    assert chunk_count > 0, "Expected at least one chunk from sample prompt"
    print(f"\n[pipeline] chunk_count={chunk_count}")

    # Run 5 analyst agents
    analysis_result = await app_graph.ainvoke({"retriever": retriever})

    financial = analysis_result.get("financial", "")
    vc = analysis_result.get("vc", "")
    cto = analysis_result.get("cto", "")
    marketing = analysis_result.get("marketing", "")
    product = analysis_result.get("product", "")

    for name, output in [("financial", financial), ("vc", vc), ("cto", cto),
                          ("marketing", marketing), ("product", product)]:
        assert isinstance(output, str) and output.strip(), f"{name} agent returned empty output"

    # Build a mock competitor summary (no Exa API needed for this test)
    competitors_summary = (
        "- Kira Systems: AI contract review for enterprises (Series B)\n"
        "- Luminance: ML-based legal document analysis (Series B)\n"
        "- LawGeex: Contract review automation for in-house teams"
    )

    # Run aggregator
    llm = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0.3)
    aggregator_chain = AGGREGATOR_PROMPT | llm | StrOutputParser()
    overall = await aggregator_chain.ainvoke({
        "financial": financial,
        "vc": vc,
        "cto": cto,
        "marketing": marketing,
        "product": product,
        "competitors": competitors_summary,
    })

    assert isinstance(overall, str) and overall.strip(), "Aggregator returned empty output"

    # Print full output
    separator = "=" * 60
    print(f"\n{separator}")
    print("FINANCIAL ANALYSIS")
    print(separator)
    print(financial)

    print(f"\n{separator}")
    print("VC ANALYSIS")
    print(separator)
    print(vc)

    print(f"\n{separator}")
    print("CTO ANALYSIS")
    print(separator)
    print(cto)

    print(f"\n{separator}")
    print("MARKETING ANALYSIS")
    print(separator)
    print(marketing)

    print(f"\n{separator}")
    print("PRODUCT ANALYSIS")
    print(separator)
    print(product)

    print(f"\n{separator}")
    print("OVERALL EVALUATION (AGGREGATOR)")
    print(separator)
    print(overall)
    print(f"\n{separator}\n")
