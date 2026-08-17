from flask import Blueprint, render_template, request, redirect, send_from_directory, abort, Response
student = Blueprint("student",__name__)
import io
import csv
from database import conn


@student.route("/view_student.html")
def fetchall_all_student():
    cursor = conn.cursor()

    page = request.args.get("page", 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    cursor.execute("SELECT * FROM student LIMIT %s OFFSET %s", (per_page, offset))
    students = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM student")
    row = cursor.fetchone()
    total = row[0] if row else 0

    cursor.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "login/student/view_student.html",
        students=students,
        page=page,
        total_students=total,
        total_pages=total_pages,
        classes="",
        section="",
        session="",
        query=""
    )

@student.route("/add_new_student.html")
def add_new_student():
    return render_template("login/student/add_new_student.html")

@student.route("/add_new_student", methods=["POST"])
def add_new():
        
        cursor = conn.cursor()
        academic_session = request.form["academic_session"]
        admission_no = request.form["admission_no"]
        admission_date = request.form["admission_date"]
        student_class = request.form["class"]
        section = request.form["section"]
        roll_no = request.form["roll_no"]

        # Student Personal Details
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        date_of_birth = request.form["date_of_birth"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        category = request.form["category"]
        religion = request.form["religion"]
        mother_tongue = request.form["mother_tongue"]
        nationality = request.form["nationality"]
        aadhaar_number = request.form["aadhaar_number"]

        # Parents & Contact Details
        father_name = request.form["father_name"]
        father_occupation = request.form["father_occupation"]
        father_phone = request.form["father_phone"]
        mother_name = request.form["mother_name"]
        mother_occupation = request.form["mother_occupation"]
        mother_phone = request.form["mother_phone"]
        email_address = request.form["parent_email"]
        annual_income = request.form["annual_income"]
        emergency_contact = request.form["emergency_contact"]

        # Current Address
        current_address = request.form["present_address"]
        current_city = request.form["present_city"]
        current_state = request.form["present_state"]
        current_pincode = request.form["present_pincode"]

        # Permanent Address
        permanent_address = request.form["permanent_address"]
        permanent_city = request.form["permanent_city"]
        permanent_state = request.form["permanent_state"]
        permanent_pincode = request.form["permanent_pincode"]

        # Previous Academic History
        previous_school_name = request.form["previous_school_name"]
        previous_class = request.form["previous_class"]
        previous_marks = request.form["previous_marks"]
        tc_number = request.form["tc_number"]

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
        cursor.close()
        return redirect("/view_student.html")


@student.route("/delete/<int:id>")
def delete_student(id):
      cursor = conn.cursor()

      cursor.execute("DELETE FROM student WHERE id = %s",(id,))

      conn.commit()
      cursor.close()
      return redirect("/view_student.html")


@student.route("/edit_student.html/<int:id>")
def edit_student(id):
       
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM student WHERE id=%s",(id,))
       edit = cursor.fetchone()
       cursor.close()
       return render_template("login/student/edit_student.html",edit = edit)



@student.route("/update_student/<int:id>",methods = ["POST"])
def update_student(id):
        
        cursor = conn.cursor()
        academic_session = request.form["academic_session"]
        admission_no = request.form["admission_no"]
        admission_date = request.form["admission_date"]
        student_class = request.form["class"]
        section = request.form["section"]
        roll_no = request.form["roll_no"]

        # Student Personal Details
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        date_of_birth = request.form["date_of_birth"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        category = request.form["category"]
        religion = request.form["religion"]
        mother_tongue = request.form["mother_tongue"]
        nationality = request.form["nationality"]
        aadhaar_number = request.form["aadhaar_number"]

        # Parents & Contact Details
        father_name = request.form["father_name"]
        father_occupation = request.form["father_occupation"]
        father_phone = request.form["father_phone"]
        mother_name = request.form["mother_name"]
        mother_occupation = request.form["mother_occupation"]
        mother_phone = request.form["mother_phone"]
        email_address = request.form["parent_email"]
        annual_income = request.form["annual_income"]
        emergency_contact = request.form["emergency_contact"]

        # Current Address
        current_address = request.form["present_address"]
        current_city = request.form["present_city"]
        current_state = request.form["present_state"]
        current_pincode = request.form["present_pincode"]

        # Permanent Address
        permanent_address = request.form["permanent_address"]
        permanent_city = request.form["permanent_city"]
        permanent_state = request.form["permanent_state"]
        permanent_pincode = request.form["permanent_pincode"]

        # Previous Academic History
        previous_school_name = request.form["previous_school_name"]
        previous_class = request.form["previous_class"]
        previous_marks = request.form["previous_marks"]
        tc_number = request.form["tc_number"]

        sql = """
            UPDATE student SET 
                academic_session= %s, admission_no = %s, admission_date = %s, student_class = %s, section = %s, roll_no = %s,
                first_name = %s, middle_name = %s, last_name = %s, date_of_birth = %s, gender = %s, blood_group = %s,
                category = %s, religion = %s, mother_tongue = %s, nationality = %s, aadhaar_number = %s,
                father_name = %s, father_occupation = %s, father_phone = %s, mother_name = %s,
                mother_occupation = %s, mother_phone = %s, email_address = %s, annual_income = %s, emergency_contact = %s,
                current_address = %s, current_city = %s, current_state = %s, current_pincode = %s,
                permanent_address = %s, permanent_city = %s, permanent_state = %s, permanent_pincode = %s,
                previous_school_name = %s, previous_class = %s, previous_marks = %s, tc_number = %s WHERE id = %s
            
        """

        data = (
            academic_session, admission_no, admission_date, student_class, section, roll_no,
            first_name, middle_name, last_name, date_of_birth, gender, blood_group,
            category, religion, mother_tongue, nationality, aadhaar_number,
            father_name, father_occupation, father_phone, mother_name,
            mother_occupation, mother_phone, email_address, annual_income, emergency_contact,
            current_address, current_city, current_state, current_pincode,
            permanent_address, permanent_city, permanent_state, permanent_pincode,
            previous_school_name, previous_class, previous_marks, tc_number,id
        )
              


        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        return redirect("/view_student.html")


@student.route("/view_student_profile.html/<int:id>")       
def view_student_profile(id):
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM student WHERE id=%s",(id,))
       view = cursor.fetchone()
       cursor.close()
       return render_template("login/student/view_student_profile.html", view=view)


@student.route("/student/export")
@student.route("/students/export")
def export_student():
        cursor = conn.cursor()


        cursor.execute("SELECT * FROM student")
        data = cursor.fetchall()

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(["database id","academic_sessio"," admission_no","admission_date","student_class","section","roll_no","first_name","middle_name", 
        "last_name","date_of_birth", "gender","blood_group","category","religion","mother_tongue","nationality","aadhaar_number","father_name", 
        "father_occupation","father_phone","mother_name","mother_occupation","mother_phone","email_address","annual_income","emergency_contact",
        "current_address","current_city","current_state","current_pincode","permanent_address","permanent_city","permanent_state","permanent_pincode",
        "previous_school_name","previous_class","previous_marks","tc_number"])
        writer.writerows(data)
        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=student.csv"}
        )


        # return export_student()
@student.route("/Search_student_management", methods=["GET"])
def Search_student_management():
    cursor = conn.cursor()

    section = request.args.get("section", "").strip()
    classes = request.args.get("classes", "").strip()
    session = request.args.get("session", "").strip()
    query_text = request.args.get("query", "").strip()

    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    # Debug
    print(f"Class search: '{classes}'")

    # First, let's check what's in the database
    cursor.execute("SELECT student_class, section, academic_session FROM student LIMIT 10")
    sample = cursor.fetchall()
    print(f"Sample data: {sample}")

    # Build query dynamically
    sql = "SELECT * FROM student WHERE 1=1"
    values = []

    if classes:
        # Try multiple approaches
        sql += " AND ("
        sql += " student_class = %s"  # Exact match
        sql += " OR CAST(student_class AS CHAR) LIKE %s"  # Convert to string and match
        sql += " OR student_class LIKE %s"
        sql += ")"
        values.append(classes)
        values.append(f"%{classes}%")
        values.append(f"%{classes}%")
    
    if section:
        sql += " AND section = %s"
        values.append(section)
    
    if session:
        sql += " AND academic_session = %s"
        values.append(session)
    
    if query_text:
        sql += """ AND (
            first_name LIKE %s OR 
            last_name LIKE %s OR 
            father_name LIKE %s
        )"""
        values.append(f"%{query_text}%")
        values.append(f"%{query_text}%")
        values.append(f"%{query_text}%")

    print(f"Final SQL: {sql}")
    print(f"Values: {values}")

    # Get total count
    count_sql = sql.replace("SELECT *", "SELECT COUNT(*)", 1)
    cursor.execute(count_sql, tuple(values))
    row = cursor.fetchone()
    total = row[0] if row else 0
    total_pages = max(1, (total + per_page - 1) // per_page)

    # Execute paginated query
    paginated_sql = sql + " ORDER BY id DESC LIMIT %s OFFSET %s"
    final_values = tuple(values) + (per_page, offset)
    
    cursor.execute(paginated_sql, final_values)
    students = cursor.fetchall()
    cursor.close()

    return render_template(
        "login/student/view_student.html",
        students=students,
        page=page,
        total_pages=total_pages,
        total_students=total,
        classes=classes,
        section=section,
        session=session,
        query=query_text
    )