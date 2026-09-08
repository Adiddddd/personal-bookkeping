from flask import Flask, render_template, request, redirect, url_for, flash
from models import init_db, get_connection, get_wallet_balance
from seed_data import seed_wallets, show_wallets

app = Flask(__name__)
app.secret_key = "bookkeeping-dev-key"


@app.route("/")
def dashboard():
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
    return render_template("dashboard.html", wallets=result, total_uang=total_uang)


@app.route("/wallet/add", methods=["POST"])
def add_wallet():
    name = request.form.get("name", "").strip()
    initial_balance = request.form.get("initial_balance", "0")
    allow_expense = 1 if request.form.get("allow_expense") else 0

    if not name:
        flash("Nama tempat wajib diisi.", "error")
        return redirect(url_for("dashboard"))

    try:
        initial_balance = float(initial_balance)
    except ValueError:
        flash("Saldo awal tidak valid.", "error")
        return redirect(url_for("dashboard"))

    conn = get_connection()
    existing = conn.execute("SELECT id FROM wallets WHERE name = ?", (name,)).fetchone()
    if existing:
        conn.close()
        flash(f'Nama "{name}" sudah digunakan.', "error")
        return redirect(url_for("dashboard"))

    conn.execute(
        "INSERT INTO wallets (name, initial_balance, allow_expense) VALUES (?, ?, ?)",
        (name, initial_balance, allow_expense),
    )
    conn.commit()
    conn.close()

    flash(f'Tempat "{name}" berhasil ditambahkan.', "success")
    return redirect(url_for("dashboard"))


@app.route("/wallet/delete", methods=["POST"])
def delete_wallet():
    wallet_id = request.form.get("wallet_id")
    if not wallet_id:
        return redirect(url_for("dashboard"))

    conn = get_connection()
    wallet = conn.execute("SELECT name FROM wallets WHERE id = ?", (wallet_id,)).fetchone()
    if wallet:
        conn.execute("DELETE FROM transactions WHERE source_wallet_id = ? OR destination_wallet_id = ?", (wallet_id, wallet_id))
        conn.execute("DELETE FROM wallets WHERE id = ?", (wallet_id,))
        conn.commit()
        flash(f'Tempat "{wallet["name"]}" berhasil dihapus.', "success")
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    print("=" * 50)
    print("  Personal Bookkeeping - Tahap 2")
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
