import aiosqlite
import json
import uuid
import datetime

DATABASE_URL = "ssp.db"

async def get_db():
    db = await aiosqlite.connect(DATABASE_URL)
    # Important connection settings for SQLite concurrency and stability
    await db.execute("PRAGMA journal_mode=WAL;")
    await db.execute("PRAGMA synchronous=NORMAL;")
    # Return Dict-like rows
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                prompt TEXT NOT NULL,
                result JSON NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                report_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
            )
        """)
        await db.commit()

async def save_report(db: aiosqlite.Connection, user_id: str, prompt: str, result: dict):
    report_id = str(uuid.uuid4())
    created_at = datetime.datetime.now(datetime.UTC).isoformat()
    await db.execute(
        "INSERT INTO reports (id, user_id, prompt, result, created_at) VALUES (?, ?, ?, ?, ?)",
        (report_id, user_id, prompt, json.dumps(result), created_at)
    )
    await db.commit()
    return report_id

async def get_user_reports(db: aiosqlite.Connection, user_id: str):
    async with db.execute("SELECT * FROM reports WHERE user_id = ? ORDER BY created_at DESC", (user_id,)) as cursor:
        rows = await cursor.fetchall()
        reports = []
        for row in rows:
            reports.append({
                "id": row["id"],
                "user_id": row["user_id"],
                "prompt": row["prompt"],
                "result": json.loads(row["result"]),
                "created_at": row["created_at"],
            })
        return reports

async def get_report_by_id(db: aiosqlite.Connection, user_id: str, report_id: str):
    async with db.execute("SELECT * FROM reports WHERE user_id = ? AND id = ?", (user_id, report_id)) as cursor:
        row = await cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "prompt": row["prompt"],
            "result": json.loads(row["result"]),
            "created_at": row["created_at"],
        }

async def save_message(db: aiosqlite.Connection, report_id: str, role: str, content: str) -> str:
    message_id = str(uuid.uuid4())
    created_at = datetime.datetime.now(datetime.UTC).isoformat()
    await db.execute(
        "INSERT INTO messages (id, report_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
        (message_id, report_id, role, content, created_at)
    )
    await db.commit()
    return message_id

async def get_report_messages(db: aiosqlite.Connection, report_id: str) -> list[dict]:
    async with db.execute("SELECT * FROM messages WHERE report_id = ? ORDER BY created_at ASC", (report_id,)) as cursor:
        rows = await cursor.fetchall()
        messages = []
        for row in rows:
            messages.append({
                "id": row["id"],
                "report_id": row["report_id"],
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"],
            })
        return messages
