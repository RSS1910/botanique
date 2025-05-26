from app import app, db
from models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with app.app_context():
    # Check if the admin user already exists
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        # Update existing admin user
        admin.email = 'admin@botanique.com'
        admin.is_admin = True
        admin.set_password('Botanique123!')
        db.session.commit()
        print("Admin user 'admin' updated with new password: Botanique123!")
    else:
        # Create new admin user
        admin = User()
        admin.username='admin'
        admin.email='admin@botanique.com',\
        admin.is_admin=True
        admin.set_password('Botanique123!')
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin user 'admin' created with password: Botanique123!")