🧑‍💼 Job Portal Web Application

- This is a Job Portal Web App developed as a part of my training program. It allows Job Seekers, Employers, and Admins to interact within a simplified job recruitment platform.

📌 Features

👤 User Roles

- Job Seekers: Register, search for jobs, apply by submitting resume and details.

- Employers: Post job listings, view applicants.

- Admins: Manage all users and jobs.

✅ Functional Highlights

- Secure user authentication (Flask-Login)

- Resume upload (PDF)

- Job application form with seeker details

- Job listing with filters (location, keyword)

- Role-based dashboards

- Admin panel (user & job deletion)

- Flash messages and user feedback

- Responsive Bootstrap UI

🛠️ Technologies Used

- Python + Flask

- HTML/CSS + Bootstrap 5

- SQLite3 (development)

- Flask-WTF (forms & validation)

- Flask-Login (authentication)

- Werkzeug (file handling)

- Jinja2 (templating)


Step-by-step process

1.Set Up Virtual Environment

- bash
python3 -m venv venv
source venv/bin/activate


2.Install Dependencies

bash
pip install -r requirements.txt


3.Run the App

bash
flask run
Visit: http://127.0.0.1:5000

🧪 Admin Credentials
To add an admin manually via Flask shell:

from app import db
from app.models import User
from werkzeug.security import generate_password_hash

admin = User(username="admin_username", email="admin@example.com", password=generate_password_hash("admin_password"), role="admin")
db.session.add(admin)
db.session.commit()


🧾 Developer Details
- Developed by: Ganesh Doodam
- Employee Code: IT-4623-09K
- Training Program: Python Developer Program (August 2025 Batch)

📄 License
This project is licensed for academic and training purposes only.

