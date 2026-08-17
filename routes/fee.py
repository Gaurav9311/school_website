from flask import Blueprint, render_template, request, redirect, send_from_directory, abort, Response, flash
fees = Blueprint("fees",__name__)
import io
import csv
from database import conn


@fees.route("/fee.html")
def fee():

    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM fee_management LIMIT %s OFFSET %s",
        (per_page, offset)
    )
    fee_student = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM fee_management")
    row = cursor.fetchone()
    total = row[0] if row and row[0] is not None else 0

    cursor.execute(
        "SELECT COUNT(*) FROM fee_management WHERE status='Paid'"
    )
    row = cursor.fetchone()
    paid_count = row[0] if row and row[0] is not None else 0

    cursor.execute(
        "SELECT SUM(paid_amount) FROM fee_management"
    )
    row = cursor.fetchone()
    total_collection = row[0] if row and row[0] is not None else 0

    cursor.execute(
        "SELECT SUM(balance) FROM fee_management"
    )
    row = cursor.fetchone()
    pending_fee = row[0] if row and row[0] is not None else 0

    cursor.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "login/fee_management/fee.html",
        fees=fee_student,
        page=page,
        total_pages=total_pages,
        fee_count=total,
        paid_count=paid_count,
        total_collection=total_collection,
        pending_fee=pending_fee,
        query="",
        classes="",
        month=""
    )


# ==========================
# UPDATE FEE (FIXED)
# ==========================

@fees.route("/update_fees/<record_id>", methods=["POST"])
def fee_update_history(record_id):
    print("Record Table ID:", record_id)
    cursor = conn.cursor()

    student_id = request.form["id_no"]
    name = request.form["name"]
    classes = request.form["classes"]
    fee_month = request.form["fee_month"]
    payment_date = request.form["payment_date"]
    payment_mode = request.form["payment_mode"]

    paid_amount = float(request.form["paid_amount"])

    # 1. Primary Key 'id' se search karo (student_id se nahi)
    cursor.execute("SELECT * FROM fee_management WHERE id=%s", (record_id,))
    row = cursor.fetchone()

    if row is None:
        cursor.close()
        return "Student record not found"

    # 2. Database Structure ke mutabiq Balance (7th Index) pick karo
    # Table Structure: id(0), student_id(1), name(2), class(3), month(4), total(5), paid(6), balance(7)
    current_balance = float(row[7])

    # Dynamic balance recalculation
    new_balance = current_balance - paid_amount
    if new_balance < 0:
        new_balance = 0

    status = "Paid" if new_balance == 0 else "Pending"

    # 3. Existing paid amount me Naya paid amount ADD karo
    total_paid = float(row[6]) + paid_amount

    # Update Table using Primary Key 'id'
    cursor.execute("""
        UPDATE fee_management 
        SET paid_amount=%s, balance=%s, payment_date=%s, payment_mode=%s, status=%s 
        WHERE id=%s 
    """, (total_paid, new_balance, payment_date, payment_mode, status, record_id))

    # # Payment History Audit Record
    # cursor.execute("""
    #     INSERT INTO fee_payment_history
    #     (student_id, student_name, class, fee_month, payment_amount, payment_date, payment_mode)
    #     VALUES (%s, %s, %s, %s, %s, %s, %s)
    # """, (student_id, name, classes, fee_month, paid_amount, payment_date, payment_mode))

    conn.commit()
    cursor.close()

    flash("Fee Record Updated Successfully!", "success")
    return redirect("/fee.html")




# ===================================
# SEARCH FEE
# ===================================
@fees.route("/search_fee")
def search():
    query = request.args.get("query", "").strip()
    classes = request.args.get("classes", "").strip()
    month = request.args.get("month", "").strip()
    page = request.args.get("page", 1, type=int)

    per_page = 10
    offset = (page - 1) * per_page

    cursor = conn.cursor()

    # Build search pattern
    search_pattern = f"%{query}%" if query else "%"
    class_pattern = f"%{classes}%" if classes else "%"
    month_pattern = f"%{month}%" if month else "%"

    # DEBUG: Print patterns
    print(f"Search: '{search_pattern}'")
    print(f"Class: '{class_pattern}'")
    print(f"Month: '{month_pattern}'")

    # Count query
    cursor.execute("""
        SELECT COUNT(*)
        FROM fee_management
        WHERE
        (student_id LIKE %s OR student_name LIKE %s)
        AND class LIKE %s
        AND fee_month LIKE %s
    """, (
        search_pattern,
        search_pattern,
        class_pattern,
        month_pattern
    ))

    row = cursor.fetchone()
    total = row[0] if row is not None else 0

    # Main query
    cursor.execute("""
        SELECT *
        FROM fee_management
        WHERE
        (student_id LIKE %s OR student_name LIKE %s)
        AND class LIKE %s
        AND fee_month LIKE %s
        ORDER BY id DESC
        LIMIT %s OFFSET %s
    """, (
        search_pattern,
        search_pattern,
        class_pattern,
        month_pattern,
        per_page,
        offset
    ))

    fee = cursor.fetchall()

    # Summary statistics (these should also be filtered for accuracy)
    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN status='Paid' THEN 1 END) as paid_count,
            COALESCE(SUM(paid_amount), 0) as total_collection,
            COALESCE(SUM(balance), 0) as pending_fee
        FROM fee_management
        WHERE
        (student_id LIKE %s OR student_name LIKE %s)
        AND class LIKE %s
        AND fee_month LIKE %s
    """, (
        search_pattern,
        search_pattern,
        class_pattern,
        month_pattern
    ))

    stats = cursor.fetchone()
    paid_count = stats[0] if stats else 0
    total_collection = stats[1] if stats else 0
    pending_fee = stats[2] if stats else 0

    cursor.close()

    total_pages = (total + per_page - 1) // per_page if total > 0 else 1

    return render_template(
        "login/fee_management/fee.html",
        fee=fee,
        page=page,
        total_pages=total_pages,
        fee_count=total,
        query=query,
        classes=classes,
        month=month,
        paid_count=paid_count,
        total_collection=total_collection,
        pending_fee=pending_fee
    )
# ==========================
# ADD NEW FEE
# ==========================

@fees.route("/add_fee.html")
def add():
    return render_template("login/fee_management/add_fee.html")
@fees.route("/add_fee",methods=["POST"])
def add_fee():

    cursor = conn.cursor()

    student_id = request.form["student_id"]
    student_name = request.form["student_name"]
    classes = request.form["class"]
    fee_month = request.form["fee_month"]
    total_fee = request.form["total_fee"]
    paid_amount = request.form["paid_amount"]
    payment_date = request.form["payment_date"]
    balance = float(total_fee)-float(paid_amount)
    payment_mode = request.form["payment_mode"]

    if balance ==0:
        status = "Paid"
    else:
        status = "Pending"

    
    cursor.execute("INSERT INTO fee_management(student_id,student_name,class,fee_month,total_fee,paid_amount,balance,payment_date,payment_mode,status)" \
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(student_id,student_name,classes,fee_month,total_fee,paid_amount,balance,payment_date,payment_mode,status))

    conn.commit()
    cursor.close()

    return redirect("/fee.html")

# ================================
# EXPORT CSV FILE FEE MANAGEMENT
# ================================

@fees.route("/export_fee_management")
def export_fee_management():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fee_management")
    data = cursor.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Student Id","Name","Class","Fee Month","Total Fee","Paid Amount","Balance","Payment Date","Payment Mode","Status"])
    writer.writerows(data)

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=FEE MANAGEMENT.csv"}
    )

