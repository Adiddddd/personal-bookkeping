from datetime import date
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
    return render_template(
        "dashboard.html",
        wallets=result,
        total_uang=total_uang,
        today=date.today().isoformat(),
    )


@app.route("/transaction/income", methods=["POST"])
def add_income():
    wallet_id = request.form.get("destination_wallet_id")
    amount = request.form.get("amount", "0").strip()
    tx_date = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip()

    if not wallet_id:
        flash("Pilih tempat tujuan.", "error")
        return redirect(url_for("dashboard"))

    try:
        amount = float(amount)
    except ValueError:
        flash("Nominal tidak valid.", "error")
        return redirect(url_for("dashboard"))

    if amount <= 0:
        flash("Nominal harus lebih besar dari Rp0.", "error")
        return redirect(url_for("dashboard"))

    if not tx_date:
        flash("Tanggal wajib diisi.", "error")
        return redirect(url_for("dashboard"))

    conn = get_connection()
    wallet = conn.execute("SELECT name FROM wallets WHERE id = ?", (wallet_id,)).fetchone()
    if not wallet:
        conn.close()
        flash("Tempat tujuan tidak ditemukan.", "error")
        return redirect(url_for("dashboard"))

    conn.execute(
        "INSERT INTO transactions (type, amount, date, destination_wallet_id, description) "
        "VALUES ('income', ?, ?, ?, ?)",
        (amount, tx_date, wallet_id, description),
    )
    conn.commit()
    conn.close()

    flash(f"Pemasukan Rp{amount:,.0f} ke {wallet['name']} berhasil dicatat.", "success")
    return redirect(url_for("dashboard"))


@app.route("/transaction/expense", methods=["POST"])
def add_expense():
    wallet_id = request.form.get("source_wallet_id")
    amount = request.form.get("amount", "0").strip()
    tx_date = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip()

    if not wallet_id:
        flash("Pilih tempat sumber.", "error")
        return redirect(url_for("dashboard"))

    try:
        amount = float(amount)
    except ValueError:
        flash("Nominal tidak valid.", "error")
        return redirect(url_for("dashboard"))

    if amount <= 0:
        flash("Nominal harus lebih besar dari Rp0.", "error")
        return redirect(url_for("dashboard"))

    if not tx_date:
        flash("Tanggal wajib diisi.", "error")
        return redirect(url_for("dashboard"))

    conn = get_connection()
    wallet = conn.execute(
        "SELECT name, allow_expense FROM wallets WHERE id = ?", (wallet_id,)
    ).fetchone()

    if not wallet:
        conn.close()
        flash("Tempat sumber tidak ditemukan.", "error")
        return redirect(url_for("dashboard"))

    if not wallet["allow_expense"]:
        conn.close()
        flash(f'{wallet["name"]} adalah akun tabungan. Tidak bisa langsung pengeluaran. Gunakan transfer ke akun operasional terlebih dahulu.', "error")
        return redirect(url_for("dashboard"))

    balance = get_wallet_balance(conn, wallet_id)
    if amount > balance:
        conn.close()
        flash(f"Saldo {wallet['name']} tidak mencukupi. Saldo: Rp{balance:,.0f}, Pengeluaran: Rp{amount:,.0f}.", "error")
        return redirect(url_for("dashboard"))

    conn.execute(
        "INSERT INTO transactions (type, amount, date, source_wallet_id, description) "
        "VALUES ('expense', ?, ?, ?, ?)",
        (amount, tx_date, wallet_id, description),
    )
    conn.commit()
    conn.close()

    flash(f"Pengeluaran Rp{amount:,.0f} dari {wallet['name']} berhasil dicatat.", "success")
    return redirect(url_for("dashboard"))


@app.route("/transaction/transfer", methods=["POST"])
def add_transfer():
    source_id = request.form.get("source_wallet_id")
    dest_id = request.form.get("destination_wallet_id")
    amount = request.form.get("amount", "0").strip()
    tx_date = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip()

    if not source_id or not dest_id:
        flash("Pilih tempat asal dan tujuan.", "error")
        return redirect(url_for("dashboard"))

    if source_id == dest_id:
        flash("Tempat asal dan tujuan tidak boleh sama.", "error")
        return redirect(url_for("dashboard"))

    try:
        amount = float(amount)
    except ValueError:
        flash("Nominal tidak valid.", "error")
        return redirect(url_for("dashboard"))

    if amount <= 0:
        flash("Nominal harus lebih besar dari Rp0.", "error")
        return redirect(url_for("dashboard"))

    if not tx_date:
        flash("Tanggal wajib diisi.", "error")
        return redirect(url_for("dashboard"))

    conn = get_connection()

    source = conn.execute("SELECT name FROM wallets WHERE id = ?", (source_id,)).fetchone()
    if not source:
        conn.close()
        flash("Tempat asal tidak ditemukan.", "error")
        return redirect(url_for("dashboard"))

    dest = conn.execute("SELECT name FROM wallets WHERE id = ?", (dest_id,)).fetchone()
    if not dest:
        conn.close()
        flash("Tempat tujuan tidak ditemukan.", "error")
        return redirect(url_for("dashboard"))

    balance = get_wallet_balance(conn, source_id)
    if amount > balance:
        conn.close()
        flash(f"Saldo {source['name']} tidak mencukupi. Saldo: Rp{balance:,.0f}, Transfer: Rp{amount:,.0f}.", "error")
        return redirect(url_for("dashboard"))

    conn.execute(
        "INSERT INTO transactions (type, amount, date, source_wallet_id, destination_wallet_id, description) "
        "VALUES ('transfer', ?, ?, ?, ?, ?)",
        (amount, tx_date, source_id, dest_id, description),
    )
    conn.commit()
    conn.close()

    flash(f"Transfer Rp{amount:,.0f} dari {source['name']} ke {dest['name']} berhasil dicatat.", "success")
    return redirect(url_for("dashboard"))


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
    print("  Personal Bookkeeping - Tahap 3")
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
