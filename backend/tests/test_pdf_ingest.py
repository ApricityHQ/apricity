"""
Unit tests for pdf_ingest.py.

No LLM calls required. Verifies extract_pdf_text() handles empty bytes and
produces the correct return type from a real in-memory PDF.
"""
import os
import sys
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf_ingest import extract_pdf_text


def _blank_pdf_bytes() -> bytes:
    """Return bytes for a minimal valid single-page PDF with no text content."""
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = BytesIO()
    writer.write(buf)
    return buf.getvalue()


def test_extract_pdf_text_empty_bytes():
    """extract_pdf_text returns empty string for empty input."""
    assert extract_pdf_text(b"") == ""


def test_extract_pdf_text_valid_pdf_returns_string():
    """extract_pdf_text returns a str (possibly empty) for a valid PDF, never raises."""
    result = extract_pdf_text(_blank_pdf_bytes())
    assert isinstance(result, str)


def test_extract_pdf_text_return_type_is_always_str():
    """extract_pdf_text always returns str, not None or any other type."""
    assert type(extract_pdf_text(b"")) is str
    assert type(extract_pdf_text(_blank_pdf_bytes())) is str
