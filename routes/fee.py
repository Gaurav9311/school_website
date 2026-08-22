from flask import Blueprint, render_template, request, redirect, Response, flash
import io
import csv
from datetime import datetime
import pymysql.cursors
from database import conn

fees = Blueprint("fees", __name__)

@fees.route("/fee.html")
def fee():
    return redirect("/search_fee")

# PyMySQL Dictionary Cursor Helper
def get_dict_cursor():
    return conn.cursor(pymysql.cursors.DictCursor)

# Filter Query Builder
def build_fee_filter_query(classes, month, section, query_text):
    sql = "FROM fee_management WHERE 1=1"
    values = []

    if classes and classes.strip():
        sql += " AND TRIM(class) = %s"
        values.append(classes.strip())

    if month and month.strip():
        sql += " AND TRIM(fee_month) = %s"
        values.append(month.strip())

    if section and section.strip():
        sql += " AND TRIM(section) = %s"
        values.append(section.strip())

    if query_text and query_text.strip():
        q = f"%{query_text.strip()}%"
        sql += " AND (student_id LIKE %s OR name LIKE %s)"
        values.extend([q, q])

    return sql, values

# ===================================
# SEARCH & FILTER FEE
# ===================================
@fees.route("/search_fee", methods=["GET"])
def search():
    cursor = get_dict_cursor()
    
    submitted = request.args.get("submitted", "").strip()
    query = request.args.get("query", "").strip()
    classes = request.args.get("classes", "").strip()
    month = request.args.get("month", "").strip()
    section = request.args.get("section", "").strip()
    page = request.args.get("page", 1, type=int)

    per_page = 10
    offset = (page - 1) * per_page

    fee_student = []
    total = 0
    paid_count = 0
    total_collection = 0
    pending_fee = 0
    total_pages = 1

    try:
        if submitted == "true":
            base_sql, values = build_fee_filter_query(classes, month, section, query)

            # 1. Total Count Query
            count_sql = "SELECT COUNT(*) AS count " + base_sql
            cursor.execute(count_sql, tuple(values))
            row = cursor.fetchone()
            total = row["count"] if row and row.get("count") else 0
            total_pages = max(1, (total + per_page - 1) // per_page)

            # 2. Filtered Main Data
            main_sql = "SELECT * " + base_sql + " ORDER BY id DESC LIMIT %s OFFSET %s"
            cursor.execute(main_sql, tuple(values) + (per_page, offset))
            fee_student = cursor.fetchall()

            # 3. Filtered Statistics
            stats_sql = f"""
                SELECT 
                    COUNT(CASE WHEN status='Paid' THEN 1 END) as paid_count,
                    COALESCE(SUM(paid_amount), 0) as total_collection,
                    COALESCE(SUM(balance), 0) as pending_fee
                {base_sql}
            """
            cursor.execute(stats_sql, tuple(values))
            stats = cursor.fetchone()

            if stats:
                paid_count = stats.get("paid_count") or 0
                total_collection = stats.get("total_collection") or 0
                pending_fee = stats.get("pending_fee") or 0
    finally:
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
        section=section
    )

