from flask import Flask, render_template, request, redirect, jsonify, url_for
import sqlite3
import string
import random
import os

app = Flask(__name__)

# ── Database setup ──────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "urls.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                short     TEXT UNIQUE NOT NULL,
                original  TEXT NOT NULL,
                clicks    INTEGER DEFAULT 0,
                created   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()

# ── Helpers ─────────────────────────────────────────────────────
def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

def make_unique_code():
    with get_db() as conn:
        for _ in range(10):
            code = generate_code()
            exists = conn.execute("SELECT 1 FROM urls WHERE short=?", (code,)).fetchone()
            if not exists:
                return code
    raise RuntimeError("Could not generate a unique short code.")

# ── Routes ───────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json(silent=True) or {}
    original = (data.get("url") or "").strip()
    custom   = (data.get("custom") or "").strip()

    if not original:
        return jsonify({"error": "Please provide a URL."}), 400

    # Basic URL guard
    if not original.startswith(("http://", "https://")):
        original = "https://" + original

    code = custom if custom else None

    with get_db() as conn:
        if code:
            if not code.replace("-", "").replace("_", "").isalnum():
                return jsonify({"error": "Custom alias may only contain letters, numbers, - and _."}), 400
            exists = conn.execute("SELECT 1 FROM urls WHERE short=?", (code,)).fetchone()
            if exists:
                return jsonify({"error": f'"{code}" is already taken. Try another alias.'}), 409
        else:
            code = make_unique_code()

        conn.execute("INSERT INTO urls (short, original) VALUES (?, ?)", (code, original))
        conn.commit()

    short_url = url_for("redirect_short", code=code, _external=True)
    return jsonify({"short_url": short_url, "code": code})

@app.route("/<code>")
def redirect_short(code):
    with get_db() as conn:
        row = conn.execute("SELECT original FROM urls WHERE short=?", (code,)).fetchone()
        if not row:
            return render_template("404.html"), 404
        conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE short=?", (code,))
        conn.commit()
        return redirect(row["original"], 301)

@app.route("/stats/<code>")
def stats(code):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM urls WHERE short=?", (code,)).fetchone()
        if not row:
            return jsonify({"error": "Not found"}), 404
        return jsonify({
            "short":    code,
            "original": row["original"],
            "clicks":   row["clicks"],
            "created":  row["created"],
        })

@app.route("/recent")
def recent():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT short, original, clicks, created FROM urls ORDER BY id DESC LIMIT 5"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(debug=False)
