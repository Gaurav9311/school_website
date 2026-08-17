from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from database import conn
import hashlib

auth = Blueprint("auth", __name__)

# ===========================
# ADMIN LOGIN
# ===========================
@auth.route("/login.html", methods=["GET", "POST"])
def login():
    # Fixed Admin Credentials (Aap ise apne mutabiq change kar sakte hain)
    ADMIN_USERNAME = "gaurav"
    ADMIN_EMAIL = "gkg603348@gmail.com"
    ADMIN_PASSWORD = "gaurav@123#"# Safe side: aap .env ya config se bhi le sakte hain

    if request.method == "POST":
        username = request.form.get("user_name", "").strip()
        email = request.form.get("user_email", "").strip()
        password = request.form.get("user_password", "").strip()

        # Database Query ke bina Direct Check
        if username == ADMIN_USERNAME and email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            
            # Session Store
            session["admin"] = username
            session["role"] = "admin"# Role define kiya taaki marksheet page par full access mile
            session["logged_in"] = True

            return redirect(url_for("website.dashboard"))

        # Agar Credentials Match nahi hote
        return render_template(
            "login/login.html",
            error="Invalid Username, Email or Password"
        )

    return render_template("login/login.html")

# ===========================
# LOGOUT
# ===========================

@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))

# ===================================
# 1. STUDENT LOGIN ROUTE
# ===================================
@auth.route("/student_login.html", methods=["GET", "POST"])
def student_login():
    # Jab User Form Submit kare (POST Method)
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        password = request.form.get("password", "").strip()

        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE student_id = %s AND password = %s", 
            (student_id, password)
        )
        student = cursor.fetchone()
        cursor.close()

        if student:
            session["logged_in"] = True
            session["role"] = "student"
            session["student_id"] = student_id  # Session me ID store hui
            
            return redirect("/marksheet")       # Direct Result Page
        else:
            flash("Invalid Student ID or Password!", "danger")
            return redirect("/student_login.html")  # Correct URL redirect

    # Jab Browser me Login Page open ho (GET Method)
    return render_template("login/student_login.html")


# ===================================
# 2. STUDENT MARKSHEET / RESULT ROUTE
# ===================================
@auth.route("/marksheet")
def marksheet():
    # 1. Login Access Check
    if not session.get("logged_in"):
        return redirect("/student_login.html")

    # 2. Session se Student ID nikalein
    current_student_id = session.get("student_id")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM student_results WHERE roll_no=%s",
        (current_student_id,)
    )

    student_marksheet = cursor.fetchall()

    cursor.close()

    # 4. Filtered data ko HTML template me render karein (No leading '/')
    return render_template("login/student_result.html", marksheets=student_marksheet)
@auth.route("/student_logout")
def student_logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect("/student_login")