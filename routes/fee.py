
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    Response,
    flash,
)

import io
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation

import pymysql.cursors

from database import conn


# ============================================================
# FEE MANAGEMENT BLUEPRINT
# ============================================================
fees = Blueprint("fees", __name__)


# ============================================================
# CONFIGURATION
# ============================================================
PER_PAGE = 10


# ============================================================
# FEE MANAGEMENT HOME
# ============================================================
@fees.route("/fee.html")
def fee():

    # Keep the existing redirect URL unchanged.
    return redirect("/search_fee")


# ============================================================
# DICTIONARY CURSOR HELPER
# ============================================================
def get_dict_cursor():
    """
    Return a PyMySQL dictionary cursor.
    """

    return conn.cursor(
        pymysql.cursors.DictCursor
    )


# ============================================================
# DECIMAL CONVERSION HELPER
# ============================================================
def parse_amount(value, default=None):
    """
    Safely convert an amount into Decimal.
    """

    value = str(value or "").strip()

    if not value:
        return default

    try:
        amount = Decimal(value)

        # Reject NaN and Infinity values.
        if not amount.is_finite():
            return default

        return amount

    except (InvalidOperation, ValueError, TypeError):
        return default


# ============================================================
# FILTER QUERY BUILDER
# ============================================================
def build_fee_filter_query(
    classes,
    month,
    section,
    query_text
):
    """
    Build a parameterized SQL filter query.
    """

    sql = """
        FROM fee_management
        WHERE 1 = 1
    """

    values = []

    # Filter by class.
    classes = str(classes or "").strip()

    if classes:
        sql += """
            AND TRIM(class) = %s
        """
        values.append(classes)

    # Filter by fee month.
    month = str(month or "").strip()

    if month:
        sql += """
            AND TRIM(fee_month) = %s
        """
        values.append(month)

    # Filter by section.
    section = str(section or "").strip()

    if section:
        sql += """
            AND TRIM(section) = %s
        """
        values.append(section)

    # Search by student ID or student name.
    query_text = str(query_text or "").strip()

    if query_text:
        search_value = f"%{query_text}%"

        sql += """
            AND (
                student_id LIKE %s
                OR name LIKE %s
            )
        """

        values.extend([
            search_value,
            search_value,
        ])

    return sql, values


# ============================================================
# SEARCH / FILTER / PAGINATION
# ============================================================
@fees.route("/search_fee", methods=["GET"])
def search():

    cursor = None

    # Read filter parameters safely.
    submitted = request.args.get(
        "submitted",
        ""
    ).strip()

    query = request.args.get(
        "query",
        ""
    ).strip()

    classes = request.args.get(
        "classes",
        ""
    ).strip()

    month = request.args.get(
        "month",
        ""
    ).strip()

    section = request.args.get(
        "section",
        ""
    ).strip()

    # Safely parse page number.
    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    fee_student = []

    total = 0
    paid_count = 0
    total_collection = Decimal("0.00")
    pending_fee = Decimal("0.00")
    total_pages = 1

    try:

        if submitted == "true":

            # Build the parameterized filter query.
            base_sql, values = build_fee_filter_query(
                classes,
                month,
                section,
                query
            )

            # ------------------------------------------------
            # COUNT FILTERED RECORDS
            # ------------------------------------------------
            count_sql = (
                "SELECT COUNT(*) AS count "
                + base_sql
            )

            cursor = get_dict_cursor()

            cursor.execute(
                count_sql,
                tuple(values)
            )

            row = cursor.fetchone()

            total = (
                int(row["count"])
                if row and row.get("count") is not None
                else 0
            )

            total_pages = max(
                1,
                (total + PER_PAGE - 1)
                // PER_PAGE
            )

            # Prevent invalid page numbers.
            if page > total_pages:
                page = total_pages

            offset = (
                page - 1
            ) * PER_PAGE

            # ------------------------------------------------
            # FETCH FILTERED FEE RECORDS
            # ------------------------------------------------
            main_sql = (
                "SELECT * "
                + base_sql
                + """
                    ORDER BY id DESC
                    LIMIT %s OFFSET %s
                """
            )

            cursor.execute(
                main_sql,
                tuple(values)
                + (
                    PER_PAGE,
                    offset,
                )
            )

            fee_student = cursor.fetchall()

            # ------------------------------------------------
            # FILTERED FEE STATISTICS
            # ------------------------------------------------
            stats_sql = f"""
                SELECT
                    COUNT(
                        CASE
                            WHEN status = 'Paid'
                            THEN 1
                        END
                    ) AS paid_count,

                    COALESCE(
                        SUM(paid_amount),
                        0
                    ) AS total_collection,

                    COALESCE(
                        SUM(balance),
                        0
                    ) AS pending_fee

                {base_sql}
            """

            cursor.execute(
                stats_sql,
                tuple(values)
            )

            stats = cursor.fetchone()

            if stats:

                paid_count = (
                    int(
                        stats.get(
                            "paid_count"
                        ) or 0
                    )
                )

                total_collection = (
                    stats.get(
                        "total_collection"
                    )
                    or Decimal("0.00")
                )

                pending_fee = (
                    stats.get(
                        "pending_fee"
                    )
                    or Decimal("0.00")
                )

    except Exception:

        # Roll back the connection if a database
        # operation fails.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to load fee records. Please try again.",
            "danger"
        )

        fee_student = []

    finally:

        # Always close the database cursor.
        if cursor:
            cursor.close()

    return render_template(
        "login/fee_management/fee.html",
        fees=fee_student,
        submitted=submitted,
        page=page,
        total_pages=total_pages,
        fee_count=total,
        paid_count=paid_count,
        total_collection=total_collection,
        pending_fee=pending_fee,
        query=query,
        classes=classes,
        month=month,
        section=section,
    )


