
from flask import Blueprint,render_template,request,redirect,url_for,session,make_response


# ============================================================
# WEBSITE BLUEPRINT
# ============================================================
website = Blueprint("website", __name__)


# ============================================================
# SECURITY HEADER HELPER
# ============================================================
def apply_security_headers(response, no_cache=False):
    """
    Apply basic security-related HTTP headers.
    """

    # Prevent MIME type sniffing.
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent the page from being embedded by other websites.
    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    # Control how much referrer information is sent.
    response.headers["Referrer-Policy"] = (
        "strict-origin-when-cross-origin"
    )

    # Disable browser caching when required.
    if no_cache:
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, "
            "max-age=0, post-check=0, pre-check=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

    return response


# ============================================================
# HOME
# ============================================================
@website.route("/")
def index():

    response = make_response(
        render_template("index.html")
    )

    return apply_security_headers(response)


# ============================================================
# DASHBOARD
# ============================================================
@website.route("/dashboard.html")
def dashboard():

    # Check whether the user is logged in.
    if not session.get("logged_in"):
        return redirect(
            url_for("auth.login")
        )

    # Make sure only an administrator can access the dashboard.
    if session.get("role") != "admin":
        session.clear()

        return redirect(
            url_for("auth.login")
        )

    # Render the dashboard with browser caching disabled.
    response = make_response(
        render_template("login/dashboard.html")
    )

    return apply_security_headers(
        response,
        no_cache=True
    )


# ============================================================
# STUDENT RESULT
# ============================================================
@website.route("/student_result.html")
def result():

    response = make_response(
        render_template(
            "login/student_result.html"
        )
    )

    return apply_security_headers(response)


# ============================================================
# ABOUT
# ============================================================
@website.route("/history-of-ssv.html")
def history_of_kdb():
    return render_template(
        "about/history-of-ssv.html"
    )


@website.route("/our-mission-and-vision.html")
def our_mission_and_vision():
    return render_template(
        "about/our-mission-and-vision.html"
    )


@website.route("/our-education-system.html")
def our_education_system():
    return render_template(
        "about/our-education-system.html"
    )


@website.route("/chairman-message.html")
def chairman_message():
    return render_template(
        "about/chairman-message.html"
    )


@website.route("/vice-president-message.html")
def vice_president():
    return render_template(
        "about/vice-president-message.html"
    )


@website.route("/school-management-committee.html")
def school_management_committee():
    return render_template(
        "about/school-management-committee.html"
    )


@website.route("/manager-message.html")
def manager_message():
    return render_template(
        "about/manager-message.html"
    )


@website.route("/principal-message.html")
def principal_message():
    return render_template(
        "about/principal-message.html"
    )


@website.route("/mandatory-public-disclosure.html")
def mandatory_public_disclosure():
    return render_template(
        "about/mandatory-public-disclosure.html"
    )


# ============================================================
# ADMISSION
# ============================================================
@website.route("/faq.html")
def faq():
    return render_template(
        "admission/faq.html"
    )


@website.route("/admission-syllabus.html")
def admission_syllabus():
    return render_template(
        "admission/admission-syllabus.html"
    )


@website.route("/admission-procedure.html")
def admission_procedure():
    return render_template(
        "admission/admission-procedure.html"
    )


@website.route("/fee-structure.html")
def fee_structure():
    return render_template(
        "admission/fee-structure.html"
    )


@website.route("/admission-form.html")
def admission_form():
    return render_template(
        "admission/admission-form.html"
    )


# ============================================================
# ACADEMICS
# ============================================================
@website.route("/teacher-list.html")
def teacher_list():
    return render_template(
        "academics/teacher-list.html"
    )


@website.route("/academic_calender.html")
def academic_plan():
    return render_template(
        "academics/academic_calender.html"
    )


@website.route("/achievers.html")
def achievers():
    return render_template(
        "academics/achievers.html"
    )


@website.route("/Planner.html")
def planner():
    return render_template(
        "academics/Planner.html"
    )


@website.route("/bifurcated-syllabus.html")
def bifurcated_syllabus():
    return render_template(
        "academics/bifurcated-syllabus.html"
    )


@website.route("/school-book-timetable.html")
def school_book_timetable():
    return render_template(
        "academics/school-book-timetable.html"
    )


@website.route("/board-toppers.html")
def board_toppers():
    return render_template(
        "academics/board-toppers.html"
    )


# ============================================================
# STUDENT CORNER
# ============================================================
@website.route("/Transportfaq.html")
def transportfaq():
    return render_template(
        "student_corner/Transportfaq.html"
    )


@website.route("/fee-payment.html")
def fee_payment():
    return render_template(
        "student_corner/fee-payment.html"
    )


@website.route("/school-discipline.html")
def school_discipline():
    return render_template(
        "student_corner/school-discipline.html"
    )


@website.route("/general-rules.html")
def general_rules():
    return render_template(
        "student_corner/general-rules.html"
    )


@website.route("/attendance.html")
def attendance():
    return render_template(
        "student_corner/attendance.html"
    )


@website.route("/timing.html")
def timing():
    return render_template(
        "student_corner/timing.html"
    )


@website.route("/house-system.html")
def house_system():
    return render_template(
        "student_corner/house-system.html"
    )


@website.route("/uniform.html")
def uniform():
    return render_template(
        "student_corner/uniform.html"
    )


@website.route("/transport.html")
def transport():
    return render_template(
        "student_corner/transport.html"
    )


@website.route("/assessment-criteria.html")
def assessment_criteria():
    return render_template(
        "student_corner/assessment-criteria.html"
    )


@website.route("/transfer-certificates.html")
def transfer_certificates():
    return render_template(
        "student_corner/transfer-certificates.html"
    )


@website.route("/student-list.html")
def student_list():
    return render_template(
        "student_corner/student-list.html"
    )


# ============================================================
# CURRICULUM
# ============================================================
@website.route("/scholarships.html")
def scholarships():
    return render_template(
        "curriculums/scholarships.html"
    )


@website.route("/career-counselling-and-guidance.html")
def career_guidance():
    return render_template(
        "curriculums/career-counselling-and-guidance.html"
    )


@website.route("/sports.html")
def sports():
    return render_template(
        "curriculums/sports.html"
    )


@website.route("/visual-and-performing-arts.html")
def visual_and_performing_arts():
    return render_template(
        "curriculums/visual-and-performing-arts.html"
    )


@website.route("/skill-education.html")
def skill_education():
    return render_template(
        "curriculums/skill-education.html"
    )


@website.route("/clubs.html")
def clubs():
    return render_template(
        "curriculums/clubs.html"
    )


@website.route("/alt-robotics.html")
def alt_robotics():
    return render_template(
        "curriculums/alt-robotics.html"
    )


@website.route("/ncc.html")
def ncc():
    return render_template(
        "curriculums/ncc.html"
    )


@website.route("/initiative.html")
def initiative():
    return render_template(
        "curriculums/initiative.html"
    )


# ============================================================
# GALLERY
# ============================================================
@website.route("/photo-gallery.html")
def photo_gallery():
    return render_template(
        "gallery/photo-gallery.html"
    )


# ============================================================
# BLOGS
# ============================================================
@website.route("/bloglist.html")
def blog():
    return render_template(
        "bloglist.html"
    )


# ============================================================
# CONTACT
# ============================================================
@website.route("/contact-us.html")
def contact():
    return render_template(
        "contact/contact-us.html"
    )


@website.route("/career.html")
def career():
    return render_template(
        "contact/career.html"
    )
