
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
import re

from database import conn


# ============================================================
# STUDENT BLUEPRINT
# ============================================================
student = Blueprint("student", __name__)


# ============================================================
# CONFIGURATION
# ============================================================
PER_PAGE = 10


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def clean_value(value):
    """
    Safely convert form input into a trimmed string.
    """
    if value is None:
        return ""

    return str(value).strip()


def parse_numeric(value):
    """
    Convert a numeric input into float.
    Return None when the value is empty or invalid.
    """
    value = clean_value(value)

    if not value:
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def is_valid_email(email):
    """
    Validate the basic structure of an email address.
    """
    if not email:
        return False

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """
    Validate a 10-digit phone number.
    """
    phone = clean_value(phone)

    return phone.isdigit() and len(phone) == 10


def is_valid_pincode(pincode):
    """
    Validate a standard 6-digit Indian PIN code.
    Empty PIN codes are allowed because some fields may be optional.
    """
    pincode = clean_value(pincode)

    if not pincode:
        return True

    return pincode.isdigit() and len(pincode) == 6


def get_student_form_data():
    """
    Collect and clean all student form fields.
    """

    return {
        "academic_session": clean_value(
            request.form.get("academic_session")
        ),
        "admission_no": clean_value(
            request.form.get("admission_no")
        ),
        "admission_date": clean_value(
            request.form.get("admission_date")
        ),
        "student_class": clean_value(
            request.form.get("class")
        ),
        "section": clean_value(
            request.form.get("section")
        ),
        "roll_no": clean_value(
            request.form.get("roll_no")
        ),

        "first_name": clean_value(
            request.form.get("first_name")
        ),
        "middle_name": clean_value(
            request.form.get("middle_name")
        ),
        "last_name": clean_value(
            request.form.get("last_name")
        ),
        "date_of_birth": clean_value(
            request.form.get("date_of_birth")
        ),
        "gender": clean_value(
            request.form.get("gender")
        ),
        "blood_group": clean_value(
            request.form.get("blood_group")
        ),
        "category": clean_value(
            request.form.get("category")
        ),
        "religion": clean_value(
            request.form.get("religion")
        ),
        "mother_tongue": clean_value(
            request.form.get("mother_tongue")
        ),
        "nationality": clean_value(
            request.form.get("nationality")
        ),
        "aadhaar_number": clean_value(
            request.form.get("aadhaar_number")
        ),

        "father_name": clean_value(
            request.form.get("father_name")
        ),
        "father_occupation": clean_value(
            request.form.get("father_occupation")
        ),
        "father_phone": clean_value(
            request.form.get("father_phone")
        ),
        "mother_name": clean_value(
            request.form.get("mother_name")
        ),
        "mother_occupation": clean_value(
            request.form.get("mother_occupation")
        ),
        "mother_phone": clean_value(
            request.form.get("mother_phone")
        ),
        "email_address": clean_value(
            request.form.get("parent_email")
        ),

        "annual_income": parse_numeric(
            request.form.get("annual_income")
        ),
        "emergency_contact": clean_value(
            request.form.get("emergency_contact")
        ),

        "current_address": clean_value(
            request.form.get("present_address")
        ),
        "current_city": clean_value(
            request.form.get("present_city")
        ),
        "current_state": clean_value(
            request.form.get("present_state")
        ),
        "current_pincode": clean_value(
            request.form.get("present_pincode")
        ),

        "permanent_address": clean_value(
            request.form.get("permanent_address")
        ),
        "permanent_city": clean_value(
            request.form.get("permanent_city")
        ),
        "permanent_state": clean_value(
            request.form.get("permanent_state")
        ),
        "permanent_pincode": clean_value(
            request.form.get("permanent_pincode")
        ),

        "previous_school_name": clean_value(
            request.form.get("previous_school_name")
        ),
        "previous_class": clean_value(
            request.form.get("previous_class")
        ),
        "previous_marks": parse_numeric(
            request.form.get("previous_marks")
        ),
        "tc_number": clean_value(
            request.form.get("tc_number")
        ),
    }