# ==========================
# UPDATE FEE
# ==========================
@fees.route("/update_fees/<record_id>", methods=["POST"])
def fee_update_history(record_id):
    cursor = get_dict_cursor()

    try:
        cursor.execute("SELECT * FROM fee_management WHERE id=%s", (record_id,))
        row = cursor.fetchone()

        if not row:
            flash("Student record not found!", "danger")
            return redirect("/search_fee?submitted=true")

        raw_date = request.form.get("payment_date", "").strip()
        payment_mode = request.form.get("payment_mode", "").strip()
        paid_amount_raw = request.form.get("paid_amount", "0").strip()
        fee_month = request.form.get("fee_month", "").strip()
        section = request.form.get("section", "").strip()

        try:
            paid_amount = float(paid_amount_raw)
            if paid_amount < 0:
                raise ValueError
        except ValueError:
            flash("Invalid paid amount specified!", "danger")
            return redirect(request.referrer or "/search_fee?submitted=true")

        total_fee = float(row.get("total_amount") or row.get("total_fee") or 0.0)
        existing_paid = float(row.get("paid_amount") or 0.0)

        if (existing_paid + paid_amount) > total_fee:
            flash(f"Error: Paid amount (₹{existing_paid + paid_amount}) cannot exceed Total Fee (₹{total_fee})!", "danger")
            return redirect(request.referrer or "/search_fee?submitted=true")

        payment_date = raw_date
        if raw_date:
            try:
                payment_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                pass

        total_paid = existing_paid + paid_amount
        new_balance = max(0.0, total_fee - total_paid)
        status = "Paid" if new_balance == 0 else "Pending"

        cursor.execute("""
            UPDATE fee_management 
            SET paid_amount=%s, fee_month=%s, section=%s, balance=%s, payment_date=%s, payment_mode=%s, status=%s 
            WHERE id=%s 
        """, (total_paid, fee_month, section, new_balance, payment_date, payment_mode, status, record_id))

        conn.commit()
        flash("Fee Record Updated Successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"An error occurred: {str(e)}", "danger")
    finally:
        cursor.close()

    return redirect(request.referrer or "/search_fee?submitted=true")

# ==========================
# ADD NEW FEE
# ==========================
@fees.route("/add_fee.html")
def add():
    return render_template("login/fee_management/add_fee.html")

@fees.route("/add_fee", methods=["POST"])
def add_fee():
    cursor = conn.cursor()

    try:
        student_id = request.form.get("student_id", "").strip()
        student_name = request.form.get("student_name", "").strip()
        classes = request.form.get("class", "").strip()
        section = request.form.get("section", "").strip()
        fee_month = request.form.get("fee_month", "").strip()
        total_fee = float(request.form.get("total_fee", 0))
        paid_amount = float(request.form.get("paid_amount", 0))
        payment_date = request.form.get("payment_date", "").strip()
        payment_mode = request.form.get("payment_mode", "").strip()

        if total_fee <= 0 or paid_amount < 0:
            flash("Error: Please enter valid positive fee amounts!", "danger")
            return redirect("/add_fee.html")

        if paid_amount > total_fee:
            flash(f"Error: Paid amount (₹{paid_amount}) cannot be greater than Total Fee (₹{total_fee})!", "danger")
            return redirect("/add_fee.html")

        balance = total_fee - paid_amount
        status = "Paid" if balance == 0 else "Pending"

        cursor.execute(
            """INSERT INTO fee_management
               (student_id, name, class, section, fee_month, total_amount, paid_amount, balance, payment_date, payment_mode, status) 
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (student_id, student_name, classes, section, fee_month, total_fee, paid_amount, balance, payment_date, payment_mode, status)
        )

        conn.commit()
        flash("Fee Added Successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error saving record: {str(e)}", "danger")
    finally:
        cursor.close()

    return redirect("/search_fee?submitted=true")

# ================================
# EXPORT CSV FILE
# ================================
@fees.route("/export_fee_management")
def export_fee_management():
    cursor = get_dict_cursor()
    
    try:
        query = request.args.get("query", "").strip()
        classes = request.args.get("classes", "").strip()
        month = request.args.get("month", "").strip()
        section = request.args.get("section", "").strip()

        base_sql, values = build_fee_filter_query(classes, month, section, query)
        main_sql = "SELECT * " + base_sql

        cursor.execute(main_sql, tuple(values))
        data = cursor.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["ID", "Student ID", "Name", "Class", "Section", "Fee Month", "Total Fee", "Paid Amount", "Balance", "Payment Date", "Payment Mode", "Status"])
        for row in data:
            writer.writerow([
                row.get("id"), row.get("student_id"), row.get("name") or row.get("student_name"), row.get("class"),
                row.get("section"), row.get("fee_month"), row.get("total_amount") or row.get("total_fee"), row.get("paid_amount"),
                row.get("balance"), row.get("payment_date"), row.get("payment_mode"), row.get("status")
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=FEE_MANAGEMENT.csv"}
        )
    finally:
        cursor.close()