from flask import request
from database import conn

def add_admission():
        
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









