def validate_student_data(data):
    """
    Validate important student fields before database operations.
    """

    if not data["first_name"]:
        return "First name is required."

    if not data["academic_session"]:
        return "Academic session is required."

    if not data["admission_no"]:
        return "Admission number is required."

    if not data["student_class"]:
        return "Class is required."

    if not data["section"]:
        return "Section is required."

    if data["email_address"]:
        if not is_valid_email(data["email_address"]):
            return "Please enter a valid parent email address."

    if data["father_phone"]:
        if not is_valid_phone(data["father_phone"]):
            return "Father phone number must contain 10 digits."

    if data["mother_phone"]:
        if not is_valid_phone(data["mother_phone"]):
            return "Mother phone number must contain 10 digits."

    if data["emergency_contact"]:
        if not is_valid_phone(data["emergency_contact"]):
            return "Emergency contact must contain 10 digits."

    if not is_valid_pincode(data["current_pincode"]):
        return "Present address PIN code must contain 6 digits."

    if not is_valid_pincode(data["permanent_pincode"]):
        return "Permanent address PIN code must contain 6 digits."

    if data["annual_income"] is not None:
        if data["annual_income"] < 0:
            return "Annual income cannot be negative."

    if data["previous_marks"] is not None:
        if data["previous_marks"] < 0 or data["previous_marks"] > 100:
            return "Previous marks must be between 0 and 100."

    return None


# ============================================================
# STUDENT VIEW REDIRECT
# ============================================================
@student.route("/view_student.html")
def fetchall_all_student():

    # Keep the existing redirect URL unchanged.
    return redirect("/Search_student_management")


# ============================================================
# ADD STUDENT PAGE
# ============================================================
@student.route("/add_new_student.html")
def add_new_student():

    return render_template(
        "login/student/add_new_student.html"
    )


