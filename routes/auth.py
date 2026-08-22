from flask import Blueprint, render_template, request, redirect, session, url_for, make_response

auth = Blueprint("auth", __name__)


# ===========================
# ADMIN LOGIN
# ===========================
@auth.route("/login.html", methods=["GET", "POST"])
def login():

    ADMIN_USERNAME = "gaurav"
    ADMIN_EMAIL = "gkg603348@gmail.com"
    ADMIN_PASSWORD = "gaurav@123#"

    # Already logged in
    if session.get("logged_in"):
        return redirect(url_for("website.dashboard"))

    if request.method == "POST":

        username = request.form.get("user_name", "").strip()
        email = request.form.get("user_email", "").strip()
        password = request.form.get("user_password", "").strip()

        if (
            username == ADMIN_USERNAME
            and email == ADMIN_EMAIL
            and password == ADMIN_PASSWORD
        ):

            session["admin"] = username
            session["role"] = "admin"
            session["logged_in"] = True

            return redirect(url_for("website.dashboard"))

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

    # Session completely remove
    session.clear()

    response = redirect(url_for("auth.login"))

    # Browser cache disable
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response