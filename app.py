from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Initialize DB when app starts
init_db()

app.secret_key = "your_secret_key_here"


# ===========================================================
#  DATABASE CONNECTION
# ===========================================================
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


# ===========================================================
#  HOME
# ===========================================================
@app.route("/")
def home():
    return render_template("home.html")


# ===========================================================
#  SIGNUP
# ===========================================================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Check duplicate user
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "User already exists!"

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# ===========================================================
#  LOGIN
# ===========================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None   # To send errors back to page

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            error_message = "❌ User does not exist!"
        else:
            stored_hash = user[0]
            if not check_password_hash(stored_hash, password):
                error_message = "❌ Incorrect password!"
            else:
                session["user"] = username
                return redirect("/dashboard")

    return render_template("login.html", error=error_message)


# ===========================================================
#  DASHBOARD (PROTECTED)
# ===========================================================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", username=session["user"])


# ===========================================================
#  PROFILE (PROTECTED)
# ===========================================================
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    return render_template("profile.html", username=session["user"])


# ===========================================================
#  LOGOUT
# ===========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ===========================================================
#  MAIN
# ===========================================================
if __name__ == "__main__":
    app.run(debug=True)
