from __future__ import annotations

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Inputs shorter than this threshold are passed directly to agents without
# chunking. At ~4000 chars (~1000 tokens) the full text fits comfortably in
# context and RAG retrieval only adds fragmentation overhead.
RAG_THRESHOLD = 4000


def should_chunk(text: str, threshold: int = RAG_THRESHOLD) -> bool:
    """
    Determine whether the input text is long enough to benefit from RAG chunking.

    For short inputs (e.g. a typed startup pitch), passing the full text directly
    to the LLM produces better results than chunking and retrieving fragments.
    RAG becomes useful once PDFs or other long documents push the input past the
    threshold where the full text no longer fits cleanly in a single context window.

    Args:
        text: The combined input text (startup prompt + any extracted PDF content).
        threshold: Character length above which chunking is applied. Defaults to
            RAG_THRESHOLD (4000 chars ≈ 1000 tokens).

    Returns:
        True if the text should be chunked and indexed for retrieval, False if it
        should be passed directly as context.
    """
    return len(text) > threshold


def chunk_text(text: str) -> list[Document]:
    if not text or not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = [Document(page_content=text)]
    return splitter.split_documents(docs)
