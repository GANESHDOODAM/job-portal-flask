import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from . import db, login_manager
from .models import User, Job, Application
from .forms import RegisterForm as RegistrationForm, LoginForm, JobForm, ApplicationForm

bp = Blueprint('routes', __name__)
UPLOAD_FOLDER = 'static/resumes'

# Load user for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home route (with filters)
@bp.route('/')
def index():
    location = request.args.get('location')
    keyword = request.args.get('keyword')
    query = Job.query

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if keyword:
        query = query.filter(Job.title.ilike(f"%{keyword}%"))

    jobs = query.all()
    return render_template('index.html', jobs=jobs)


# Register route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in or use a different email.', 'danger')
            return redirect(url_for('routes.register'))

        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html', form=form)


# Login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)


# Dashboard route
@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'employer':
        jobs = Job.query.filter_by(posted_by=current_user.id).all()
        return render_template("dashboard.html", jobs=jobs)

    elif current_user.role == 'seeker':
        all_jobs = Job.query.all()
        applications = Application.query.filter_by(user_id=current_user.id).all()
        applied_job_ids = {app.job_id for app in applications}
        return render_template("dashboard.html", jobs=all_jobs, applications=applications, applied_job_ids=applied_job_ids)

    elif current_user.role == 'admin':
        return redirect(url_for('routes.admin_dashboard'))

    else:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('routes.index'))


# Post a new job
@bp.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'employer':
        flash("Only employers can post jobs.")
        return redirect(url_for('routes.dashboard'))

    form = JobForm()
    if form.validate_on_submit():
        new_job = Job(
            title=form.title.data,
            company_name=form.company_name.data,
            description=form.description.data,
            salary=form.salary.data,
            location=form.location.data,
            posted_by=current_user.id
        )
        db.session.add(new_job)
        db.session.commit()
        flash("Job posted successfully.")
        return redirect(url_for('routes.dashboard'))

    return render_template('post_job.html', form=form)


# Job Listings Page
@bp.route('/jobs', methods=['GET'])
def job_listings():
    location = request.args.get('location')
    keyword = request.args.get('keyword')

    query = Job.query

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if keyword:
        query = query.filter(Job.title.ilike(f"%{keyword}%"))

    jobs = query.all()
    return render_template('job_listings.html', jobs=jobs)


# Apply for a job (GET form and POST application)
@bp.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply(job_id):
    if current_user.role != 'seeker':
        flash("Only job seekers can apply.")
        return redirect(url_for('routes.dashboard'))

    job = Job.query.get_or_404(job_id)
    existing = Application.query.filter_by(user_id=current_user.id, job_id=job.id).first()
    if existing:
        flash("You have already applied to this job.", "warning")
        return redirect(url_for('routes.dashboard'))

    form = ApplicationForm()
    if form.validate_on_submit():
        file = form.resume.data
        if file and file.filename.endswith('.pdf'):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(f"{current_user.username}_{job_id}_{file.filename}")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            application = Application(
                user_id=current_user.id,
                job_id=job.id,
                phone=form.phone.data,
                cover_letter=form.cover_letter.data,
                resume_filename=filename
            )
            db.session.add(application)
            db.session.commit()
            flash("Application submitted successfully!", "success")
            return redirect(url_for('routes.dashboard'))
        else:
            flash("Only PDF files are allowed.", "danger")

    return render_template("apply.html", job=job, form=form)


# Admin dashboard
@bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('routes.dashboard'))
    users = User.query.all()
    jobs = Job.query.all()
    return render_template('admin_dashboard.html', users=users, jobs=jobs)


# Delete user (admin only)
@bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('routes.dashboard'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for('routes.admin_dashboard'))


# Delete job (admin only)
@bp.route('/admin/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('routes.dashboard'))
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully.", "success")
    return redirect(url_for('routes.admin_dashboard'))


# Logout route
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('routes.index'))

'''
# ✅ Temporary route to create admin on deployed DB (e.g., Render)
@bp.route('/create-admin')
def create_admin():
    if User.query.filter_by(username='admin').first():
        return "Admin user already exists!"
    
    admin = User(
        username='admin',
        email='admin@example.com',
        password=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    return "Admin user created!"
'''