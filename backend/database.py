from __future__ import annotations
import aiosqlite
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).parent / "mediai.db"

_CREATE_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS sessions (
    id         TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    urgency    TEXT DEFAULT 'LOW'
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role       TEXT NOT NULL CHECK(role IN ('user','ai')),
    content    TEXT NOT NULL,
    timestamp  TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detected_symptoms (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id   TEXT NOT NULL,
    symptom_id   TEXT NOT NULL,
    symptom_name TEXT NOT NULL,
    severity     INTEGER NOT NULL,
    timestamp    TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
"""


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(_CREATE_SQL)
        await db.commit()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Session helpers ───────────────────────────────────────────────────────────

async def upsert_session(session_id: str, urgency: str = "LOW") -> None:
    now = _now()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO sessions(id, created_at, updated_at, urgency)
               VALUES(?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET updated_at=excluded.updated_at, urgency=excluded.urgency""",
            (session_id, now, now, urgency)
        )
        await db.commit()


async def get_sessions(limit: int = 20) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """SELECT s.id, s.created_at as date, s.urgency,
                      COUNT(m.id) as msg_count,
                      MIN(CASE WHEN m.role='user' THEN m.content END) as first_msg
               FROM sessions s
               LEFT JOIN messages m ON m.session_id = s.id
               GROUP BY s.id
               ORDER BY s.updated_at DESC
               LIMIT ?""",
            (limit,)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def delete_all_sessions() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM detected_symptoms")
        await db.execute("DELETE FROM messages")
        await db.execute("DELETE FROM sessions")
        await db.commit()


# ── Message helpers ───────────────────────────────────────────────────────────

async def add_message(session_id: str, role: str, content: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO messages(session_id, role, content, timestamp) VALUES(?,?,?,?)",
            (session_id, role, content, _now())
        )
        await db.commit()


async def get_messages(session_id: str) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT role, content, timestamp FROM messages WHERE session_id=? ORDER BY id",
            (session_id,)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


# ── Symptom helpers ───────────────────────────────────────────────────────────

async def upsert_symptoms(session_id: str, symptoms: list[dict]) -> None:
    now = _now()
    async with aiosqlite.connect(DB_PATH) as db:
        for s in symptoms:
            # Replace (upsert) by symptom_id per session
            await db.execute(
                """INSERT INTO detected_symptoms(session_id, symptom_id, symptom_name, severity, timestamp)
                   VALUES(?,?,?,?,?)
                   ON CONFLICT DO NOTHING""",
                (session_id, s["id"], s["name"], s["severity"], now)
            )
        await db.commit()


async def get_session_symptoms(session_id: str) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT symptom_id as id, symptom_name as name, severity FROM detected_symptoms WHERE session_id=? ORDER BY id",
            (session_id,)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]
