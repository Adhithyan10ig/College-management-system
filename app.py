from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import users_col, students_col, faculty_col, courses_col, attendance_col, marks_col, fees_col
from bson import ObjectId
import json, datetime

app = Flask(__name__)
app.secret_key = "college_secret_key_2024"

# ─── Helper ───────────────────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def str_id(doc):
    """Convert ObjectId fields to string for JSON serialization."""
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

# ─── Auth ─────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = users_col.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            session["role"] = user.get("role", "admin")
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ─── Dashboard ────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "students": students_col.count_documents({}),
        "faculty":  faculty_col.count_documents({}),
        "courses":  courses_col.count_documents({}),
        "fees_pending": fees_col.count_documents({"status": "pending"}),
    }
    return render_template("dashboard.html", stats=stats, user=session["user"], role=session["role"])

# ─── Students ─────────────────────────────────────────
@app.route("/students")
@login_required
def students():
    all_students = list(students_col.find())
    for s in all_students:
        s["_id"] = str(s["_id"])
    return render_template("students.html", students=all_students, user=session["user"])

@app.route("/api/students", methods=["POST"])
@login_required
def add_student():
    data = request.json
    data["created_at"] = datetime.datetime.utcnow()
    students_col.insert_one(data)
    return jsonify({"success": True})

@app.route("/api/students/<sid>", methods=["DELETE"])
@login_required
def delete_student(sid):
    students_col.delete_one({"_id": ObjectId(sid)})
    return jsonify({"success": True})

# ─── Faculty ──────────────────────────────────────────
@app.route("/faculty")
@login_required
def faculty():
    all_faculty = list(faculty_col.find())
    for f in all_faculty:
        f["_id"] = str(f["_id"])
    return render_template("faculty.html", faculty=all_faculty, user=session["user"])

@app.route("/api/faculty", methods=["POST"])
@login_required
def add_faculty():
    data = request.json
    data["created_at"] = datetime.datetime.utcnow()
    faculty_col.insert_one(data)
    return jsonify({"success": True})

@app.route("/api/faculty/<fid>", methods=["DELETE"])
@login_required
def delete_faculty(fid):
    faculty_col.delete_one({"_id": ObjectId(fid)})
    return jsonify({"success": True})

# ─── Courses ──────────────────────────────────────────
@app.route("/courses")
@login_required
def courses():
    all_courses = list(courses_col.find())
    for c in all_courses:
        c["_id"] = str(c["_id"])
    return render_template("courses.html", courses=all_courses, user=session["user"])

@app.route("/api/courses", methods=["POST"])
@login_required
def add_course():
    data = request.json
    courses_col.insert_one(data)
    return jsonify({"success": True})

# ─── Attendance ───────────────────────────────────────
@app.route("/attendance")
@login_required
def attendance():
    all_students = list(students_col.find({}, {"name": 1, "roll_no": 1}))
    all_courses  = list(courses_col.find({}, {"name": 1, "code": 1}))
    for x in all_students + all_courses:
        x["_id"] = str(x["_id"])
    records = list(attendance_col.find().sort("date", -1).limit(50))
    for r in records:
        r["_id"] = str(r["_id"])
    return render_template("attendance.html", students=all_students, courses=all_courses,
                           records=records, user=session["user"])

@app.route("/api/attendance", methods=["POST"])
@login_required
def mark_attendance():
    data = request.json
    data["date"] = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    attendance_col.insert_one(data)
    return jsonify({"success": True})

# ─── Marks ────────────────────────────────────────────
@app.route("/marks")
@login_required
def marks():
    all_students = list(students_col.find({}, {"name": 1, "roll_no": 1}))
    all_courses  = list(courses_col.find({}, {"name": 1, "code": 1}))
    for x in all_students + all_courses:
        x["_id"] = str(x["_id"])
    records = list(marks_col.find().limit(50))
    for r in records:
        r["_id"] = str(r["_id"])
    return render_template("marks.html", students=all_students, courses=all_courses,
                           records=records, user=session["user"])

@app.route("/api/marks", methods=["POST"])
@login_required
def add_marks():
    data = request.json
    marks_col.insert_one(data)
    return jsonify({"success": True})

# ─── Fees ─────────────────────────────────────────────
@app.route("/fees")
@login_required
def fees():
    all_students = list(students_col.find({}, {"name": 1, "roll_no": 1}))
    for s in all_students:
        s["_id"] = str(s["_id"])
    records = list(fees_col.find().limit(50))
    for r in records:
        r["_id"] = str(r["_id"])
    return render_template("fees.html", students=all_students, records=records, user=session["user"])

@app.route("/api/fees", methods=["POST"])
@login_required
def add_fee():
    data = request.json
    fees_col.insert_one(data)
    return jsonify({"success": True})

@app.route("/api/fees/<fid>/pay", methods=["POST"])
@login_required
def pay_fee(fid):
    fees_col.update_one({"_id": ObjectId(fid)}, {"$set": {"status": "paid"}})
    return jsonify({"success": True})

# ─── Seed admin user ──────────────────────────────────
def seed_admin():
    if not users_col.find_one({"username": "admin"}):
        users_col.insert_one({
            "username": "admin",
            "password": generate_password_hash("admin123"),
            "role": "admin"
        })
        print("✅ Admin user created: admin / admin123")
@app.route("/setup")
def setup():
    users_col.delete_many({"username": "admin"})
    users_col.insert_one({
        "username": "admin",
        "password": generate_password_hash("admin123"),
        "role": "admin"
    })
    return "Admin user created! Go to /login now."
if __name__ == "__main__":
    app.run(debug=True)
