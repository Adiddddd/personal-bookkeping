<div align="center">

# Personal Bookkeeping

### A Modern Personal Financial Management Web App

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)

*A sleek, fintech-inspired web application for tracking personal cash flow across multiple wallets and accounts.*

</div>

---

## About

**Personal Bookkeeping** is a lightweight, responsive web application designed for personal financial management. It allows users to monitor real-time balances across multiple storage locations (cash, e-wallets, bank accounts, savings), record income and expense transactions, and transfer funds between accounts — all with automated balance recalculation and business rule enforcement.

Built with a clean Python backend (Flask + SQLite) and a modern Tailwind CSS frontend, the app runs locally and requires no external services.

---

## Key Features

### Multi-Wallet & Storage Management
- Create and manage multiple wallets: cash (Dompet), digital wallets (DANA, Gopay), bank accounts (BNI, SeaBank), and more.
- Each wallet maintains an independent balance with its own initial balance setting.
- Dashboard displays all wallets in a responsive grid with real-time balance cards.

### Smart Rules & Savings Protection
- **Operational Wallets** — Allow direct income, expense, and transfer transactions.
- **Savings Accounts** — Protected from direct expenses. Users must transfer funds to an operational wallet before spending.
- Prevents negative balances through real-time validation on every transaction.

### Transaction Engine
- **Income** — Record money flowing into any wallet from external sources.
- **Expense** — Record money flowing out of operational wallets for purchases and bills.
- **Internal Transfer** — Move funds between wallets with zero change to total net worth.
- All balances are recalculated automatically on every add, edit, or delete operation.

### Interactive UI/UX
- Modern fintech-style dashboard with gradient hero card showing total net worth.
- Dynamic cross-filtering in transfer dropdowns (prevents selecting the same wallet for source and destination).
- Responsive layout optimized for both desktop and mobile screens.
- Status badges distinguishing operational vs. savings accounts.

### Transaction History & Management
- Color-coded transaction log: **Green** for income, **Red** for expense, **Blue** for transfer.
- Inline edit and delete buttons on every transaction row with confirmation dialogs.
- **Clear History** feature safely removes all transaction records while preserving current wallet balances (adjusts `initial_balance` to match current balance before clearing).
- Empty state displayed when no transactions exist.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.x, Flask 3.0.3 |
| **Database** | SQLite (via Python `sqlite3`) |
| **Frontend** | HTML5, Tailwind CSS (CDN), Vanilla JavaScript |
| **Fonts** | Plus Jakarta Sans (Google Fonts) |

---

## Project Structure

```
personal-bookkeeping/
├── app.py              # Flask application — routes & business logic
├── models.py           # Database schema, connection, balance calculations
├── seed_data.py        # Default wallet seeding (Dompet, DANA, Wondr BNI, SeaBank)
├── bookkeeping.db      # SQLite database file (auto-created)
├── requirements.txt    # Python dependencies
├── templates/
│   ├── base.html       # Layout template — navbar, modals, flash messages
│   └── dashboard.html  # Main dashboard — wallets, quick actions, transaction history
├── static/             # Static assets (currently empty)
└── venv/               # Python virtual environment
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher installed on your system.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/personal-bookkeeping.git
   cd personal-bookkeeping
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python app.py
   ```

5. **Open your browser and navigate to:**

   ```
   http://127.0.0.1:5000
   ```

On first launch, the app automatically initializes the SQLite database and seeds four default wallets: **Dompet** (Cash), **DANA** (E-Wallet), **Wondr BNI** (Bank), and **SeaBank** (Savings).

---

## Business Rules

| Rule | Description |
|------|-------------|
| **Nominal > 0** | All transactions must have an amount greater than Rp0. |
| **No Negative Balance** | Expenses and outbound transfers are rejected if the source wallet has insufficient funds. |
| **Source ≠ Destination** | Transfer source and destination must be different wallets. |
| **Savings Protection** | Wallets marked as savings cannot be used as expense sources. |
| **Total Immutability on Transfer** | Internal transfers do not change the total net worth across all wallets. |
| **Real-time Recalculation** | Every add, edit, or delete triggers automatic balance recalculation. |

---

## Default Wallets

| Wallet | Category | Income | Expense | Transfer |
|--------|----------|:------:|:-------:|:--------:|
| Dompet | Operational (Cash) | Yes | Yes | Yes |
| DANA | Operational (E-Wallet) | Yes | Yes | Yes |
| Wondr BNI | Operational (Bank) | Yes | Yes | Yes |
| SeaBank | Savings | Yes | **No** | Yes |

---

## License

This project is for personal use. Feel free to fork and modify for your own needs.
