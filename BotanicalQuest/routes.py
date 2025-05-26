from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from datetime import datetime, date
import random
from sqlalchemy import or_

from app import app, db
from forms import (LoginForm, RegistrationForm, QuestionnaireForm, AddPlantForm,
                  EditPlantForm, DailyFeatureForm, UserPlantForm, SearchForm)
from models import User, Plant, PlantCharacteristic, UserPlant, DailyFeature
from utils import identify_plants, get_or_create_daily_feature, save_uploaded_file

@app.route('/')
def index():
    # Get daily featured plant
    daily_feature = get_or_create_daily_feature()
    
    # Get counters for statistics
    plant_count = Plant.query.count()
    user_count = User.query.count()
    
    return render_template('index.html', 
                           daily_feature=daily_feature,
                           plant_count=plant_count,
                           user_count=user_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
            
        flash('You have been logged in successfully!', 'success')
        return redirect(next_page)
    
    return render_template('login.html', form=form, title='Sign In')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Make the first user an admin
        if User.query.count() == 0:
            user.is_admin = True
            
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form, title='Register')

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    
    if form.validate_on_submit() or request.args.get('query'):
        # Get search query from either form submission or URL parameter
        query = form.query.data if form.validate_on_submit() else request.args.get('query')
        
        # Search for plants matching the query in common_name or scientific_name
        results = Plant.query.filter(
            or_(
                Plant.common_name.ilike(f'%{query}%'),
                Plant.scientific_name.ilike(f'%{query}%')
            )
        ).all()
        
        return render_template('search_results.html', 
                             plants=results,
                             query=query,
                             form=form,
                             title='Search Results')
    
    # Get random popular plants for display on search page
    popular_plants = Plant.query.order_by(Plant.id).limit(6).all()
    if len(popular_plants) > 3:
        random.shuffle(popular_plants)
        popular_plants = popular_plants[:3]  # Limit to 3 random plants
    
    return render_template('search.html', form=form, plants=popular_plants, title='Search Plants')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = QuestionnaireForm()
    
    if form.validate_on_submit():
        # Get form data for plant identification
        criteria = {
            'height_range': form.height_range.data,
            'geographic_location': form.geographic_location.data,
            'has_flowers': form.has_flowers.data,
            'flower_color': form.flower_color.data,
            'leaf_shape': form.leaf_shape.data,
            'leaf_arrangement': form.leaf_arrangement.data,
            'bark_texture': form.bark_texture.data,
            'deciduous': form.deciduous.data,
            'has_fruit': form.has_fruit.data,
            'fruit_type': form.fruit_type.data,
            'growth_pattern': form.growth_pattern.data,
            'sunlight_preference': form.sunlight_preference.data
        }
        
        # Filter out empty or 'unknown' responses
        criteria = {k: v for k, v in criteria.items() if v and v != 'unknown' and v != 'na'}
        
        # Identify plants based on criteria
        matched_plants = identify_plants(criteria)
        
        return render_template('results.html', 
                               plants=matched_plants, 
                               criteria=criteria,
                               title='Identification Results')
    
    return render_template('questionnaire.html', form=form, title='Plant Identification')

@app.route('/plant/<int:plant_id>')
def plant_details(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    characteristic = plant.characteristics.first()
    
    # Check if user has saved this plant
    saved = False
    if current_user.is_authenticated:
        saved = UserPlant.query.filter_by(user_id=current_user.id, plant_id=plant.id).first() is not None
    
    return render_template('plant_details.html', 
                           plant=plant, 
                           characteristic=characteristic,
                           saved=saved,
                           title=plant.common_name)

@app.route('/dashboard')
@login_required
def user_dashboard():
    saved_plants = UserPlant.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', 
                           saved_plants=saved_plants, 
                           title='My Plant Library')

@app.route('/save_plant/<int:plant_id>', methods=['GET', 'POST'])
@login_required
def save_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    # Check if plant is already saved
    existing = UserPlant.query.filter_by(user_id=current_user.id, plant_id=plant.id).first()
    if existing:
        flash(f'{plant.common_name} is already in your library!', 'info')
        return redirect(url_for('plant_details', plant_id=plant.id))
    
    form = UserPlantForm()
    
    if form.validate_on_submit():
        user_plant = UserPlant(
            user_id=current_user.id,
            plant_id=plant.id,
            nickname=form.nickname.data,
            notes=form.notes.data
        )
        
        db.session.add(user_plant)
        db.session.commit()
        
        flash(f'{plant.common_name} has been added to your library!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('save_plant.html', 
                           form=form, 
                           plant=plant,
                           title=f'Save {plant.common_name}')

