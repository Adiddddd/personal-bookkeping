import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bookkeeping.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            initial_balance REAL NOT NULL DEFAULT 0,
            allow_expense INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense', 'transfer')),
            amount REAL NOT NULL CHECK(amount > 0),
            date TEXT NOT NULL,
            source_wallet_id INTEGER,
            destination_wallet_id INTEGER,
            description TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (source_wallet_id) REFERENCES wallets(id),
            FOREIGN KEY (destination_wallet_id) REFERENCES wallets(id)
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] Database initialized.")


def get_wallet_balance(conn, wallet_id):
    row = conn.execute(
        "SELECT initial_balance FROM wallets WHERE id = ?", (wallet_id,)
    ).fetchone()
    if not row:
        return 0

    initial = row["initial_balance"]

    income = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM transactions "
        "WHERE destination_wallet_id = ? AND type = 'income'",
        (wallet_id,),
    ).fetchone()["total"]

    expense = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM transactions "
        "WHERE source_wallet_id = ? AND type = 'expense'",
        (wallet_id,),
    ).fetchone()["total"]

    transfer_in = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM transactions "
        "WHERE destination_wallet_id = ? AND type = 'transfer'",
        (wallet_id,),
    ).fetchone()["total"]

    transfer_out = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM transactions "
        "WHERE source_wallet_id = ? AND type = 'transfer'",
        (wallet_id,),
    ).fetchone()["total"]

    return initial + income + transfer_in - expense - transfer_out


def recalculate_all_balances():
    conn = get_connection()
    wallets = conn.execute("SELECT id FROM wallets").fetchall()
    results = {}
    for w in wallets:
        results[w["id"]] = get_wallet_balance(conn, w["id"])
    conn.close()
    return results
