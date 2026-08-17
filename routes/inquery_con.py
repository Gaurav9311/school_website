from flask import Blueprint, render_template, request, redirect, send_from_directory, abort, Response, flash
inquiry_contacts = Blueprint("inquiry_contacts",__name__)
import io
import csv
from database import conn

@inquiry_contacts.route("/inquiry_contacts.html")
def inquiry_contacts_page():

    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inquiries LIMIT %s OFFSET %s", (per_page, offset))
    inquiries = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM inquiries")
    result = cursor.fetchone()
    total = result[0] if result else 0
    total_pages = (total + per_page - 1) // per_page

    return render_template("login/inquiry_contacts.html", inquiries=inquiries, page=page, total_pages=total_pages,totals=total)

@inquiry_contacts.route("/contact_form", methods=["POST"])
def contact():
    full_name = request.form.get("name")
    email_address = request.form.get("email")
    phone_number = request.form.get("phone")
    subject = request.form.get("subject")
    message = request.form.get("message")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO inquiries (full_name, email_address, phone_number, subject, message) VALUES (%s, %s, %s, %s, %s)", (full_name, email_address, phone_number, subject, message))
    conn.commit()
    cursor.close()
    flash("Message sent successfully!")
    return redirect("/contact-us.html")

@inquiry_contacts.route("/delete_inquiry/<int:id>", methods=["GET", "POST"])
def delete_inquiry(id):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM inquiries WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    flash("Inquiry deleted successfully!", "success")
    return redirect("/inquiry_contacts.html")