# ============================================================
# UPDATE FEE RECORD
# ============================================================
@fees.route(
    "/update_fees/<record_id>",
    methods=["POST"]
)
def fee_update_history(record_id):

    cursor = None

    try:

        # Validate the record ID.
        try:
            record_id = int(record_id)
        except (ValueError, TypeError):

            flash(
                "Invalid fee record ID!",
                "danger"
            )

            return redirect(
                "/search_fee?submitted=true"
            )

        if record_id <= 0:

            flash(
                "Invalid fee record ID!",
                "danger"
            )

            return redirect(
                "/search_fee?submitted=true"
            )

        cursor = get_dict_cursor()

        # ------------------------------------------------
        # CHECK EXISTING RECORD
        # ------------------------------------------------
        cursor.execute(
            """
            SELECT *
            FROM fee_management
            WHERE id = %s
            """,
            (record_id,)
        )

        row = cursor.fetchone()

        if not row:

            flash(
                "Fee record not found!",
                "danger"
            )

            return redirect(
                "/search_fee?submitted=true"
            )

        # ------------------------------------------------
        # READ FORM DATA
        # ------------------------------------------------
        raw_date = request.form.get(
            "payment_date",
            ""
        ).strip()

        payment_mode = request.form.get(
            "payment_mode",
            ""
        ).strip()

        paid_amount_raw = request.form.get(
            "paid_amount",
            "0"
        ).strip()

        fee_month = request.form.get(
            "fee_month",
            ""
        ).strip()

        section = request.form.get(
            "section",
            ""
        ).strip()

        # ------------------------------------------------
        # VALIDATE PAYMENT AMOUNT
        # ------------------------------------------------
        paid_amount = parse_amount(
            paid_amount_raw
        )

        if paid_amount is None:

            flash(
                "Invalid paid amount specified!",
                "danger"
            )

            return redirect(
                request.referrer
                or "/search_fee?submitted=true"
            )

        if paid_amount < 0:

            flash(
                "Paid amount cannot be negative!",
                "danger"
            )

            return redirect(
                request.referrer
                or "/search_fee?submitted=true"
            )

        # ------------------------------------------------
        # GET CURRENT FEE VALUES
        # ------------------------------------------------
        total_fee = parse_amount(
            row.get("total_amount")
            if row.get("total_amount") is not None
            else row.get("total_fee"),
            Decimal("0.00")
        )

        existing_paid = parse_amount(
            row.get("paid_amount"),
            Decimal("0.00")
        )

        # ------------------------------------------------
        # VALIDATE TOTAL PAYMENT
        # ------------------------------------------------
        total_paid = (
            existing_paid
            + paid_amount
        )

        if total_paid > total_fee:

            flash(
                (
                    f"Error: Paid amount "
                    f"(₹{total_paid:.2f}) cannot exceed "
                    f"Total Fee (₹{total_fee:.2f})!"
                ),
                "danger"
            )

            return redirect(
                request.referrer
                or "/search_fee?submitted=true"
            )

        # ------------------------------------------------
        # VALIDATE PAYMENT DATE
        # ------------------------------------------------
        payment_date = raw_date

        if raw_date:

            try:

                payment_date = (
                    datetime.strptime(
                        raw_date,
                        "%Y-%m-%d"
                    ).strftime("%Y-%m-%d")
                )

            except ValueError:

                flash(
                    "Invalid payment date!",
                    "danger"
                )

                return redirect(
                    request.referrer
                    or "/search_fee?submitted=true"
                )

        # ------------------------------------------------
        # CALCULATE BALANCE AND STATUS
        # ------------------------------------------------
        new_balance = (
            total_fee
            - total_paid
        )

        if new_balance < 0:
            new_balance = Decimal("0.00")

        status = (
            "Paid"
            if new_balance == Decimal("0.00")
            else "Pending"
        )

        # ------------------------------------------------
        # UPDATE DATABASE
        # ------------------------------------------------
        cursor.execute(
            """
            UPDATE fee_management
            SET
                paid_amount = %s,
                fee_month = %s,
                section = %s,
                balance = %s,
                payment_date = %s,
                payment_mode = %s,
                status = %s
            WHERE id = %s
            """,
            (
                total_paid,
                fee_month,
                section,
                new_balance,
                payment_date,
                payment_mode,
                status,
                record_id,
            )
        )

        conn.commit()

        flash(
            "Fee record updated successfully!",
            "success"
        )

    except Exception:

        # Roll back any failed transaction.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to update the fee record. Please try again.",
            "danger"
        )

    finally:

        if cursor:
            cursor.close()

    return redirect(
        request.referrer
        or "/search_fee?submitted=true"
    )


