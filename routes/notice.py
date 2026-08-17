from flask import Blueprint, render_template, request, redirect, url_for
from database import conn

notice_bp = Blueprint("notice_bp", __name__)

# 1. Admin Notice Management Page
@notice_bp.route("/admin-notices.html", methods=["GET"])
def admin_notices():
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, date_posted FROM notices ORDER BY id DESC")
    notices = cursor.fetchall()
    cursor.close()
    return render_template("login/admin-notices.html", notices=notices)


# 2. Save Notice Route (Admin Panel se post hoga)
@notice_bp.route("/admin/notices/add", methods=["POST"])
def add_notice():
    title = request.form.get("title")
    content = request.form.get("content")

    if title and content:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notices (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        cursor.close()
        
    return redirect(url_for("notice_bp.admin_notices"))


# 3. Delete Notice Route
@notice_bp.route("/admin/notices/delete/<int:id>", methods=["GET"])
def delete_notice(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notices WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for("notice_bp.admin_notices"))

# 4. Public Notice Page Route
@notice_bp.route("/notice.html")
def public_notices():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notices")
    total_result = cursor.fetchone()
    total = total_result[0] if total_result else 0

    cursor.execute(
        "SELECT id, title, content, date_posted FROM notices ORDER BY id DESC LIMIT %s OFFSET %s",
        (per_page, offset),
    )
    notices = cursor.fetchall()
    cursor.close()

    total_pages = (total + per_page - 1) // per_page if total else 1
    return render_template(
        "academics/notice.html",
        notices=notices,
        page=page,
        total_pages=total_pages,
        totals=total,
    )