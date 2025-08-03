# app/models.py

from . import db
from flask_login import UserMixin
from datetime import datetime

# User model to handle authentication and roles
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'seeker', 'employer', or 'admin'

    # Relationships
    jobs = db.relationship('Job', backref='employer', lazy=True)
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"


# Job model to store job listings
class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)  # ✅ Added field
    description = db.Column(db.Text, nullable=False)
    salary = db.Column(db.String(50))
    location = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ Added field

    # Foreign key to link to employer
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to applications
    applications = db.relationship('Application', backref='job', lazy=True)

    def __repr__(self):
        return f"<Job {self.title} at {self.company_name} in {self.location}>"


# Application model to store who applied to which job
class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ New fields
    phone = db.Column(db.String(20))
    cover_letter = db.Column(db.Text)
    resume_filename = db.Column(db.String(200))

    def __repr__(self):
        return f"<Application User {self.user_id} -> Job {self.job_id}>"

