from flask import Flask, send_from_directory
import os

# ===========================
# Blueprints
# ===========================

from routes.website import website
from routes.auth import auth
from routes.student import student
from routes.fee import fees
from routes.inquery_con import inquiry_contacts
from routes.career_inquiry import career
from routes.notice import notice_bp

app = Flask(__name__, static_folder="statics", static_url_path="/static")
app.secret_key = "super_secret_key"

# ===========================
# Register Blueprints
# ===========================
app.register_blueprint(website)
app.register_blueprint(auth)
app.register_blueprint(student)
app.register_blueprint(fees)
app.register_blueprint(inquiry_contacts)
app.register_blueprint(career)
app.register_blueprint(notice_bp)

# =========================================================
# GLOBAL CACHE DISABLE (BACK BUTTON SECURITY)
# =========================================================
@app.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
# ===========================
# Static Folder
# ===========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, "statics")


@app.route("/Assest/Css/<path:filename>")
def assest_css(filename):
    return send_from_directory(
        os.path.join(STATIC_ROOT, "Css"),
        filename
    )


@app.route("/Assest/Image/<path:filename>")
def assest_image(filename):
    return send_from_directory(
        os.path.join(STATIC_ROOT, "image"),
        filename
    )


@app.route("/WebAssets/<path:filename>")
def webassets(filename):

    if filename.startswith("banner-image/"):
        return send_from_directory(
            os.path.join(STATIC_ROOT, "image", "banner-image"),
            filename[len("banner-image/"):]
        )

    return send_from_directory(
        os.path.join(STATIC_ROOT, "image", "WebAssets"),
        filename
    )


@app.route("/HelperJs/<path:filename>")
def helper_js(filename):
    return send_from_directory(
        os.path.join(STATIC_ROOT, "js", "HelperJs"),
        filename
    )


@app.route("/MobileJs/<path:filename>")
def mobile_js(filename):
    return send_from_directory(
        os.path.join(STATIC_ROOT, "js"),
        filename
    )


@app.route("/parsleyjs/<path:filename>")
def parsley_js(filename):
    return send_from_directory(
        os.path.join(STATIC_ROOT, "parsleyjs"),
        filename
    )


@app.route("/toastr/<path:filename>")
def toastr_files(filename):
    return send_from_directory(
        os.path.join(STATIC_ROOT, "toastr"),
        filename
    )


if __name__ == "__main__":
    app.run(debug=True)