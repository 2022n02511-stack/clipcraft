import os
import sqlite3
from pathlib import Path


DATA_DIR = Path(
    os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
) / "clipcraft"

DB_PATH = DATA_DIR / "history.db"
MAX_HISTORY = 100


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS clipboard_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original TEXT NOT NULL,
            formatted TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    return connection


def save(original, formatted):
    if not original:
        return

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO clipboard_history (original, formatted)
            VALUES (?, ?)
            """,
            (original, formatted)
        )

        connection.execute(
            """
            DELETE FROM clipboard_history
            WHERE id NOT IN (
                SELECT id FROM clipboard_history
                ORDER BY id DESC
                LIMIT ?
            )
            """,
            (MAX_HISTORY,)
        )


def get_recent(limit=10):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT original, formatted
            FROM clipboard_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return rows


def clear():
    with get_connection() as connection:
        connection.execute("DELETE FROM clipboard_history")


if __name__ == "__main__":
    print("Database:", DB_PATH)
    print("Current entries:", len(get_recent(100)))
