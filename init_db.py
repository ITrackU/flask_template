# init_db.py
from app import create_app
from models import db
import os

def init_database():
    # Check if database file already exists
    db_path = 'secure_app.db'
    if os.path.exists(db_path):
        print(f"Database {db_path} already exists.")
        user_input = input("Do you want to reset the database? (y/N): ")
        if user_input.lower() != 'y':
            print("Database initialization cancelled.")
            return
        os.remove(db_path)
        print("Existing database removed.")

    # Create database
    app = create_app()  # Use the factory function to create app
    with app.app_context():
        print("Creating new database...")
        db.create_all()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