@app.route('/remove_plant/<int:plant_id>', methods=['POST'])
@login_required
def remove_plant(plant_id):
    user_plant = UserPlant.query.filter_by(user_id=current_user.id, plant_id=plant_id).first_or_404()
    plant_name = user_plant.plant.common_name
    
    db.session.delete(user_plant)
    db.session.commit()
    
    flash(f'{plant_name} has been removed from your library.', 'success')
    return redirect(url_for('user_dashboard'))

# Admin routes
@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    # Get counts for admin dashboard
    plant_count = Plant.query.count()
    user_count = User.query.count()
    
    return render_template('admin_panel.html', 
                           plant_count=plant_count,
                           user_count=user_count,
                           title='Admin Panel')

@app.route('/admin/plants')
@login_required
def admin_plants():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    plants = Plant.query.all()
    return render_template('admin_plants.html', plants=plants, title='Manage Plants')

@app.route('/admin/plants/add', methods=['GET', 'POST'])
@login_required
def admin_add_plant():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    form = AddPlantForm()
    
    if form.validate_on_submit():
        # Handle image upload if provided
        image_url = form.image_url.data
        if form.image_upload.data:
            uploaded_image_url = save_uploaded_file(form.image_upload.data, directory='uploads/plants')
            if uploaded_image_url:
                image_url = uploaded_image_url
        
        # Create new plant
        plant = Plant(
            common_name=form.common_name.data,
            scientific_name=form.scientific_name.data,
            description=form.description.data,
            care_instructions=form.care_instructions.data,
            plant_type=form.plant_type.data,
            image_url=image_url
        )
        
        db.session.add(plant)
        db.session.flush()  # Get plant ID without committing
        
        # Create plant characteristics
        characteristic = PlantCharacteristic(
            plant_id=plant.id,
            min_height=form.min_height.data,
            max_height=form.max_height.data,
            geographic_location=form.geographic_location.data,
            has_flowers=form.has_flowers.data,
            flower_color=form.flower_color.data if form.has_flowers.data else None,
            flowering_season=form.flowering_season.data if form.has_flowers.data else None,
            leaf_shape=form.leaf_shape.data,
            leaf_arrangement=form.leaf_arrangement.data,
            leaf_color=form.leaf_color.data,
            bark_texture=form.bark_texture.data,
            deciduous=form.deciduous.data,
            fall_color=form.fall_color.data if form.deciduous.data else None,
            has_fruit=form.has_fruit.data,
            fruit_type=form.fruit_type.data if form.has_fruit.data else None,
            fruit_color=form.fruit_color.data if form.has_fruit.data else None,
            growth_pattern=form.growth_pattern.data,
            growth_rate=form.growth_rate.data,
            sunlight_preference=form.sunlight_preference.data,
            soil_preference=form.soil_preference.data,
            moisture_preference=form.moisture_preference.data,
            hardiness_zone=form.hardiness_zone.data
        )
        
        db.session.add(characteristic)
        db.session.commit()
        
        flash(f'Plant "{form.common_name.data}" has been added successfully!', 'success')
        return redirect(url_for('admin_plants'))
    
    return render_template('admin_add_plant.html', form=form, title='Add New Plant')

