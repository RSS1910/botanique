from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_admin_user(username, email, password):
    """Create a new admin user."""
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            if existing_user.is_admin:
                logger.info(f"Admin user {username} already exists.")
                return
            else:
                # Upgrade existing user to admin
                existing_user.is_admin = True
                db.session.commit()
                logger.info(f"User {username} has been upgraded to admin.")
                return
        
        # Create new admin user
        admin = User(
            username=username,
            email=email,
            is_admin=True
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        logger.info(f"Admin user {username} created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_admin.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_admin_user(username, email, password)