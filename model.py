from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# -------------------------
# User Model
# -------------------------
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'user'

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"


# -------------------------
# Level Model
# -------------------------
class Level(db.Model):
    __tablename__ = "levels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    courses = db.relationship(
        "Course",
        backref="level",
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Level {self.name}>"


# -------------------------
# Course Model
# -------------------------
class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level_id = db.Column(
        db.Integer,
        db.ForeignKey("levels.id"),
        nullable=False
    )

    assignments = db.relationship(
        "Assignment",
        backref="course",
        lazy=True,
        cascade="all, delete"
    )

    __table_args__ = (
        db.UniqueConstraint("name", "level_id", name="unique_course_per_level"),
    )

    def __repr__(self):
        return f"<Course {self.name}>"


# -------------------------
# Assignment Model
# -------------------------
class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )
    week_number = db.Column(db.Integer, nullable=False)
    pdf_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "course_id",
            "week_number",
            name="unique_assignment_per_week"
        ),
    )

    def __repr__(self):
        return f"<Assignment Course:{self.course_id} Week:{self.week_number}>"
