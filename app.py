from flask import Flask, jsonify
from models import init_db, get_connection, get_wallet_balance
from seed_data import seed_wallets, show_wallets

app = Flask(__name__)


@app.route("/")
def index():
    conn = get_connection()
    wallets = conn.execute("SELECT * FROM wallets ORDER BY id").fetchall()

    result = []
    total_uang = 0
    for w in wallets:
        balance = get_wallet_balance(conn, w["id"])
        total_uang += balance
        result.append({
            "id": w["id"],
            "name": w["name"],
            "initial_balance": w["initial_balance"],
            "allow_expense": bool(w["allow_expense"]),
            "current_balance": balance,
        })

    conn.close()
    return jsonify({
        "total_uang": total_uang,
        "wallets": result,
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("=" * 50)
    print("  Personal Bookkeeping - Tahap 1")
    print("=" * 50)

    print("\n[1/3] Initializing database...")
    init_db()

    print("[2/3] Seeding default wallets...")
    seed_wallets()

    print("[3/3] Current wallet data:")
    show_wallets()

    print("[DONE] Database and seed data ready!")
    print("[RUN] Starting Flask server on http://127.0.0.1:5000\n")

    app.run(debug=True, port=5000)
