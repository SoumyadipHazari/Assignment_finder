from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from model import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()


        if not name:
            flash("Please enter your name.")
            return redirect(url_for("auth.home"))


        user = User.query.filter_by(name=name).first()

        if not user:
            flash("User not found. Access denied.")
            return redirect(url_for("auth.home"))


        login_user(user)


        if user.role == "admin":
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("user.levels"))

    return render_template("home/home.html")



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.home"))
