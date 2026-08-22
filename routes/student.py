from flask import Blueprint, render_template, request, redirect, Response, flash
import io
import csv
from database import conn

student = Blueprint("student", __name__)

# Helper Function: Convert empty input strings to float or None
def parse_numeric(val):
    if val and val.strip():
        try:
            return float(val.strip())
        except ValueError:
            return None
    return None


@student.route("/view_student.html")
def fetchall_all_student():
    return redirect("/Search_student_management")


@student.route("/add_new_student.html")
def add_new_student():
    return render_template("login/student/add_new_student.html")


@student.route("/add_new_student", methods=["POST"])
def add_new():
    cursor = conn.cursor()
    try:
        academic_session = request.form.get("academic_session", "")
        admission_no = request.form.get("admission_no", "")
        admission_date = request.form.get("admission_date", "")
        student_class = request.form.get("class", "")
        section = request.form.get("section", "")
        roll_no = request.form.get("roll_no", "")

        first_name = request.form.get("first_name", "")
        middle_name = request.form.get("middle_name", "")
        last_name = request.form.get("last_name", "")
        date_of_birth = request.form.get("date_of_birth", "")
        gender = request.form.get("gender", "")
        blood_group = request.form.get("blood_group", "")
        category = request.form.get("category", "")
        religion = request.form.get("religion", "")
        mother_tongue = request.form.get("mother_tongue", "")
        nationality = request.form.get("nationality", "")
        aadhaar_number = request.form.get("aadhaar_number", "")

        father_name = request.form.get("father_name", "")
        father_occupation = request.form.get("father_occupation", "")
        father_phone = request.form.get("father_phone", "")
        mother_name = request.form.get("mother_name", "")
        mother_occupation = request.form.get("mother_occupation", "")
        mother_phone = request.form.get("mother_phone", "")
        email_address = request.form.get("parent_email", "")

        annual_income = parse_numeric(request.form.get("annual_income"))
        emergency_contact = request.form.get("emergency_contact", "")

        current_address = request.form.get("present_address", "")
        current_city = request.form.get("present_city", "")
        current_state = request.form.get("present_state", "")
        current_pincode = request.form.get("present_pincode", "")

        permanent_address = request.form.get("permanent_address", "")
        permanent_city = request.form.get("permanent_city", "")
        permanent_state = request.form.get("permanent_state", "")
        permanent_pincode = request.form.get("permanent_pincode", "")

        previous_school_name = request.form.get("previous_school_name", "")
        previous_class = request.form.get("previous_class", "")
        previous_marks = parse_numeric(request.form.get("previous_marks"))
        tc_number = request.form.get("tc_number", "")

        sql = """
            INSERT INTO student (
                academic_session, admission_no, admission_date, student_class, section, roll_no,
                first_name, middle_name, last_name, date_of_birth, gender, blood_group,
                category, religion, mother_tongue, nationality, aadhaar_number,
                father_name, father_occupation, father_phone, mother_name,
                mother_occupation, mother_phone, email_address, annual_income, emergency_contact,
                current_address, current_city, current_state, current_pincode,
                permanent_address, permanent_city, permanent_state, permanent_pincode,
                previous_school_name, previous_class, previous_marks, tc_number
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            academic_session, admission_no, admission_date, student_class, section, roll_no,
            first_name, middle_name, last_name, date_of_birth, gender, blood_group,
            category, religion, mother_tongue, nationality, aadhaar_number,
            father_name, father_occupation, father_phone, mother_name,
            mother_occupation, mother_phone, email_address, annual_income, emergency_contact,
            current_address, current_city, current_state, current_pincode,
            permanent_address, permanent_city, permanent_state, permanent_pincode,
            previous_school_name, previous_class, previous_marks, tc_number
        )

        cursor.execute(sql, data)
        conn.commit()
        flash("Student added successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error adding student: {str(e)}", "danger")
    finally:
        cursor.close()

    return redirect("/Search_student_management?submitted=true")


@student.route("/delete/<int:id>")
def delete_student(id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM student WHERE student_id = %s", (id,))
        conn.commit()
        flash("Student deleted successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting student: {str(e)}", "danger")
    finally:
        cursor.close()

    if request.referrer and "Search_student_management" in request.referrer:
        return redirect(request.referrer)
    return redirect("/Search_student_management?submitted=true")


@student.route("/edit_student.html/<int:id>")
def edit_student(id):
    cursor = conn.cursor()
    edit = None
    try:
        cursor.execute("SELECT * FROM student WHERE student_id=%s", (id,))
        edit = cursor.fetchone()
    except Exception as e:
        flash(f"Error fetching student details: {str(e)}", "danger")
    finally:
        cursor.close()

    return render_template("login/student/edit_student.html", edit=edit)


@student.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):
    cursor = conn.cursor()
    try:
        academic_session = request.form.get("academic_session", "")
        admission_no = request.form.get("admission_no", "")
        admission_date = request.form.get("admission_date", "")
        student_class = request.form.get("class", "")
        section = request.form.get("section", "")
        roll_no = request.form.get("roll_no", "")

        first_name = request.form.get("first_name", "")
        middle_name = request.form.get("middle_name", "")
        last_name = request.form.get("last_name", "")
        date_of_birth = request.form.get("date_of_birth", "")
        gender = request.form.get("gender", "")
        blood_group = request.form.get("blood_group", "")
        category = request.form.get("category", "")
        religion = request.form.get("religion", "")
        mother_tongue = request.form.get("mother_tongue", "")
        nationality = request.form.get("nationality", "")
        aadhaar_number = request.form.get("aadhaar_number", "")

        father_name = request.form.get("father_name", "")
        father_occupation = request.form.get("father_occupation", "")
        father_phone = request.form.get("father_phone", "")
        mother_name = request.form.get("mother_name", "")
        mother_occupation = request.form.get("mother_occupation", "")
        mother_phone = request.form.get("mother_phone", "")
        email_address = request.form.get("parent_email", "")

        annual_income = parse_numeric(request.form.get("annual_income"))
        emergency_contact = request.form.get("emergency_contact", "")

        current_address = request.form.get("present_address", "")
        current_city = request.form.get("present_city", "")
        current_state = request.form.get("present_state", "")
        current_pincode = request.form.get("present_pincode", "")

        permanent_address = request.form.get("permanent_address", "")
        permanent_city = request.form.get("permanent_city", "")
        permanent_state = request.form.get("permanent_state", "")
        permanent_pincode = request.form.get("permanent_pincode", "")

        previous_school_name = request.form.get("previous_school_name", "")
        previous_class = request.form.get("previous_class", "")
        previous_marks = parse_numeric(request.form.get("previous_marks"))
        tc_number = request.form.get("tc_number", "")

        sql = """
            UPDATE student SET 
                academic_session= %s, admission_no = %s, admission_date = %s, student_class = %s, section = %s, roll_no = %s,
                first_name = %s, middle_name = %s, last_name = %s, date_of_birth = %s, gender = %s, blood_group = %s,
                category = %s, religion = %s, mother_tongue = %s, nationality = %s, aadhaar_number = %s,
                father_name = %s, father_occupation = %s, father_phone = %s, mother_name = %s,
                mother_occupation = %s, mother_phone = %s, email_address = %s, annual_income = %s, emergency_contact = %s,
                current_address = %s, current_city = %s, current_state = %s, current_pincode = %s,
                permanent_address = %s, permanent_city = %s, permanent_state = %s, permanent_pincode = %s,
                previous_school_name = %s, previous_class = %s, previous_marks = %s, tc_number = %s 
            WHERE student_id = %s
        """

        data = (
            academic_session, admission_no, admission_date, student_class, section, roll_no,
            first_name, middle_name, last_name, date_of_birth, gender, blood_group,
            category, religion, mother_tongue, nationality, aadhaar_number,
            father_name, father_occupation, father_phone, mother_name,
            mother_occupation, mother_phone, email_address, annual_income, emergency_contact,
            current_address, current_city, current_state, current_pincode,
            permanent_address, permanent_city, permanent_state, permanent_pincode,
            previous_school_name, previous_class, previous_marks, tc_number, id
        )

        cursor.execute(sql, data)
        conn.commit()
        flash("Student updated successfully!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error updating student: {str(e)}", "danger")
    finally:
        cursor.close()

    return redirect("/Search_student_management?submitted=true")


@student.route("/view_student_profile.html/<int:id>")       
def view_student_profile(id):
    cursor = conn.cursor()
    view = None
    try:
        cursor.execute("SELECT * FROM student WHERE student_id=%s", (id,))
        view = cursor.fetchone()
    except Exception as e:
        flash(f"Error loading profile: {str(e)}", "danger")
    finally:
        cursor.close()

    return render_template("login/student/view_student_profile.html", view=view)


def build_filter_query(classes, section, session, query_text):
    sql = "SELECT * FROM student WHERE 1=1"
    values = []

    if classes and classes.strip() != "":
        sql += " AND TRIM(student_class) = %s"
        values.append(classes.strip())

    if section and section.strip() != "":
        sql += " AND TRIM(section) = %s"
        values.append(section.strip())

    if session and session.strip() != "":
        s_val = session.strip()
        short_session = s_val
        if len(s_val) == 9 and "-" in s_val:
            parts = s_val.split("-")
            short_session = f"{parts[0]}-{parts[1][-2:]}"

        sql += " AND (TRIM(academic_session) = %s OR TRIM(academic_session) = %s)"
        values.extend([s_val, short_session])

    if query_text and query_text.strip() != "":
        q = f"%{query_text.strip()}%"
        sql += " AND (first_name LIKE %s OR last_name LIKE %s OR father_name LIKE %s OR admission_no LIKE %s)"
        values.extend([q, q, q, q])

    return sql, values


@student.route("/Search_student_management", methods=["GET"])
def Search_student_management():
    submitted = request.args.get("submitted", "").strip()
    section = request.args.get("section", "").strip()
    classes = request.args.get("classes", "").strip()
    session = request.args.get("session", "").strip()
    query_text = request.args.get("query", "").strip()

    try:
        page = int(request.args.get("page", 1))
    except ValueError:
        page = 1

    per_page = 10
    offset = (page - 1) * per_page

    students = []
    total = 0
    total_pages = 1

    if submitted == "true":
        cursor = conn.cursor()
        try:
            sql, values = build_filter_query(classes, section, session, query_text)

            count_sql = sql.replace("SELECT *", "SELECT COUNT(*)", 1)
            cursor.execute(count_sql, tuple(values))
            row = cursor.fetchone()
            total = row[0] if row else 0
            total_pages = max(1, (total + per_page - 1) // per_page)

            paginated_sql = sql + " ORDER BY student_id DESC LIMIT %s OFFSET %s"
            final_values = tuple(values) + (per_page, offset)

            cursor.execute(paginated_sql, final_values)
            students = cursor.fetchall()
        except Exception as e:
            flash(f"Error fetching student records: {str(e)}", "danger")
        finally:
            cursor.close()

    return render_template(
        "login/student/view_student.html",
        students=students,
        submitted=submitted,
        page=page,
        total_pages=total_pages,
        total_students=total,
        classes=classes,
        section=section,
        session=session,
        query=query_text
    )


@student.route("/students/export")
def export_student():
    cursor = conn.cursor()
    try:
        section = request.args.get("section", "").strip()
        classes = request.args.get("classes", "").strip()
        session = request.args.get("session", "").strip()
        query_text = request.args.get("query", "").strip()

        sql, values = build_filter_query(classes, section, session, query_text)
        
        cursor.execute(sql, tuple(values))
        data = cursor.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "database id", "academic_session", "admission_no", "admission_date", "student_class", "section", "roll_no",
            "first_name", "middle_name", "last_name", "date_of_birth", "gender", "blood_group", "category", "religion",
            "mother_tongue", "nationality", "aadhaar_number", "father_name", "father_occupation", "father_phone",
            "mother_name", "mother_occupation", "mother_phone", "email_address", "annual_income", "emergency_contact",
            "current_address", "current_city", "current_state", "current_pincode", "permanent_address", "permanent_city",
            "permanent_state", "permanent_pincode", "previous_school_name", "previous_class", "previous_marks", "tc_number"
        ])
        
        formatted_data = []
        for row in data:
            row_list = list(row)
            if len(row_list) > 17 and row_list[17]:
                row_list[17] = f'="{str(row_list[17]).strip()}"'
            formatted_data.append(row_list)

        writer.writerows(formatted_data)
        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=filtered_students.csv"}
        )
    except Exception as e:
        flash(f"Error exporting data: {str(e)}", "danger")
        return redirect("/Search_student_management?submitted=true")
    finally:
        cursor.close()