"""SQLite database for offset tracking and command/error logging"""

import sqlite3
from contextlib import contextmanager
from config import DB_PATH

# Ensure parent directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS offsets (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    offset INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS command_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    chat_id TEXT,
    command TEXT,
    args TEXT,
    status TEXT,
    response TEXT
);

CREATE TABLE IF NOT EXISTS error_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    context TEXT,
    error TEXT
);
"""

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init():
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        conn.execute("INSERT OR IGNORE INTO offsets (id, offset) VALUES (1, 0)")

def get_offset():
    with get_conn() as conn:
        row = conn.execute("SELECT offset FROM offsets WHERE id = 1").fetchone()
        return row['offset'] if row else 0

def set_offset(offset):
    with get_conn() as conn:
        conn.execute("UPDATE offsets SET offset = ? WHERE id = 1", (offset,))

def log_command(chat_id, command, args, status, response):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO command_log (chat_id, command, args, status, response) VALUES (?, ?, ?, ?, ?)",
            (chat_id, command, args, status, response)
        )

def log_error(context, error):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO error_log (context, error) VALUES (?, ?)",
            (context, error)
        )