@app.route('/admin/plants/edit/<int:plant_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_plant(plant_id):
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    plant = Plant.query.get_or_404(plant_id)
    characteristic = PlantCharacteristic.query.filter_by(plant_id=plant.id).first()
    
    if not characteristic:
        characteristic = PlantCharacteristic(plant_id=plant.id)
        db.session.add(characteristic)
        db.session.commit()
    
    form = EditPlantForm()
    
    if request.method == 'GET':
        # Populate form with existing data
        form.common_name.data = plant.common_name
        form.scientific_name.data = plant.scientific_name
        form.description.data = plant.description
        form.care_instructions.data = plant.care_instructions
        form.plant_type.data = plant.plant_type
        form.image_url.data = plant.image_url
        
        # Populate characteristics
        form.min_height.data = characteristic.min_height
        form.max_height.data = characteristic.max_height
        form.geographic_location.data = characteristic.geographic_location
        form.has_flowers.data = characteristic.has_flowers
        form.flower_color.data = characteristic.flower_color
        form.flowering_season.data = characteristic.flowering_season
        form.leaf_shape.data = characteristic.leaf_shape
        form.leaf_arrangement.data = characteristic.leaf_arrangement
        form.leaf_color.data = characteristic.leaf_color
        form.bark_texture.data = characteristic.bark_texture
        form.deciduous.data = characteristic.deciduous
        form.fall_color.data = characteristic.fall_color
        form.has_fruit.data = characteristic.has_fruit
        form.fruit_type.data = characteristic.fruit_type
        form.fruit_color.data = characteristic.fruit_color
        form.growth_pattern.data = characteristic.growth_pattern
        form.growth_rate.data = characteristic.growth_rate
        form.sunlight_preference.data = characteristic.sunlight_preference
        form.soil_preference.data = characteristic.soil_preference
        form.moisture_preference.data = characteristic.moisture_preference
        form.hardiness_zone.data = characteristic.hardiness_zone
    
    if form.validate_on_submit():
        # Handle image upload if provided
        image_url = form.image_url.data
        if form.image_upload.data:
            uploaded_image_url = save_uploaded_file(form.image_upload.data, directory='uploads/plants')
            if uploaded_image_url:
                image_url = uploaded_image_url
        
        # Update plant details
        plant.common_name = form.common_name.data
        plant.scientific_name = form.scientific_name.data
        plant.description = form.description.data
        plant.care_instructions = form.care_instructions.data
        plant.plant_type = form.plant_type.data
        plant.image_url = image_url
        plant.updated_at = datetime.utcnow()
        
        # Update plant characteristics
        characteristic.min_height = form.min_height.data
        characteristic.max_height = form.max_height.data
        characteristic.geographic_location = form.geographic_location.data
        characteristic.has_flowers = form.has_flowers.data
        characteristic.flower_color = form.flower_color.data if form.has_flowers.data else None
        characteristic.flowering_season = form.flowering_season.data if form.has_flowers.data else None
        characteristic.leaf_shape = form.leaf_shape.data
        characteristic.leaf_arrangement = form.leaf_arrangement.data
        characteristic.leaf_color = form.leaf_color.data
        characteristic.bark_texture = form.bark_texture.data
        characteristic.deciduous = form.deciduous.data
        characteristic.fall_color = form.fall_color.data if form.deciduous.data else None
        characteristic.has_fruit = form.has_fruit.data
        characteristic.fruit_type = form.fruit_type.data if form.has_fruit.data else None
        characteristic.fruit_color = form.fruit_color.data if form.has_fruit.data else None
        characteristic.growth_pattern = form.growth_pattern.data
        characteristic.growth_rate = form.growth_rate.data
        characteristic.sunlight_preference = form.sunlight_preference.data
        characteristic.soil_preference = form.soil_preference.data
        characteristic.moisture_preference = form.moisture_preference.data
        characteristic.hardiness_zone = form.hardiness_zone.data
        
        db.session.commit()
        
        flash(f'Plant "{form.common_name.data}" has been updated successfully!', 'success')
        return redirect(url_for('admin_plants'))
    
    return render_template('admin_edit_plant.html', 
                           form=form, 
                           plant=plant,
                           title=f'Edit {plant.common_name}')

@app.route('/admin/plants/delete/<int:plant_id>', methods=['POST'])
@login_required
def admin_delete_plant(plant_id):
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    plant = Plant.query.get_or_404(plant_id)
    plant_name = plant.common_name
    
    db.session.delete(plant)
    db.session.commit()
    
    flash(f'Plant "{plant_name}" has been deleted successfully!', 'success')
    return redirect(url_for('admin_plants'))

@app.route('/admin/feature', methods=['GET', 'POST'])
@login_required
def admin_feature():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    
    form = DailyFeatureForm()
    
    # Populate plants for selection
    form.plant_id.choices = [(p.id, p.common_name) for p in Plant.query.order_by(Plant.common_name).all()]
    
    if form.validate_on_submit():
        # Check if there's already a feature for today
        today = date.today()
        existing = DailyFeature.query.filter_by(feature_date=today).first()
        
        if existing:
            existing.plant_id = form.plant_id.data
            existing.title = form.title.data
            existing.description = form.description.data
        else:
            feature = DailyFeature(
                plant_id=form.plant_id.data,
                feature_date=today,
                title=form.title.data,
                description=form.description.data
            )
            db.session.add(feature)
        
        db.session.commit()
        flash('Daily feature has been updated successfully!', 'success')
        return redirect(url_for('admin_panel'))
    
    # Pre-populate with today's feature if it exists
    today_feature = DailyFeature.query.filter_by(feature_date=date.today()).first()
    if today_feature and request.method == 'GET':
        form.plant_id.data = today_feature.plant_id
        form.title.data = today_feature.title
        form.description.data = today_feature.description
    
    return render_template('admin_feature.html', form=form, title='Manage Daily Feature')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
