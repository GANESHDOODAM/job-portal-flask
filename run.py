# run.py

from app import create_app, db

# Create the Flask app instance
app = create_app()

# Initialize the database
with app.app_context():
    db.create_all()  # Automatically creates tables on first run

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
