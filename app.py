from flask import Flask, render_template, redirect, url_for, session, request
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "college2024secretkey")

# ─── Auth ─────────────────────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin123":
            session["user"] = username
            session["role"] = "admin"
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    stats = {"students": 0, "faculty": 0, "courses": 0, "fees_pending": 0}
    return render_template("dashboard.html", stats=stats, user=session["user"], role=session["role"])

@app.route("/students")
@login_required
def students():
    return render_template("students.html", students=[], user=session["user"])

@app.route("/faculty")
@login_required
def faculty():
    return render_template("faculty.html", faculty=[], user=session["user"])

@app.route("/courses")
@login_required
def courses():
    return render_template("courses.html", courses=[], user=session["user"])

@app.route("/attendance")
@login_required
def attendance():
    return render_template("attendance.html", students=[], courses=[], records=[], user=session["user"])

@app.route("/marks")
@login_required
def marks():
    return render_template("marks.html", students=[], courses=[], records=[], user=session["user"])

@app.route("/fees")
@login_required
def fees():
    return render_template("fees.html", students=[], records=[], user=session["user"])

if __name__ == "__main__":
    app.run(debug=True)