# ============================================================
# ADD NEW STUDENT
# ============================================================
@student.route("/add_new_student", methods=["POST"])
def add_new():

    data = get_student_form_data()

    # Validate the submitted student information.
    validation_error = validate_student_data(data)

    if validation_error:
        flash(validation_error, "danger")
        return redirect("/add_new_student.html")

    cursor = None

    try:
        cursor = conn.cursor()

        # Use a parameterized query to prevent SQL injection.
        sql = """
            INSERT INTO student (
                academic_session,
                admission_no,
                admission_date,
                student_class,
                section,
                roll_no,
                first_name,
                middle_name,
                last_name,
                date_of_birth,
                gender,
                blood_group,
                category,
                religion,
                mother_tongue,
                nationality,
                aadhaar_number,
                father_name,
                father_occupation,
                father_phone,
                mother_name,
                mother_occupation,
                mother_phone,
                email_address,
                annual_income,
                emergency_contact,
                current_address,
                current_city,
                current_state,
                current_pincode,
                permanent_address,
                permanent_city,
                permanent_state,
                permanent_pincode,
                previous_school_name,
                previous_class,
                previous_marks,
                tc_number
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        values = (
            data["academic_session"],
            data["admission_no"],
            data["admission_date"],
            data["student_class"],
            data["section"],
            data["roll_no"],
            data["first_name"],
            data["middle_name"],
            data["last_name"],
            data["date_of_birth"],
            data["gender"],
            data["blood_group"],
            data["category"],
            data["religion"],
            data["mother_tongue"],
            data["nationality"],
            data["aadhaar_number"],
            data["father_name"],
            data["father_occupation"],
            data["father_phone"],
            data["mother_name"],
            data["mother_occupation"],
            data["mother_phone"],
            data["email_address"],
            data["annual_income"],
            data["emergency_contact"],
            data["current_address"],
            data["current_city"],
            data["current_state"],
            data["current_pincode"],
            data["permanent_address"],
            data["permanent_city"],
            data["permanent_state"],
            data["permanent_pincode"],
            data["previous_school_name"],
            data["previous_class"],
            data["previous_marks"],
            data["tc_number"],
        )

        cursor.execute(sql, values)

        # Commit the new student record.
        conn.commit()

        flash(
            "Student added successfully!",
            "success"
        )

    except Exception:
        # Roll back the transaction when an error occurs.
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to add the student. Please check the information and try again.",
            "danger"
        )

    finally:
        # Always close the database cursor.
        if cursor:
            cursor.close()

    # Keep the existing redirect unchanged.
    return redirect(
        "/Search_student_management?submitted=true"
    )


# ============================================================
# DELETE STUDENT
# ============================================================
@student.route("/delete/<int:id>")
def delete_student(id):

    if id <= 0:
        flash(
            "Invalid student ID.",
            "danger"
        )
        return redirect(
            "/Search_student_management?submitted=true"
        )

    cursor = None

    try:
        cursor = conn.cursor()

        # Check whether the student exists.
        cursor.execute(
            """
            SELECT student_id
            FROM student
            WHERE student_id = %s
            """,
            (id,)
        )

        existing_student = cursor.fetchone()

        if not existing_student:
            flash(
                "Student not found.",
                "warning"
            )

        else:
            # Delete only the selected student.
            cursor.execute(
                """
                DELETE FROM student
                WHERE student_id = %s
                """,
                (id,)
            )

            conn.commit()

            flash(
                "Student deleted successfully!",
                "success"
            )

    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to delete the student. Please try again.",
            "danger"
        )

    finally:
        if cursor:
            cursor.close()

    # Preserve the existing redirect behavior.
    if request.referrer and "Search_student_management" in request.referrer:
        return redirect(request.referrer)

    return redirect(
        "/Search_student_management?submitted=true"
    )


# ============================================================
# EDIT STUDENT PAGE
# ============================================================
@student.route("/edit_student.html/<int:id>")
def edit_student(id):

    if id <= 0:
        flash(
            "Invalid student ID.",
            "danger"
        )
        return redirect(
            "/Search_student_management"
        )

    cursor = None
    edit = None

    try:
        cursor = conn.cursor()

        # Fetch the selected student.
        cursor.execute(
            """
            SELECT *
            FROM student
            WHERE student_id = %s
            """,
            (id,)
        )

        edit = cursor.fetchone()

        if not edit:
            flash(
                "Student not found.",
                "warning"
            )

    except Exception:
        flash(
            "Unable to load student details. Please try again.",
            "danger"
        )

    finally:
        if cursor:
            cursor.close()

    return render_template(
        "login/student/edit_student.html",
        edit=edit
    )


# ============================================================
# UPDATE STUDENT
# ============================================================
@student.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):

    if id <= 0:
        flash(
            "Invalid student ID.",
            "danger"
        )
        return redirect(
            "/Search_student_management"
        )

    data = get_student_form_data()

    # Validate the updated student information.
    validation_error = validate_student_data(data)

    if validation_error:
        flash(
            validation_error,
            "danger"
        )
        return redirect(
            f"/edit_student.html/{id}"
        )

    cursor = None

    try:
        cursor = conn.cursor()

        # Make sure the student still exists.
        cursor.execute(
            """
            SELECT student_id
            FROM student
            WHERE student_id = %s
            """,
            (id,)
        )

        existing_student = cursor.fetchone()

        if not existing_student:
            flash(
                "Student not found.",
                "warning"
            )
            return redirect(
                "/Search_student_management"
            )

        # Use a parameterized UPDATE query.
        sql = """
            UPDATE student SET
                academic_session = %s,
                admission_no = %s,
                admission_date = %s,
                student_class = %s,
                section = %s,
                roll_no = %s,
                first_name = %s,
                middle_name = %s,
                last_name = %s,
                date_of_birth = %s,
                gender = %s,
                blood_group = %s,
                category = %s,
                religion = %s,
                mother_tongue = %s,
                nationality = %s,
                aadhaar_number = %s,
                father_name = %s,
                father_occupation = %s,
                father_phone = %s,
                mother_name = %s,
                mother_occupation = %s,
                mother_phone = %s,
                email_address = %s,
                annual_income = %s,
                emergency_contact = %s,
                current_address = %s,
                current_city = %s,
                current_state = %s,
                current_pincode = %s,
                permanent_address = %s,
                permanent_city = %s,
                permanent_state = %s,
                permanent_pincode = %s,
                previous_school_name = %s,
                previous_class = %s,
                previous_marks = %s,
                tc_number = %s
            WHERE student_id = %s
        """

        values = (
            data["academic_session"],
            data["admission_no"],
            data["admission_date"],
            data["student_class"],
            data["section"],
            data["roll_no"],
            data["first_name"],
            data["middle_name"],
            data["last_name"],
            data["date_of_birth"],
            data["gender"],
            data["blood_group"],
            data["category"],
            data["religion"],
            data["mother_tongue"],
            data["nationality"],
            data["aadhaar_number"],
            data["father_name"],
            data["father_occupation"],
            data["father_phone"],
            data["mother_name"],
            data["mother_occupation"],
            data["mother_phone"],
            data["email_address"],
            data["annual_income"],
            data["emergency_contact"],
            data["current_address"],
            data["current_city"],
            data["current_state"],
            data["current_pincode"],
            data["permanent_address"],
            data["permanent_city"],
            data["permanent_state"],
            data["permanent_pincode"],
            data["previous_school_name"],
            data["previous_class"],
            data["previous_marks"],
            data["tc_number"],
            id,
        )

        cursor.execute(
            sql,
            values
        )

        conn.commit()

        flash(
            "Student updated successfully!",
            "success"
        )

    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to update the student. Please try again.",
            "danger"
        )

    finally:
        if cursor:
            cursor.close()

    return redirect(
        "/Search_student_management?submitted=true"
    )


# ============================================================
# VIEW STUDENT PROFILE
# ============================================================
@student.route("/view_student_profile.html/<int:id>")
def view_student_profile(id):

    if id <= 0:
        flash(
            "Invalid student ID.",
            "danger"
        )
        return redirect(
            "/Search_student_management"
        )

    cursor = None
    view = None

    try:
        cursor = conn.cursor()

        # Fetch the selected student's profile.
        cursor.execute(
            """
            SELECT *
            FROM student
            WHERE student_id = %s
            """,
            (id,)
        )

        view = cursor.fetchone()

        if not view:
            flash(
                "Student profile not found.",
                "warning"
            )

    except Exception:
        flash(
            "Unable to load student profile. Please try again.",
            "danger"
        )

    finally:
        if cursor:
            cursor.close()

    return render_template(
        "login/student/view_student_profile.html",
        view=view
    )


# ============================================================
# BUILD STUDENT FILTER QUERY
# ============================================================
def build_filter_query(
    classes,
    section,
    session,
    query_text
):
    """
    Build a safe parameterized student search query.
    """

    sql = """
        SELECT *
        FROM student
        WHERE 1 = 1
    """

    values = []

    # Filter by class.
    if classes:
        sql += """
            AND TRIM(student_class) = %s
        """
        values.append(classes)

    # Filter by section.
    if section:
        sql += """
            AND TRIM(section) = %s
        """
        values.append(section)

    # Filter by academic session.
    if session:
        short_session = session

        # Support both long and short academic session formats.
        if len(session) == 9 and "-" in session:
            parts = session.split("-")

            if len(parts) == 2:
                short_session = (
                    f"{parts[0]}-{parts[1][-2:]}"
                )

        sql += """
            AND (
                TRIM(academic_session) = %s
                OR TRIM(academic_session) = %s
            )
        """

        values.extend([
            session,
            short_session,
        ])

    # Search by common student-related fields.
    if query_text:
        search_value = f"%{query_text}%"

        sql += """
            AND (
                first_name LIKE %s
                OR middle_name LIKE %s
                OR last_name LIKE %s
                OR father_name LIKE %s
                OR admission_no LIKE %s
                OR roll_no LIKE %s
            )
        """

        values.extend([
            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
        ])

    return sql, values


# ============================================================
# STUDENT SEARCH / FILTER / PAGINATION
# ============================================================
@student.route(
    "/Search_student_management",
    methods=["GET"]
)
def Search_student_management():

    submitted = clean_value(
        request.args.get("submitted")
    )

    section = clean_value(
        request.args.get("section")
    )

    classes = clean_value(
        request.args.get("classes")
    )

    session = clean_value(
        request.args.get("session")
    )

    query_text = clean_value(
        request.args.get("query")
    )

    # Safely parse the page number.
    try:
        page = int(
            request.args.get("page", 1)
        )
    except (ValueError, TypeError):
        page = 1

    if page < 1:
        page = 1

    offset = (page - 1) * PER_PAGE

    students = []
    total = 0
    total_pages = 1

    if submitted == "true":

        cursor = None

        try:
            cursor = conn.cursor()

            sql, values = build_filter_query(
                classes,
                section,
                session,
                query_text
            )

            # Count matching records.
            count_sql = """
                SELECT COUNT(*)
                FROM (
            """ + sql.replace(
                "SELECT *",
                "SELECT 1",
                1
            ) + """
                ) AS filtered_students
            """

            cursor.execute(
                count_sql,
                tuple(values)
            )

            row = cursor.fetchone()

            total = (
                row[0]
                if row
                else 0
            )

            total_pages = max(
                1,
                (total + PER_PAGE - 1) // PER_PAGE
            )

            # Prevent requesting a page beyond the last page.
            if page > total_pages:
                page = total_pages
                offset = (
                    page - 1
                ) * PER_PAGE

            # Fetch only 10 students per page.
            paginated_sql = (
                sql
                + """
                    ORDER BY student_id DESC
                    LIMIT %s OFFSET %s
                """
            )

            final_values = (
                tuple(values)
                + (PER_PAGE, offset)
            )

            cursor.execute(
                paginated_sql,
                final_values
            )

            students = cursor.fetchall()

        except Exception:
            try:
                conn.rollback()
            except Exception:
                pass

            flash(
                "Unable to fetch student records. Please try again.",
                "danger"
            )

        finally:
            if cursor:
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
        query=query_text,
    )


# ============================================================
# EXPORT STUDENTS TO CSV
# ============================================================
@student.route("/students/export")
def export_student():

    cursor = None

    try:
        # Read the same filters used on the student management page.
        section = clean_value(
            request.args.get("section")
        )

        classes = clean_value(
            request.args.get("classes")
        )

        session = clean_value(
            request.args.get("session")
        )

        query_text = clean_value(
            request.args.get("query")
        )

        sql, values = build_filter_query(
            classes,
            section,
            session,
            query_text
        )

        cursor = conn.cursor()

        # Fetch all records matching the selected filters.
        cursor.execute(
            sql,
            tuple(values)
        )

        data = cursor.fetchall()

        # Create the CSV file in memory.
        output = io.StringIO()

        writer = csv.writer(
            output
        )

        # CSV column headers.
        writer.writerow([
            "database id",
            "academic_session",
            "admission_no",
            "admission_date",
            "student_class",
            "section",
            "roll_no",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "blood_group",
            "category",
            "religion",
            "mother_tongue",
            "nationality",
            "aadhaar_number",
            "father_name",
            "father_occupation",
            "father_phone",
            "mother_name",
            "mother_occupation",
            "mother_phone",
            "email_address",
            "annual_income",
            "emergency_contact",
            "current_address",
            "current_city",
            "current_state",
            "current_pincode",
            "permanent_address",
            "permanent_city",
            "permanent_state",
            "permanent_pincode",
            "previous_school_name",
            "previous_class",
            "previous_marks",
            "tc_number",
        ])

        formatted_data = []

        for row in data:

            row_list = list(row)

            # Preserve Aadhaar values as text in spreadsheet software.
            if (
                len(row_list) > 17
                and row_list[17]
            ):
                row_list[17] = (
                    f'="{str(row_list[17]).strip()}"'
                )

            formatted_data.append(
                row_list
            )

        writer.writerows(
            formatted_data
        )

        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                    "attachment; "
                    "filename=filtered_students.csv"
            },
        )

    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass

        flash(
            "Unable to export student data. Please try again.",
            "danger"
        )

        # Keep the existing redirect unchanged.
        return redirect(
            "/Search_student_management?submitted=true"
        )

    finally:
        if cursor:
            cursor.close()
