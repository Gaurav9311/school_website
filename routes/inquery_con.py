
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
)

import re
from database import conn


# ============================================================
# INQUIRY CONTACTS BLUEPRINT
# ============================================================
inquiry_contacts = Blueprint("inquiry_contacts", __name__)


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
# INQUIRY CONTACTS PAGE
# ============================================================
@inquiry_contacts.route("/inquiry_contacts.html")
def inquiry_contacts_page():

    # Get the requested page number.
    page = request.args.get("page", 1, type=int)

    # Prevent invalid page numbers.
    if page < 1:
        page = 1

    offset = (page - 1) * PER_PAGE
    cursor = None

    try:
        cursor = conn.cursor()

        # Fetch inquiries with pagination.
        cursor.execute(
            """
            SELECT *
            FROM inquiries
            ORDER BY id DESC
            LIMIT %s OFFSET %s
            """,
            (PER_PAGE, offset),
        )

        inquiries = cursor.fetchall()

        # Get the total number of inquiries.
        cursor.execute(
            "SELECT COUNT(*) FROM inquiries"
        )

        result = cursor.fetchone()
        total = result[0] if result else 0

        # Calculate total pages.
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
                FROM inquiries
                ORDER BY id DESC
                LIMIT %s OFFSET %s
                """,
                (PER_PAGE, offset),
            )

            inquiries = cursor.fetchall()

        return render_template(
            "login/inquiry_contacts.html",
            inquiries=inquiries,
            page=page,
            total_pages=total_pages,
            totals=total,
        )

    except Exception:
        # Roll back the transaction if a database error occurs.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to load inquiries. Please try again.",
            "danger",
        )

        return render_template(
            "login/inquiry_contacts.html",
            inquiries=[],
            page=1,
            total_pages=1,
            totals=0,
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()


# ============================================================
# CONTACT FORM SUBMISSION
# ============================================================
@inquiry_contacts.route("/contact_form", methods=["POST"])
def contact():

    # Safely read form data.
    full_name = request.form.get("name", "").strip()
    email_address = request.form.get("email", "").strip()
    phone_number = request.form.get("phone", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    # --------------------------------------------------------
    # Required Field Validation
    # --------------------------------------------------------
    if not full_name:
        flash("Full name is required.", "danger")
        return redirect("/contact-us.html")

    if not email_address:
        flash("Email address is required.", "danger")
        return redirect("/contact-us.html")

    if not phone_number:
        flash("Phone number is required.", "danger")
        return redirect("/contact-us.html")

    if not subject:
        flash("Subject is required.", "danger")
        return redirect("/contact-us.html")

    if not message:
        flash("Message is required.", "danger")
        return redirect("/contact-us.html")

    # --------------------------------------------------------
    # Email Validation
    # --------------------------------------------------------
    if not is_valid_email(email_address):
        flash(
            "Please enter a valid email address.",
            "danger",
        )
        return redirect("/contact-us.html")

    # --------------------------------------------------------
    # Phone Number Validation
    # --------------------------------------------------------
    if not phone_number.isdigit() or len(phone_number) != 10:
        flash(
            "Please enter a valid 10-digit phone number.",
            "danger",
        )
        return redirect("/contact-us.html")

    cursor = None

    try:
        cursor = conn.cursor()

        # Use a parameterized query to prevent SQL injection.
        sql = """
            INSERT INTO inquiries
            (
                full_name,
                email_address,
                phone_number,
                subject,
                message
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                full_name,
                email_address,
                phone_number,
                subject,
                message,
            ),
        )

        # Commit the new inquiry to the database.
        conn.commit()

        flash(
            "Message sent successfully!",
            "success",
        )

    except Exception:
        # Roll back the transaction if insertion fails.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to send your message. Please try again.",
            "danger",
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()

    # Keep the existing redirect URL unchanged.
    return redirect("/contact-us.html")


# ============================================================
# DELETE INQUIRY
# ============================================================
@inquiry_contacts.route(
    "/delete_inquiry/<int:id>",
    methods=["GET", "POST"],
)
def delete_inquiry(id):

    # Reject invalid IDs.
    if id <= 0:
        flash(
            "Invalid inquiry ID.",
            "danger",
        )
        return redirect("/inquiry_contacts.html")

    cursor = None

    try:
        cursor = conn.cursor()

        # Check whether the inquiry exists.
        cursor.execute(
            """
            SELECT id
            FROM inquiries
            WHERE id = %s
            """,
            (id,),
        )

        inquiry = cursor.fetchone()

        if not inquiry:
            flash(
                "Inquiry not found.",
                "warning",
            )
            return redirect("/inquiry_contacts.html")

        # Delete the selected inquiry.
        cursor.execute(
            """
            DELETE FROM inquiries
            WHERE id = %s
            """,
            (id,),
        )

        # Commit the deletion.
        conn.commit()

        flash(
            "Inquiry deleted successfully!",
            "success",
        )

    except Exception:
        # Roll back the transaction if deletion fails.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to delete the inquiry. Please try again.",
            "danger",
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()

    # Keep the existing redirect URL unchanged.
    return redirect("/inquiry_contacts.html")
