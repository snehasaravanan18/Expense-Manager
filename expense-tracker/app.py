import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("SELECT COUNT(*) FROM expenses")
    count = cur.fetchone()[0]
    if count == 0:
        sample_data = [
            ("Grocery Run", 87.50, "Food & Dining"),
            ("Netflix Subscription", 15.99, "Entertainment"),
            ("Electric Bill", 120.00, "Utilities"),
            ("Gym Membership", 45.00, "Health & Fitness"),
            ("Uber Ride", 22.30, "Transportation"),
            ("Amazon Purchase", 63.45, "Shopping"),
            ("Coffee Shop", 18.75, "Food & Dining"),
            ("Spotify", 9.99, "Entertainment"),
            ("Internet Bill", 75.00, "Utilities"),
            ("Doctor Visit Copay", 30.00, "Health & Fitness"),
        ]
        cur.executemany(
            "INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)",
            sample_data
        )
    conn.commit()
    conn.close()


CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Utilities",
    "Health & Fitness",
    "Travel",
    "Education",
    "Other",
]


@app.route("/")
def index():
    return render_template("add.html", categories=CATEGORIES)


@app.route("/expenses")
def expenses():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY created_at DESC")
    all_expenses = cur.fetchall()
    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0] or 0.0
    cur.execute(
        "SELECT category, SUM(amount) as total FROM expenses GROUP BY category ORDER BY total DESC"
    )
    chart_data = cur.fetchall()
    conn.close()
    return render_template(
        "expenses.html",
        expenses=all_expenses,
        total=total,
        chart_labels=[row["category"] for row in chart_data],
        chart_values=[row["total"] for row in chart_data],
    )


@app.route("/add", methods=["POST"])
def add_expense():
    name = request.form.get("name", "").strip()
    amount = request.form.get("amount", "0").strip()
    category = request.form.get("category", "Other").strip()
    if not name or not amount:
        return redirect(url_for("index"))
    try:
        amount = float(amount)
    except ValueError:
        return redirect(url_for("index"))
    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)",
        (name, amount, category),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("expenses"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("expenses"))


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
