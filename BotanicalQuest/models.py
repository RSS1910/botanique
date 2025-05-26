from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# User model for authentication and user-specific features
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with UserPlant (saved plants)
    saved_plants = db.relationship('UserPlant', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Plant model for plant database
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    care_instructions = db.Column(db.Text)
    plant_type = db.Column(db.String(50))  # Tree, Shrub, Flower, etc.
    image_url = db.Column(db.String(255))  # URL to an image (could be a local path)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    characteristics = db.relationship('PlantCharacteristic', backref='plant', lazy='dynamic', cascade='all, delete-orphan')
    user_plants = db.relationship('UserPlant', backref='plant', lazy='dynamic', cascade='all, delete-orphan')
    daily_features = db.relationship('DailyFeature', backref='plant', lazy='dynamic')

# PlantCharacteristic model for storing plant identification characteristics
class PlantCharacteristic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    
    # Height range (in cm)
    min_height = db.Column(db.Integer)
    max_height = db.Column(db.Integer)
    
    # Geographic location
    geographic_location = db.Column(db.String(100))
    
    # Flower characteristics
    has_flowers = db.Column(db.Boolean, default=False)
    flower_color = db.Column(db.String(50))
    flowering_season = db.Column(db.String(50))  # Spring, Summer, etc.
    
    # Leaf characteristics
    leaf_shape = db.Column(db.String(50))  # Oval, Heart-shaped, etc.
    leaf_arrangement = db.Column(db.String(50))  # Alternate, Opposite, etc.
    leaf_color = db.Column(db.String(50))
    
    # Bark characteristics (for trees)
    bark_texture = db.Column(db.String(50))  # Smooth, Rough, etc.
    
    # Seasonal changes
    deciduous = db.Column(db.Boolean)  # True for deciduous, False for evergreen
    fall_color = db.Column(db.String(50))
    
    # Fruit characteristics
    has_fruit = db.Column(db.Boolean, default=False)
    fruit_type = db.Column(db.String(50))  # Berry, Nut, etc.
    fruit_color = db.Column(db.String(50))
    
    # Growth pattern
    growth_pattern = db.Column(db.String(50))  # Upright, Spreading, etc.
    growth_rate = db.Column(db.String(20))  # Slow, Medium, Fast
    
    # Environmental preferences
    sunlight_preference = db.Column(db.String(50))  # Full sun, Partial shade, etc.
    soil_preference = db.Column(db.String(50))  # Well-drained, Clay, etc.
    moisture_preference = db.Column(db.String(50))  # Dry, Moist, etc.
    hardiness_zone = db.Column(db.String(20))  # USDA zones

# UserPlant model for storing users' saved plants
class UserPlant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    nickname = db.Column(db.String(50))
    notes = db.Column(db.Text)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

# DailyFeature model for featured plants
class DailyFeature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    feature_date = db.Column(db.Date, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
