"""
Unit tests for text_chunking.py.

No LLM calls required. Verifies chunk_text() behaviour for empty input,
normal input, and long input that produces multiple chunks.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from text_chunking import chunk_text


def test_chunk_text_returns_documents():
    """chunk_text returns a non-empty list with page_content for normal input."""
    text = "We are building an AI-powered legal document review tool for small law firms."
    result = chunk_text(text)

    assert isinstance(result, list)
    assert len(result) > 0
    assert all(hasattr(doc, "page_content") for doc in result)
    assert all(doc.page_content.strip() for doc in result)


def test_chunk_text_empty_input():
    """chunk_text returns an empty list for empty or whitespace-only strings."""
    assert chunk_text("") == []
    assert chunk_text("   ") == []
    assert chunk_text("\n\n") == []


def test_chunk_text_splits_long_input():
    """chunk_text produces multiple chunks when input exceeds chunk_size (1000 chars)."""
    # chunk_size=1000, chunk_overlap=200 — 5000 chars should yield multiple chunks
    long_text = "a" * 5000
    result = chunk_text(long_text)

    assert len(result) > 1, f"Expected multiple chunks, got {len(result)}"
    # Each chunk should be at most chunk_size chars
    for doc in result:
        assert len(doc.page_content) <= 1000, (
            f"Chunk exceeds chunk_size: {len(doc.page_content)} chars"
        )


def test_chunk_text_single_chunk_for_short_input():
    """chunk_text returns exactly one chunk when input is well under chunk_size."""
    short_text = "Short startup pitch under 1000 characters."
    result = chunk_text(short_text)

    assert len(result) == 1
    assert result[0].page_content == short_text
