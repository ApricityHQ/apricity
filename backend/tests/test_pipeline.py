"""
Integration tests for the multi-agent startup analysis pipeline.

All tests use real LLM calls (no mocks). Requires OPENAI_API_KEY set in backend/.env.

Test coverage:
- Full pipeline: all 5 agents + aggregator produce non-empty output
- Short input path: RAG is skipped, full text passed directly as context
- Long input path: RAG chunking is active when input exceeds the threshold
- should_chunk threshold logic (no LLM needed)
- Agents function correctly when competitor data is provided in state
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# A realistic short startup pitch (well under the 4000-char RAG threshold).
SAMPLE_PROMPT = """
We are building an AI-powered legal document review tool for small law firms.
Lawyers upload contracts and our system highlights risky clauses, suggests edits,
and benchmarks terms against industry standards. Pricing is $299/month per firm.
Target customers are solo practitioners and firms with 2-10 attorneys in the US.
We have 3 pilot customers and $50k ARR. The team has one ex-BigLaw attorney and
two ML engineers with NLP backgrounds.
"""

# A mock competitor summary used in tests that don't need a live Exa API call.
MOCK_COMPETITORS = (
    "- Kira Systems: AI contract review for enterprises (Series B)\n"
    "- Luminance: ML-based legal document analysis (Series B)\n"
    "- LawGeex: Contract review automation for in-house teams"
)


@pytest.mark.asyncio
async def test_full_pipeline_produces_all_outputs():
    """
    Run all 5 analysis agents + aggregator on a sample prompt.

    Uses the short-input path (no RAG) with mock competitor data so the test
    does not require an Exa API key. Asserts every output is a non-empty string
    and prints the full results for manual inspection.
    """
    from main import app_graph, AGGREGATOR_PROMPT, analysis_llm
    from langchain_core.output_parsers import StrOutputParser

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "OPENAI_API_KEY must be set in backend/.env"

    analysis_result = await app_graph.ainvoke({
        "pitch": SAMPLE_PROMPT,
        "context": SAMPLE_PROMPT,
        "retriever": None,
        "competitors": MOCK_COMPETITORS,
    })

    for name in ("financial", "vc", "cto", "marketing", "product"):
        output = analysis_result.get(name, "")
        assert isinstance(output, str) and output.strip(), f"{name} agent returned empty output"

    aggregator_chain = AGGREGATOR_PROMPT | analysis_llm | StrOutputParser()
    overall = await aggregator_chain.ainvoke({
        "pitch": SAMPLE_PROMPT,
        "financial": analysis_result["financial"],
        "vc": analysis_result["vc"],
        "cto": analysis_result["cto"],
        "marketing": analysis_result["marketing"],
        "product": analysis_result["product"],
        "competitors": MOCK_COMPETITORS,
    })
    assert isinstance(overall, str) and overall.strip(), "Aggregator returned empty output"

    separator = "=" * 60
    for label, key in [
        ("FINANCIAL ANALYSIS", "financial"),
        ("VC ANALYSIS", "vc"),
        ("CTO ANALYSIS", "cto"),
        ("MARKETING ANALYSIS", "marketing"),
        ("PRODUCT ANALYSIS", "product"),
    ]:
        print(f"\n{separator}\n{label}\n{separator}")
        print(analysis_result[key])

    print(f"\n{separator}\nOVERALL EVALUATION (AGGREGATOR)\n{separator}")
    print(overall)
    print(f"\n{separator}\n")


@pytest.mark.asyncio
async def test_short_input_skips_rag():
    """
    Verify the pipeline works correctly on the short-input (no-RAG) path.

    should_chunk() must return False for the sample prompt, and agents must
    produce non-empty output when retriever=None and context is passed directly.
    """
    from main import app_graph
    from text_chunking import should_chunk

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "OPENAI_API_KEY must be set in backend/.env"

    assert not should_chunk(SAMPLE_PROMPT), (
        f"Expected should_chunk to return False for a {len(SAMPLE_PROMPT)}-char prompt"
    )

    analysis_result = await app_graph.ainvoke({
        "pitch": SAMPLE_PROMPT,
        "context": SAMPLE_PROMPT,
        "retriever": None,
        "competitors": MOCK_COMPETITORS,
    })

    for name in ("financial", "vc", "cto", "marketing", "product"):
        output = analysis_result.get(name, "")
        assert isinstance(output, str) and output.strip(), (
            f"{name} agent returned empty output on short-input (no-RAG) path"
        )


@pytest.mark.asyncio
async def test_long_input_uses_rag():
    """
    Verify the pipeline works correctly on the long-input (RAG active) path.

    Constructs a prompt that exceeds the RAG threshold by repeating the sample
    prompt, then builds a retriever and runs agents with it. Asserts all outputs
    are non-empty.
    """
    from main import app_graph, build_retriever
    from text_chunking import should_chunk

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "OPENAI_API_KEY must be set in backend/.env"

    # Repeat until we exceed the 4000-char threshold.
    long_text = (SAMPLE_PROMPT.strip() + "\n\n") * 10
    assert should_chunk(long_text), (
        f"Expected should_chunk to return True for a {len(long_text)}-char input"
    )

    retriever, chunk_count = build_retriever(long_text)
    assert chunk_count > 0, "Expected at least one chunk from long input"

    analysis_result = await app_graph.ainvoke({
        "pitch": SAMPLE_PROMPT,
        "context": "",
        "retriever": retriever,
        "competitors": MOCK_COMPETITORS,
    })

    for name in ("financial", "vc", "cto", "marketing", "product"):
        output = analysis_result.get(name, "")
        assert isinstance(output, str) and output.strip(), (
            f"{name} agent returned empty output on long-input (RAG active) path"
        )


def test_should_chunk_threshold():
    """
    Unit test for should_chunk() boundary conditions.

    No LLM calls required. Verifies the function correctly classifies inputs
    as short or long relative to the default and custom thresholds.
    """
    from text_chunking import should_chunk, RAG_THRESHOLD

    short = "a" * (RAG_THRESHOLD - 1)
    assert not should_chunk(short), "One char below threshold should not chunk"

    exact = "a" * RAG_THRESHOLD
    assert not should_chunk(exact), "Exactly at threshold should not chunk"

    long = "a" * (RAG_THRESHOLD + 1)
    assert should_chunk(long), "One char above threshold should chunk"

    # Custom threshold works correctly
    assert should_chunk("hello world", threshold=5), "Should chunk when text > custom threshold"
    assert not should_chunk("hi", threshold=5), "Should not chunk when text <= custom threshold"


@pytest.mark.asyncio
async def test_agents_with_competitor_context():
    """
    Verify that passing competitor data in state does not break the pipeline.

    Runs the full pipeline with a non-empty competitor summary and asserts all
    5 agents produce non-empty output. This confirms competitor data flows
    through to agents without errors.
    """
    from main import app_graph

    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key, "OPENAI_API_KEY must be set in backend/.env"

    analysis_result = await app_graph.ainvoke({
        "pitch": SAMPLE_PROMPT,
        "context": SAMPLE_PROMPT,
        "retriever": None,
        "competitors": MOCK_COMPETITORS,
    })

    for name in ("financial", "vc", "cto", "marketing", "product"):
        output = analysis_result.get(name, "")
        assert isinstance(output, str) and output.strip(), (
            f"{name} agent returned empty output when competitor context was provided"
        )
        # Outputs should be substantive — rich prompts should produce more than a trivial response
        assert len(output) > 100, (
            f"{name} agent output is suspiciously short ({len(output)} chars) — "
            "rich persona prompts should produce detailed analysis"
        )
