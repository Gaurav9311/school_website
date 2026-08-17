from flask import Blueprint, render_template, request, redirect, send_from_directory, abort,Response,flash
career = Blueprint("career",__name__)
import io
import csv
from database import conn

@career.route("/career-inquiry.html")
def marks():


    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page


    cursor = conn.cursor()
    cursor.execute("SELECT * FROM career_inquiry LIMIT %s OFFSET %s", (per_page, offset))
    sen_car = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM career_inquiry")
    row = cursor.fetchone()
    total = row[0] if row else 0

    cursor.close()

    total_pages = (total + per_page - 1) // per_page
    return render_template("login/career-inquiry.html",
                           careers = sen_car,
                           counts = row,
                           page = page,
                           per_page = per_page,
                           total_pages = total_pages)

@career.route("/add_career.html", methods=["POST"])
def career_get():
    cursor = conn.cursor()

    full_name = request.form["name"]
    email = request.form["email"]
    mobile_number = request.form["phone"]
    applying_for = request.form["message"]
    address = request.form["address"]

    sql = """ INSERT INTO career_inquiry (full_name, email, mobile_number, applying_for, address) VALUES (%s, %s, %s, %s, %s) """
    cursor.execute(sql, (full_name, email, mobile_number, applying_for, address))
    conn.commit()
    cursor.close()
    flash("Your career inquiry has been submitted successfully!", "success")
    return redirect("/career.html")

@career.route("/delete_career_inquiry/<int:id>")
def delete_career_inquiry(id):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM career_inquiry WHERE id = %s", (id,))
    conn.commit()

    cursor.close()

    return redirect("/career-inquiry.html")