# ============================================================
# ADD FEE PAGE
# ============================================================
@fees.route("/add_fee.html")
def add():

    return render_template(
        "login/fee_management/add_fee.html"
    )


# ============================================================
# ADD NEW FEE
# ============================================================
@fees.route("/add_fee", methods=["POST"])
def add_fee():

    cursor = None

    try:

        # ------------------------------------------------
        # READ FORM DATA
        # ------------------------------------------------
        student_id = request.form.get(
            "student_id",
            ""
        ).strip()

        student_name = request.form.get(
            "student_name",
            ""
        ).strip()

        classes = request.form.get(
            "class",
            ""
        ).strip()

        section = request.form.get(
            "section",
            ""
        ).strip()

        fee_month = request.form.get(
            "fee_month",
            ""
        ).strip()

        payment_date = request.form.get(
            "payment_date",
            ""
        ).strip()

        payment_mode = request.form.get(
            "payment_mode",
            ""
        ).strip()

        # ------------------------------------------------
        # VALIDATE REQUIRED FIELDS
        # ------------------------------------------------
        if not student_id:

            flash(
                "Student ID is required!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        if not student_name:

            flash(
                "Student name is required!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        if not classes:

            flash(
                "Class is required!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        if not section:

            flash(
                "Section is required!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        if not fee_month:

            flash(
                "Fee month is required!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        # ------------------------------------------------
        # PARSE FEE AMOUNTS
        # ------------------------------------------------
        total_fee = parse_amount(
            request.form.get(
                "total_fee",
                "0"
            )
        )

        paid_amount = parse_amount(
            request.form.get(
                "paid_amount",
                "0"
            ),
            Decimal("0.00")
        )

        if total_fee is None:

            flash(
                "Please enter a valid total fee!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        if paid_amount is None:

            flash(
                "Please enter a valid paid amount!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        # ------------------------------------------------
        # AMOUNT VALIDATION
        # ------------------------------------------------
        if total_fee <= 0:

            flash(
                "Total fee must be greater than zero!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        if paid_amount < 0:

            flash(
                "Paid amount cannot be negative!",
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        if paid_amount > total_fee:

            flash(
                (
                    f"Error: Paid amount "
                    f"(₹{paid_amount:.2f}) cannot be "
                    f"greater than Total Fee "
                    f"(₹{total_fee:.2f})!"
                ),
                "danger"
            )

            return redirect(
                "/add_fee.html"
            )

        # ------------------------------------------------
        # VALIDATE PAYMENT DATE
        # ------------------------------------------------
        if payment_date:

            try:

                payment_date = (
                    datetime.strptime(
                        payment_date,
                        "%Y-%m-%d"
                    ).strftime("%Y-%m-%d")
                )

            except ValueError:

                flash(
                    "Invalid payment date!",
                    "danger"
                )

                return redirect(
                    "/add_fee.html"
                )

        # ------------------------------------------------
        # CALCULATE BALANCE
        # ------------------------------------------------
        balance = (
            total_fee
            - paid_amount
        )

        status = (
            "Paid"
            if balance == Decimal("0.00")
            else "Pending"
        )

        # ------------------------------------------------
        # INSERT FEE RECORD
        # ------------------------------------------------
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO fee_management
            (
                student_id,
                name,
                class,
                section,
                fee_month,
                total_amount,
                paid_amount,
                balance,
                payment_date,
                payment_mode,
                status
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
            """,
            (
                student_id,
                student_name,
                classes,
                section,
                fee_month,
                total_fee,
                paid_amount,
                balance,
                payment_date,
                payment_mode,
                status,
            )
        )

        conn.commit()

        flash(
            "Fee added successfully!",
            "success"
        )

    except Exception:

        # Roll back failed database operations.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to save the fee record. Please try again.",
            "danger"
        )

    finally:

        # Always close the database cursor.
        if cursor:
            cursor.close()

    return redirect(
        "/search_fee?submitted=true"
    )


# ============================================================
# EXPORT FEE DATA TO CSV
# ============================================================
@fees.route("/export_fee_management")
def export_fee_management():

    cursor = None

    try:

        # Read current filters.
        query = request.args.get(
            "query",
            ""
        ).strip()

        classes = request.args.get(
            "classes",
            ""
        ).strip()

        month = request.args.get(
            "month",
            ""
        ).strip()

        section = request.args.get(
            "section",
            ""
        ).strip()

        # Build the same filtered query used by search.
        base_sql, values = build_fee_filter_query(
            classes,
            month,
            section,
            query
        )

        main_sql = (
            "SELECT * "
            + base_sql
            + " ORDER BY id DESC"
        )

        cursor = get_dict_cursor()

        cursor.execute(
            main_sql,
            tuple(values)
        )

        data = cursor.fetchall()

        # ------------------------------------------------
        # CREATE CSV IN MEMORY
        # ------------------------------------------------
        output = io.StringIO(
            newline=""
        )

        writer = csv.writer(
            output
        )

        writer.writerow([
            "ID",
            "Student ID",
            "Name",
            "Class",
            "Section",
            "Fee Month",
            "Total Fee",
            "Paid Amount",
            "Balance",
            "Payment Date",
            "Payment Mode",
            "Status",
        ])

        for row in data:

            writer.writerow([
                row.get("id"),

                row.get("student_id"),

                (
                    row.get("name")
                    or row.get("student_name")
                    or ""
                ),

                row.get("class"),

                row.get("section"),

                row.get("fee_month"),

                (
                    row.get("total_amount")
                    or row.get("total_fee")
                    or 0
                ),

                row.get(
                    "paid_amount"
                ) or 0,

                row.get(
                    "balance"
                ) or 0,

                row.get(
                    "payment_date"
                ),

                row.get(
                    "payment_mode"
                ),

                row.get(
                    "status"
                ),
            ])

        output.seek(0)

        # Return CSV as a downloadable file.
        return Response(
            output.getvalue(),
            mimetype="text/csv; charset=utf-8",
            headers={
                "Content-Disposition":
                    "attachment; "
                    "filename=FEE_MANAGEMENT.csv"
            },
        )

    except Exception:

        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to export fee data. Please try again.",
            "danger"
        )

        return redirect(
            "/search_fee?submitted=true"
        )

    finally:

        if cursor:
            cursor.close()
