from flask import Blueprint,render_template,request,redirect,flash
import re
from database import conn


# ============================================================
# CAREER BLUEPRINT
# ============================================================
career = Blueprint("career", __name__)


# ============================================================
# CONFIGURATION
# ============================================================
PER_PAGE = 10


# ============================================================
# EMAIL VALIDATION
# ============================================================
def is_valid_email(email):
    """
    Validate the basic structure of an email address.
    """
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


# ============================================================
# CAREER INQUIRY LIST
# ============================================================
@career.route("/career-inquiry.html")
def marks():

    # Get the requested page number.
    page = request.args.get("page", 1, type=int)

    # Prevent invalid or negative page numbers.
    if page < 1:
        page = 1

    offset = (page - 1) * PER_PAGE

    cursor = None

    try:
        cursor = conn.cursor()

        # Fetch paginated career inquiries.
        cursor.execute(
            """
            SELECT *
            FROM career_inquiry
            ORDER BY id DESC
            LIMIT %s OFFSET %s
            """,
            (PER_PAGE, offset),
        )

        sent_careers = cursor.fetchall()

        # Get the total number of career inquiries.
        cursor.execute(
            "SELECT COUNT(*) FROM career_inquiry"
        )

        row = cursor.fetchone()
        total = row[0] if row else 0

        # Calculate the total number of pages.
        total_pages = max(
            1,
            (total + PER_PAGE - 1) // PER_PAGE
        )

        # Prevent accessing a page beyond the available range.
        if page > total_pages:
            page = total_pages
            offset = (page - 1) * PER_PAGE

            cursor.execute(
                """
                SELECT *
                FROM career_inquiry
                ORDER BY id DESC
                LIMIT %s OFFSET %s
                """,
                (PER_PAGE, offset),
            )

            sent_careers = cursor.fetchall()

        return render_template(
            "login/career-inquiry.html",
            careers=sent_careers,
            counts=row,
            page=page,
            per_page=PER_PAGE,
            total_pages=total_pages,
        )

    except Exception:
        # Roll back the transaction if a database error occurs.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to load career inquiries. Please try again.",
            "danger",
        )

        return render_template(
            "login/career-inquiry.html",
            careers=[],
            counts=(0,),
            page=1,
            per_page=PER_PAGE,
            total_pages=1,
        )

    finally:
        # Always close the cursor.
        if cursor:
            cursor.close()


# ============================================================
# ADD CAREER INQUIRY
# ============================================================
@career.route("/add_career.html", methods=["POST"])
def career_get():

    # Read form values safely.
    full_name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    mobile_number = request.form.get("phone", "").strip()
    applying_for = request.form.get("message", "").strip()
    address = request.form.get("address", "").strip()

    # --------------------------------------------------------
    # Required Field Validation
    # --------------------------------------------------------
    if not full_name:
        flash("Full name is required.", "danger")
        return redirect("/career.html")

    if not email:
        flash("Email address is required.", "danger")
        return redirect("/career.html")

    if not mobile_number:
        flash("Mobile number is required.", "danger")
        return redirect("/career.html")

    if not applying_for:
        flash("Please specify the position you are applying for.", "danger")
        return redirect("/career.html")

    if not address:
        flash("Address is required.", "danger")
        return redirect("/career.html")

    # --------------------------------------------------------
    # Email Validation
    # --------------------------------------------------------
    if not is_valid_email(email):
        flash("Please enter a valid email address.", "danger")
        return redirect("/career.html")

    # --------------------------------------------------------
    # Mobile Number Validation
    # --------------------------------------------------------
    if not mobile_number.isdigit() or len(mobile_number) != 10:
        flash("Please enter a valid 10-digit mobile number.", "danger")
        return redirect("/career.html")

    cursor = None

    try:
        cursor = conn.cursor()

        # Use a parameterized query to prevent SQL injection.
        sql = """
            INSERT INTO career_inquiry
            (
                full_name,
                email,
                mobile_number,
                applying_for,
                address
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                full_name,
                email,
                mobile_number,
                applying_for,
                address,
            ),
        )

        # Save the inquiry permanently.
        conn.commit()

        flash(
            "Your career inquiry has been submitted successfully!",
            "success",
        )

    except Exception:
        # Undo the transaction if something goes wrong.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to submit your career inquiry. Please try again.",
            "danger",
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()

    # Keep the existing redirect URL unchanged.
    return redirect("/career.html")


# ============================================================
# DELETE CAREER INQUIRY
# ============================================================
@career.route("/delete_career_inquiry/<int:id>")
def delete_career_inquiry(id):

    # Reject invalid IDs.
    if id <= 0:
        flash("Invalid career inquiry ID.", "danger")
        return redirect("/career-inquiry.html")

    cursor = None

    try:
        cursor = conn.cursor()

        # Check whether the inquiry exists.
        cursor.execute(
            """
            SELECT id
            FROM career_inquiry
            WHERE id = %s
            """,
            (id,),
        )

        inquiry = cursor.fetchone()

        if not inquiry:
            flash(
                "Career inquiry not found.",
                "warning",
            )

            return redirect("/career-inquiry.html")

        # Delete the selected inquiry.
        cursor.execute(
            """
            DELETE FROM career_inquiry
            WHERE id = %s
            """,
            (id,),
        )

        # Save the deletion.
        conn.commit()

        flash(
            "Career inquiry deleted successfully.",
            "success",
        )

    except Exception:
        # Roll back the transaction if deletion fails.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to delete the career inquiry. Please try again.",
            "danger",
        )

    finally:
        # Always close the cursor.
        if cursor:
            cursor.close()

    # Keep the existing redirect URL unchanged.
    return redirect("/career-inquiry.html")
