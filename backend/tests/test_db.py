"""
Integration tests for the database layer (db.py).

Uses a real temporary SQLite file — no mocks. Tests cover:
- Report save and retrieval round-trip
- User data isolation (users only see their own reports)
- Message save and retrieval round-trip
- Cascade delete (messages removed with their parent report)
"""
import os
import sys

import aiosqlite
import pytest
import pytest_asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import db as db_module


@pytest_asyncio.fixture
async def test_db(tmp_path):
    """
    Provide an isolated aiosqlite connection pointed at a temp DB file.

    Args:
        tmp_path: pytest-provided temporary directory.

    Yields:
        An open aiosqlite.Connection with the schema initialized.
    """
    db_path = str(tmp_path / "test_ssp.db")
    original_url = db_module.DATABASE_URL
    db_module.DATABASE_URL = db_path

    await db_module.init_db()

    conn = await aiosqlite.connect(db_path)
    await conn.execute("PRAGMA journal_mode=WAL;")
    await conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = aiosqlite.Row

    yield conn

    await conn.close()
    db_module.DATABASE_URL = original_url


@pytest.mark.asyncio
async def test_save_and_retrieve_report(test_db):
    """
    save_report followed by get_report_by_id returns the same data.

    Args:
        test_db: Isolated database connection fixture.
    """
    result_data = {"financial": "looks good", "vc": "strong team"}
    report_id = await db_module.save_report(test_db, "user_1", "my pitch", result_data)

    assert isinstance(report_id, str) and report_id

    report = await db_module.get_report_by_id(test_db, "user_1", report_id)
    assert report is not None
    assert report["id"] == report_id
    assert report["user_id"] == "user_1"
    assert report["prompt"] == "my pitch"
    assert report["result"] == result_data


@pytest.mark.asyncio
async def test_get_user_reports_returns_only_own(test_db):
    """
    Each user only sees their own reports — not other users' data.

    Args:
        test_db: Isolated database connection fixture.
    """
    await db_module.save_report(test_db, "user_A", "pitch A", {"score": 80})
    await db_module.save_report(test_db, "user_B", "pitch B", {"score": 60})

    reports_a = await db_module.get_user_reports(test_db, "user_A")
    reports_b = await db_module.get_user_reports(test_db, "user_B")

    assert len(reports_a) == 1
    assert reports_a[0]["user_id"] == "user_A"

    assert len(reports_b) == 1
    assert reports_b[0]["user_id"] == "user_B"


@pytest.mark.asyncio
async def test_get_report_by_id_wrong_user_returns_none(test_db):
    """
    get_report_by_id returns None when the report_id belongs to a different user.

    Args:
        test_db: Isolated database connection fixture.
    """
    report_id = await db_module.save_report(test_db, "user_A", "secret pitch", {})
    result = await db_module.get_report_by_id(test_db, "user_B", report_id)
    assert result is None


@pytest.mark.asyncio
async def test_save_and_retrieve_messages(test_db):
    """
    save_message followed by get_report_messages returns messages in order.

    Args:
        test_db: Isolated database connection fixture.
    """
    report_id = await db_module.save_report(test_db, "user_1", "pitch", {})

    msg_id_1 = await db_module.save_message(test_db, report_id, "user", "hello")
    msg_id_2 = await db_module.save_message(test_db, report_id, "assistant", "world")

    messages = await db_module.get_report_messages(test_db, report_id)
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "hello"
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "world"


@pytest.mark.asyncio
async def test_cascade_delete_messages(test_db):
    """
    Deleting a report also deletes its associated messages (ON DELETE CASCADE).

    Args:
        test_db: Isolated database connection fixture.
    """
    report_id = await db_module.save_report(test_db, "user_1", "pitch", {})
    await db_module.save_message(test_db, report_id, "user", "msg 1")
    await db_module.save_message(test_db, report_id, "assistant", "msg 2")

    # Confirm messages exist before deletion
    messages_before = await db_module.get_report_messages(test_db, report_id)
    assert len(messages_before) == 2

    # Delete the parent report
    await test_db.execute("PRAGMA foreign_keys = ON;")
    await test_db.execute("DELETE FROM reports WHERE id = ?", (report_id,))
    await test_db.commit()

    # Messages should be gone due to CASCADE
    messages_after = await db_module.get_report_messages(test_db, report_id)
    assert len(messages_after) == 0
