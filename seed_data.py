from models import get_connection

DEFAULT_WALLETS = [
    {"name": "Dompet", "initial_balance": 0, "allow_expense": 1},
    {"name": "DANA", "initial_balance": 0, "allow_expense": 1},
    {"name": "Wondr BNI", "initial_balance": 0, "allow_expense": 1},
    {"name": "SeaBank", "initial_balance": 0, "allow_expense": 0},
]


def seed_wallets():
    conn = get_connection()
    existing = conn.execute("SELECT COUNT(*) as cnt FROM wallets").fetchone()["cnt"]

    if existing > 0:
        print(f"[SKIP] {existing} wallet(s) already exist. Skipping seed.")
        conn.close()
        return False

    for w in DEFAULT_WALLETS:
        conn.execute(
            "INSERT INTO wallets (name, initial_balance, allow_expense) VALUES (?, ?, ?)",
            (w["name"], w["initial_balance"], w["allow_expense"]),
        )

    conn.commit()
    conn.close()
    print("[OK] Default wallets seeded: Dompet, DANA, Wondr BNI, SeaBank")
    return True


def show_wallets():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM wallets ORDER BY id").fetchall()
    conn.close()

    print("\n--- Daftar Wallet ---")
    print(f"{'ID':<5} {'Nama':<15} {'Saldo Awal':<15} {'Izin Expense':<12}")
    print("-" * 50)
    for r in rows:
        izin = "Ya" if r["allow_expense"] else "Tidak"
        print(f"{r['id']:<5} {r['name']:<15} Rp{r['initial_balance']:<13,.0f} {izin:<12}")
    print()
