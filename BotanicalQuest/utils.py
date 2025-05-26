from datetime import date, datetime, timedelta
import random
import os
import uuid
from werkzeug.utils import secure_filename
from app import db
from models import Plant, PlantCharacteristic, DailyFeature

def save_uploaded_file(file, directory='uploads'):
    """
    Save an uploaded file to the specified directory with a unique filename.
    
    Args:
        file: The file object from the request
        directory: The subdirectory in static/ to save the file (default: 'uploads')
        
    Returns:
        str: The relative URL path to the saved file
    """
    if not file:
        return None
    
    # Create a unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Ensure directory exists
    upload_dir = os.path.join('static', directory)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Save the file
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)
    
    # Return the URL relative path
    return f"/{file_path}"

def identify_plants(criteria):
    """
    Identify plants based on the given criteria.
    
    Args:
        criteria (dict): Dictionary containing plant identification criteria
        
    Returns:
        list: List of plants matching the criteria
    """
    query = db.session.query(Plant).join(PlantCharacteristic)
    
    # Apply filters based on user input
    if 'height_range' in criteria:
        height = criteria['height_range']
        if height == 'small':
            query = query.filter(PlantCharacteristic.max_height < 100)
        elif height == 'medium':
            query = query.filter(PlantCharacteristic.min_height >= 100, 
                                PlantCharacteristic.max_height <= 300)
        elif height == 'tall':
            query = query.filter(PlantCharacteristic.min_height >= 300, 
                                PlantCharacteristic.max_height <= 1000)
        elif height == 'very_tall':
            query = query.filter(PlantCharacteristic.min_height > 1000)
    
    if 'geographic_location' in criteria and criteria['geographic_location'] != 'global':
        # Simple text matching for location
        query = query.filter(PlantCharacteristic.geographic_location.ilike(
            f"%{criteria['geographic_location']}%"
        ))
    
    if 'has_flowers' in criteria:
        has_flowers = criteria['has_flowers'] == 'yes'
        query = query.filter(PlantCharacteristic.has_flowers == has_flowers)
        
        if has_flowers and 'flower_color' in criteria and criteria['flower_color'] != '':
            query = query.filter(PlantCharacteristic.flower_color.ilike(
                f"%{criteria['flower_color']}%"
            ))
    
    if 'leaf_shape' in criteria and criteria['leaf_shape'] != '':
        query = query.filter(PlantCharacteristic.leaf_shape.ilike(
            f"%{criteria['leaf_shape']}%"
        ))
    
    if 'leaf_arrangement' in criteria and criteria['leaf_arrangement'] != '':
        query = query.filter(PlantCharacteristic.leaf_arrangement.ilike(
            f"%{criteria['leaf_arrangement']}%"
        ))
    
    if 'bark_texture' in criteria and criteria['bark_texture'] not in ('', 'na'):
        query = query.filter(PlantCharacteristic.bark_texture.ilike(
            f"%{criteria['bark_texture']}%"
        ))
    
    if 'deciduous' in criteria:
        deciduous = criteria['deciduous'] == 'yes'
        query = query.filter(PlantCharacteristic.deciduous == deciduous)
    
    if 'has_fruit' in criteria:
        has_fruit = criteria['has_fruit'] == 'yes'
        query = query.filter(PlantCharacteristic.has_fruit == has_fruit)
        
        if has_fruit and 'fruit_type' in criteria and criteria['fruit_type'] != '':
            query = query.filter(PlantCharacteristic.fruit_type.ilike(
                f"%{criteria['fruit_type']}%"
            ))
    
    if 'growth_pattern' in criteria and criteria['growth_pattern'] != '':
        query = query.filter(PlantCharacteristic.growth_pattern.ilike(
            f"%{criteria['growth_pattern']}%"
        ))
    
    if 'sunlight_preference' in criteria:
        if criteria['sunlight_preference'] == 'full_sun':
            query = query.filter(PlantCharacteristic.sunlight_preference.ilike("%full sun%"))
        elif criteria['sunlight_preference'] == 'partial_shade':
            query = query.filter(PlantCharacteristic.sunlight_preference.ilike("%partial%"))
        elif criteria['sunlight_preference'] == 'full_shade':
            query = query.filter(PlantCharacteristic.sunlight_preference.ilike("%shade%"))
    
    # Get results
    results = query.all()
    
    return results

def get_or_create_daily_feature():
    """
    Get the daily featured plant. If there's no feature for today, create one.
    
    Returns:
        DailyFeature: The daily feature object
    """
    today = date.today()
    
    # Try to get today's feature
    feature = DailyFeature.query.filter_by(feature_date=today).first()
    
    # If no feature exists for today, create one
    if not feature:
        # Get a random plant
        plants = Plant.query.all()
        if plants:
            plant = random.choice(plants)
            
            # Create a new feature
            feature = DailyFeature(
                plant_id=plant.id,
                feature_date=today,
                title=f"Featured Plant: {plant.common_name}",
                description=f"Learn about the beautiful {plant.common_name} ({plant.scientific_name}), "
                           f"a {plant.plant_type} known for its distinctive characteristics and beauty in landscapes."
            )
            
            db.session.add(feature)
            db.session.commit()
    
    return feature
