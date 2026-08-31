
from flask import Blueprint,render_template,request,redirect,session,url_for,make_response

from functools import wraps


# ============================================================
# AUTHENTICATION BLUEPRINT
# ============================================================
auth = Blueprint("auth", __name__)


# ============================================================
# ADMIN CREDENTIALS
# IMPORTANT: DO NOT CHANGE THESE VALUES
# ============================================================
ADMIN_USERNAME = "gaurav"
ADMIN_EMAIL = "gkg603348@gmail.com"
ADMIN_PASSWORD = "gaurav@123#"


# ============================================================
# ADMIN LOGIN REQUIRED DECORATOR
# ============================================================
def admin_required(view_function):
    """
    Protect admin-only routes.
    """

    @wraps(view_function)
    def wrapper(*args, **kwargs):

        # Check whether the user has an active login session.
        if not session.get("logged_in"):
            return redirect(
                url_for("auth.login")
            )

        # Check whether the logged-in user is an administrator.
        if session.get("role") != "admin":
            session.clear()

            return redirect(
                url_for("auth.login")
            )

        return view_function(
            *args,
            **kwargs
        )

    return wrapper


# ============================================================
# NO-CACHE RESPONSE HELPER
# ============================================================
def disable_cache(response):
    """
    Prevent browsers from caching authentication pages.
    """

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, "
        "max-age=0, post-check=0, pre-check=0"
    )

    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


# ============================================================
# ADMIN LOGIN
# ============================================================
@auth.route(
    "/login.html",
    methods=["GET", "POST"]
)
def login():

    # --------------------------------------------------------
    # Already Logged In
    # --------------------------------------------------------
    if (
        session.get("logged_in")
        and session.get("role") == "admin"
    ):
        return redirect(
            url_for("website.dashboard")
        )

    # --------------------------------------------------------
    # LOGIN REQUEST
    # --------------------------------------------------------
    if request.method == "POST":

        # Read form values safely.
        username = request.form.get(
            "user_name",
            ""
        ).strip()

        email = request.form.get(
            "user_email",
            ""
        ).strip()

        password = request.form.get(
            "user_password",
            ""
        ).strip()

        # ----------------------------------------------------
        # VERIFY ADMIN CREDENTIALS
        # IMPORTANT:
        # Username, email and password are unchanged.
        # ----------------------------------------------------
        if (
            username == ADMIN_USERNAME
            and email == ADMIN_EMAIL
            and password == ADMIN_PASSWORD
        ):

            # Clear any previous session data.
            session.clear()

            # Create a fresh authenticated session.
            session["admin"] = ADMIN_USERNAME
            session["role"] = "admin"
            session["logged_in"] = True

            # Make the session permanent only if configured
            # by the application.
            session.permanent = False

            response = redirect(
                url_for("website.dashboard")
            )

            # Prevent cached login responses.
            return disable_cache(
                response
            )

        # ----------------------------------------------------
        # INVALID LOGIN
        # ----------------------------------------------------
        response = make_response(
            render_template(
                "login/login.html",
                error="Invalid Username, Email or Password",
            )
        )

        return disable_cache(
            response
        )

    # --------------------------------------------------------
    # LOGIN PAGE
    # --------------------------------------------------------
    response = make_response(
        render_template(
            "login/login.html"
        )
    )

    return disable_cache(
        response
    )


# ============================================================
# LOGOUT
# ============================================================
@auth.route("/logout")
def logout():

    # Completely remove the current session.
    session.clear()

    # Redirect to the existing login URL.
    response = redirect(
        url_for("auth.login")
    )

    # Prevent browser back-button access to cached pages.
    return disable_cache(
        response
    )
