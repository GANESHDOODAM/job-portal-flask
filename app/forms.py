from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length
from wtforms import FileField

# Registration form for Job Seekers and Employers
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(), Length(min=4, max=150)
    ])
    email = StringField("Email", validators=[
        InputRequired(), Email(), Length(max=150)
    ])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=6)
    ])
    role = SelectField("Role", choices=[
        ('seeker', 'Job Seeker'), 
        ('employer', 'Employer')
    ], validators=[InputRequired()])
    submit = SubmitField("Register")

# Login form for all users
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(), Length(min=4, max=150)
    ])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=6)
    ])
    submit = SubmitField("Login")

# Form for employers to post a job
class JobForm(FlaskForm):
    title = StringField("Job Title", validators=[
        InputRequired(), Length(max=100)
    ])
    company_name = StringField("Company Name", validators=[       # ✅ Added this line
        InputRequired(), Length(max=100)
    ])
    description = TextAreaField("Job Description", validators=[
        InputRequired()
    ])
    salary = StringField("Salary (optional)")
    location = StringField("Location", validators=[
        InputRequired(), Length(max=100)
    ])
    submit = SubmitField("Post Job")


class ApplicationForm(FlaskForm):
    phone = StringField("Phone Number", validators=[InputRequired(), Length(min=10, max=20)])
    cover_letter = TextAreaField("Cover Letter (Optional)")
    resume = FileField("Upload Resume (PDF only)", validators=[InputRequired()])
    submit = SubmitField("Submit Application")

