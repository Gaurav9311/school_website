
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from database import conn


# ============================================================
# NOTICE BLUEPRINT
# ============================================================
notice_bp = Blueprint("notice_bp", __name__)


# ============================================================
# CONFIGURATION
# ============================================================
PER_PAGE = 10


# ============================================================
# ADMIN NOTICE MANAGEMENT PAGE
# ============================================================
@notice_bp.route("/admin-notices.html", methods=["GET"])
def admin_notices():

    cursor = None

    try:
        cursor = conn.cursor()

        # Fetch all notices with the newest notice first.
        cursor.execute(
            """
            SELECT id, title, content, date_posted
            FROM notices
            ORDER BY id DESC
            """
        )

        notices = cursor.fetchall()

        return render_template(
            "login/admin-notices.html",
            notices=notices,
        )

    except Exception:
        # Roll back the transaction if a database error occurs.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to load notices. Please try again.",
            "danger",
        )

        return render_template(
            "login/admin-notices.html",
            notices=[],
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()


# ============================================================
# ADD NOTICE
# ============================================================
@notice_bp.route("/admin/notices/add", methods=["POST"])
def add_notice():

    # Safely read form data.
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    # --------------------------------------------------------
    # Validate Required Fields
    # --------------------------------------------------------
    if not title:
        flash(
            "Notice title is required.",
            "danger",
        )
        return redirect(url_for("notice_bp.admin_notices"))

    if not content:
        flash(
            "Notice content is required.",
            "danger",
        )
        return redirect(url_for("notice_bp.admin_notices"))

    # Prevent unnecessarily large input.
    if len(title) > 255:
        flash(
            "Notice title is too long.",
            "danger",
        )
        return redirect(url_for("notice_bp.admin_notices"))

    cursor = None

    try:
        cursor = conn.cursor()

        # Use a parameterized query to prevent SQL injection.
        cursor.execute(
            """
            INSERT INTO notices
            (
                title,
                content
            )
            VALUES (%s, %s)
            """,
            (
                title,
                content,
            ),
        )

        # Save the new notice.
        conn.commit()

        flash(
            "Notice added successfully.",
            "success",
        )

    except Exception:
        # Roll back the transaction if insertion fails.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to add the notice. Please try again.",
            "danger",
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()

    # Keep the existing redirect unchanged.
    return redirect(url_for("notice_bp.admin_notices"))


# ============================================================
# DELETE NOTICE
# ============================================================
@notice_bp.route(
    "/admin/notices/delete/<int:id>",
    methods=["GET"],
)
def delete_notice(id):

    # Reject invalid IDs.
    if id <= 0:
        flash(
            "Invalid notice ID.",
            "danger",
        )
        return redirect(url_for("notice_bp.admin_notices"))

    cursor = None

    try:
        cursor = conn.cursor()

        # Check whether the notice exists.
        cursor.execute(
            """
            SELECT id
            FROM notices
            WHERE id = %s
            """,
            (id,),
        )

        notice = cursor.fetchone()

        if not notice:
            flash(
                "Notice not found.",
                "warning",
            )
            return redirect(url_for("notice_bp.admin_notices"))

        # Delete the selected notice.
        cursor.execute(
            """
            DELETE FROM notices
            WHERE id = %s
            """,
            (id,),
        )

        # Save the deletion.
        conn.commit()

        flash(
            "Notice deleted successfully.",
            "success",
        )

    except Exception:
        # Roll back the transaction if deletion fails.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to delete the notice. Please try again.",
            "danger",
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()

    # Keep the existing redirect unchanged.
    return redirect(url_for("notice_bp.admin_notices"))


# ============================================================
# PUBLIC NOTICE PAGE
# ============================================================
@notice_bp.route("/notice.html")
def public_notices():

    # Get the requested page number.
    page = request.args.get(
        "page",
        1,
        type=int,
    )

    # Prevent invalid page numbers.
    if page < 1:
        page = 1

    offset = (page - 1) * PER_PAGE

    cursor = None

    try:
        cursor = conn.cursor()

        # Get the total number of notices.
        cursor.execute(
            "SELECT COUNT(*) FROM notices"
        )

        total_result = cursor.fetchone()
        total = (
            total_result[0]
            if total_result
            else 0
        )

        # Calculate total pages.
        total_pages = max(
            1,
            (total + PER_PAGE - 1) // PER_PAGE
        )

        # Prevent accessing a page beyond the available range.
        if page > total_pages:
            page = total_pages
            offset = (page - 1) * PER_PAGE

        # Fetch notices for the current page.
        cursor.execute(
            """
            SELECT id, title, content, date_posted
            FROM notices
            ORDER BY id DESC
            LIMIT %s OFFSET %s
            """,
            (
                PER_PAGE,
                offset,
            ),
        )

        notices = cursor.fetchall()

        return render_template(
            "academics/notice.html",
            notices=notices,
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
            "Unable to load notices. Please try again.",
            "danger",
        )

        return render_template(
            "academics/notice.html",
            notices=[],
            page=1,
            total_pages=1,
            totals=0,
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()
