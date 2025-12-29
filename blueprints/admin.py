from functools import wraps
from flask import abort
from flask_login import current_user
from flask import render_template

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


import os
from flask import Blueprint, request, redirect, url_for, flash, current_app, abort
from flask_login import login_required
from werkzeug.utils import secure_filename

from model import db, Level, Course, Assignment

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    courses = Course.query.all()
    assignments = Assignment.query.order_by(Assignment.uploaded_at.desc()).all()

    return render_template(
        "admin/dashboard.html",
        total_courses=len(courses),
        total_assignments=len(assignments),
        courses=courses,
        assignments=assignments
        )



@admin_bp.route("/course/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_course():
    if request.method == "POST":
        name = request.form.get("name")
        level_id = request.form.get("level_id")

        if not name or not level_id:
            flash("All fields are required.")
            return redirect(url_for("admin.add_course"))

        existing = Course.query.filter_by(
            name=name, level_id=level_id
        ).first()
        if existing:
            flash("Course already exists.")
            return redirect(url_for("admin.add_course"))

        course = Course(name=name, level_id=level_id)
        db.session.add(course)
        db.session.commit()

        flash("Course added successfully.")
        return redirect(url_for("admin.dashboard"))

    levels = Level.query.all()
    return render_template("admin/add_course.html", levels=levels)



@admin_bp.route("/assignment/upload", methods=["GET", "POST"])
@login_required
@admin_required
def upload_assignment():
    if request.method == "POST":
        course_id = request.form.get("course_id")
        week_number = request.form.get("week_number")
        file = request.files.get("pdf")

        if not all([course_id, week_number, file]):
            flash("All fields are required.")
            return redirect(url_for("admin.upload_assignment"))

        exists = Assignment.query.filter_by(
            course_id=course_id,
            week_number=week_number
        ).first()
        if exists:
            flash("This week's assignment already exists. Use update instead.")
            return redirect(url_for("admin.upload_assignment"))

        if not file.filename.lower().endswith(".pdf"):
            flash("Only PDF files are allowed.")
            return redirect(url_for("admin.upload_assignment"))

        filename = secure_filename(
            f"course_{course_id}_week_{week_number}.pdf"
        )

        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        file.save(os.path.join(upload_dir, filename))

        assignment = Assignment(
            course_id=course_id,
            week_number=week_number,
            pdf_path=f"uploads/solutions/{filename}"
        )
        db.session.add(assignment)
        db.session.commit()

        flash("Assignment uploaded successfully.")
        return redirect(url_for("admin.dashboard"))


    courses = Course.query.all()
    return render_template(
        "admin/upload_assignment.html",
        courses=courses
    )



@admin_bp.route("/assignment/update/<int:assignment_id>", methods=["GET", "POST"])
@login_required
@admin_required
def update_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    if request.method == "POST":
        file = request.files.get("pdf")

        if not file or not file.filename.lower().endswith(".pdf"):
            flash("Only PDF files are allowed.")
            return redirect(
                url_for("admin.update_assignment", assignment_id=assignment.id)
            )

        old_path = os.path.join(
            current_app.static_folder, assignment.pdf_path
        )
        if os.path.exists(old_path):
            os.remove(old_path)

        filename = secure_filename(
            f"course_{assignment.course_id}_week_{assignment.week_number}.pdf"
        )
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)

        file.save(os.path.join(upload_dir, filename))

        assignment.pdf_path = f"uploads/solutions/{filename}"
        db.session.commit()

        flash("Assignment updated successfully.")
        return redirect(url_for("admin.dashboard"))

    return render_template(
        "admin/update_assignment.html",
        assignment=assignment
    )



@admin_bp.route("/assignment/delete/<int:assignment_id>", methods=["POST"])
@login_required
@admin_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    file_path = os.path.join(
        current_app.static_folder, assignment.pdf_path
    )
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(assignment)
    db.session.commit()

    flash("Assignment deleted successfully.")
    return redirect(url_for("admin.dashboard"))
