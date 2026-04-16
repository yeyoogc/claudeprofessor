"""
SQLite store for pending verifications and sent DMs.
No ORM — keeps the dependency footprint minimal.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "claudeprofessor.db")


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS verifications (
                ig_user_id   TEXT PRIMARY KEY,
                ig_username  TEXT,
                token        TEXT NOT NULL,
                created_at   TEXT NOT NULL,
                verified     INTEGER NOT NULL DEFAULT 0,
                verified_at  TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS dm_log (
                ig_user_id  TEXT NOT NULL,
                media_id    TEXT,
                sent_at     TEXT NOT NULL
            )
        """)
        c.commit()


def already_dm_sent(ig_user_id: str, media_id: str) -> bool:
    """Prevent duplicate DMs for the same post."""
    with _conn() as c:
        row = c.execute(
            "SELECT 1 FROM dm_log WHERE ig_user_id=? AND media_id=?",
            (ig_user_id, media_id),
        ).fetchone()
    return row is not None


def log_dm(ig_user_id: str, media_id: str):
    with _conn() as c:
        c.execute(
            "INSERT INTO dm_log(ig_user_id, media_id, sent_at) VALUES(?,?,?)",
            (ig_user_id, media_id, datetime.utcnow().isoformat()),
        )
        c.commit()


def add_pending(ig_user_id: str, token: str, ig_username: str = ""):
    with _conn() as c:
        c.execute(
            """INSERT INTO verifications(ig_user_id, ig_username, token, created_at)
               VALUES(?,?,?,?)
               ON CONFLICT(ig_user_id) DO UPDATE SET token=excluded.token,
               created_at=excluded.created_at, verified=0""",
            (ig_user_id, ig_username, token, datetime.utcnow().isoformat()),
        )
        c.commit()


def get_pending(token: str) -> dict | None:
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM verifications WHERE token=? AND verified=0",
            (token,),
        ).fetchone()
    return dict(row) if row else None


def get_by_user_id(ig_user_id: str) -> dict | None:
    with _conn() as c:
        row = c.execute(
            "SELECT * FROM verifications WHERE ig_user_id=?",
            (ig_user_id,),
        ).fetchone()
    return dict(row) if row else None


def mark_verified(ig_user_id: str):
    with _conn() as c:
        c.execute(
            "UPDATE verifications SET verified=1, verified_at=? WHERE ig_user_id=?",
            (datetime.utcnow().isoformat(), ig_user_id),
        )
        c.commit()
