from app import app, db
from database import initialize_database

# Run this script to initialize the database with sample data
if __name__ == "__main__":
    with app.app_context():
        initialize_database()
