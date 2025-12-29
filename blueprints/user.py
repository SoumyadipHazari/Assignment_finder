from flask import Blueprint, abort, current_app, send_from_directory
from flask_login import login_required
from model import Level, Course, Assignment
from flask import render_template


user_bp = Blueprint("user", __name__)



@user_bp.route("/levels")
@login_required
def levels():
    levels = Level.query.all()

    return render_template(
        "user/levels.html",
        levels=levels
    )


@user_bp.route("/levels/<string:level_name>/courses")
@login_required
def courses_by_level(level_name):
    level = Level.query.filter_by(name=level_name).first_or_404()

    courses = Course.query.filter_by(level_id=level.id).all()

    return render_template(
        "user/courses.html",
        level=level,
        courses=courses
    )


@user_bp.route("/courses/<int:course_id>/weeks")
@login_required
def weeks_by_course(course_id):
    course = Course.query.get_or_404(course_id)

    assignments = Assignment.query.filter_by(
        course_id=course.id
    ).order_by(Assignment.week_number).all()

    return render_template(
        "user/weeks.html",
        course=course,
        assignments=assignments
    )



@user_bp.route("/assignment/<int:assignment_id>/view")
@login_required
def view_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

   
    directory = current_app.static_folder
    filepath = assignment.pdf_path

    return send_from_directory(
        directory=directory,
        path=filepath,
        as_attachment=False
    )
