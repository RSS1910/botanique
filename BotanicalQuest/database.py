from app import db
from models import User, Plant, PlantCharacteristic, DailyFeature
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta
import random

def initialize_database():
    """Initialize the database with default data if tables are empty."""
    
    # Check if there are any users
    if User.query.count() == 0:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('adminpass')
        db.session.add(admin)
        
        # Create some sample plants
        sample_plants = [
            {
                'common_name': 'Red Maple',
                'scientific_name': 'Acer rubrum',
                'description': 'The red maple is a deciduous tree native to eastern North America, known for its vibrant red foliage in autumn.',
                'care_instructions': 'Plant in full sun to partial shade. Prefers moist, well-drained soils but can adapt to various conditions.',
                'plant_type': 'tree',
                'image_url': 'https://cdn.pixabay.com/photo/2018/10/10/11/38/maple-3736887_1280.jpg',
                'characteristics': {
                    'min_height': 1000,
                    'max_height': 2500,
                    'geographic_location': 'North America',
                    'has_flowers': True,
                    'flower_color': 'red',
                    'flowering_season': 'Spring',
                    'leaf_shape': 'lobed',
                    'leaf_arrangement': 'opposite',
                    'leaf_color': 'green',
                    'bark_texture': 'smooth',
                    'deciduous': True,
                    'fall_color': 'red',
                    'has_fruit': True,
                    'fruit_type': 'samara',
                    'fruit_color': 'red',
                    'growth_pattern': 'rounded',
                    'growth_rate': 'medium',
                    'sunlight_preference': 'Full sun to partial shade',
                    'soil_preference': 'Well-drained',
                    'moisture_preference': 'Moist',
                    'hardiness_zone': '3-9'
                }
            },
            {
                'common_name': 'White Oak',
                'scientific_name': 'Quercus alba',
                'description': 'White oak is a long-lived, slow-growing tree native to eastern North America, valued for its strong wood and distinctive lobed leaves.',
                'care_instructions': 'Plant in full sun. Prefers well-drained, slightly acidic soil but is adaptable to various soil types.',
                'plant_type': 'tree',
                'image_url': 'https://cdn.pixabay.com/photo/2018/04/26/12/14/tree-3351451_1280.jpg',
                'characteristics': {
                    'min_height': 1500,
                    'max_height': 3000,
                    'geographic_location': 'North America',
                    'has_flowers': True,
                    'flower_color': 'yellow',
                    'flowering_season': 'Spring',
                    'leaf_shape': 'lobed',
                    'leaf_arrangement': 'alternate',
                    'leaf_color': 'green',
                    'bark_texture': 'furrowed',
                    'deciduous': True,
                    'fall_color': 'brown',
                    'has_fruit': True,
                    'fruit_type': 'nut',
                    'fruit_color': 'brown',
                    'growth_pattern': 'spreading',
                    'growth_rate': 'slow',
                    'sunlight_preference': 'Full sun',
                    'soil_preference': 'Well-drained',
                    'moisture_preference': 'Medium',
                    'hardiness_zone': '3-9'
                }
            },
            {
                'common_name': 'Eastern White Pine',
                'scientific_name': 'Pinus strobus',
                'description': 'The eastern white pine is a large coniferous tree native to eastern North America, known for its long, soft needles and tall, straight growth.',
                'care_instructions': 'Plant in full sun to partial shade. Prefers moist, well-drained, slightly acidic soil.',
                'plant_type': 'tree',
                'image_url': 'https://cdn.pixabay.com/photo/2018/02/09/21/46/tree-3142553_1280.jpg',
                'characteristics': {
                    'min_height': 2000,
                    'max_height': 5000,
                    'geographic_location': 'North America',
                    'has_flowers': False,
                    'leaf_shape': 'needle',
                    'leaf_arrangement': 'fascicle',
                    'leaf_color': 'blue-green',
                    'bark_texture': 'smooth',
                    'deciduous': False,
                    'has_fruit': True,
                    'fruit_type': 'cone',
                    'fruit_color': 'brown',
                    'growth_pattern': 'upright',
                    'growth_rate': 'fast',
                    'sunlight_preference': 'Full sun to partial shade',
                    'soil_preference': 'Well-drained',
                    'moisture_preference': 'Medium',
                    'hardiness_zone': '3-8'
                }
            },
            {
                'common_name': 'Lavender',
                'scientific_name': 'Lavandula',
                'description': 'Lavender is a fragrant herb with purple flowers, widely cultivated for its essential oils used in aromatherapy and perfumes.',
                'care_instructions': 'Plant in full sun. Requires well-drained soil and moderate watering. Prune after flowering to maintain shape.',
                'plant_type': 'herb',
                'image_url': 'https://cdn.pixabay.com/photo/2015/07/05/10/18/lavender-832415_1280.jpg',
                'characteristics': {
                    'min_height': 30,
                    'max_height': 90,
                    'geographic_location': 'Europe',
                    'has_flowers': True,
                    'flower_color': 'purple',
                    'flowering_season': 'Summer',
                    'leaf_shape': 'narrow',
                    'leaf_arrangement': 'opposite',
                    'leaf_color': 'gray-green',
                    'bark_texture': 'na',
                    'deciduous': False,
                    'has_fruit': False,
                    'growth_pattern': 'rounded',
                    'growth_rate': 'medium',
                    'sunlight_preference': 'Full sun',
                    'soil_preference': 'Well-drained',
                    'moisture_preference': 'Dry',
                    'hardiness_zone': '5-9'
                }
            },
            {
                'common_name': 'Boston Fern',
                'scientific_name': 'Nephrolepis exaltata',
                'description': 'The Boston fern is a popular houseplant known for its graceful, arching fronds and air-purifying qualities.',
                'care_instructions': 'Keep in indirect light. Maintain high humidity and keep soil consistently moist but not waterlogged.',
                'plant_type': 'fern',
                'image_url': 'https://cdn.pixabay.com/photo/2018/03/03/18/33/fern-3196491_1280.jpg',
                'characteristics': {
                    'min_height': 30,
                    'max_height': 90,
                    'geographic_location': 'Global',
                    'has_flowers': False,
                    'leaf_shape': 'compound',
                    'leaf_arrangement': 'alternate',
                    'leaf_color': 'green',
                    'bark_texture': 'na',
                    'deciduous': False,
                    'has_fruit': False,
                    'growth_pattern': 'spreading',
                    'growth_rate': 'medium',
                    'sunlight_preference': 'Partial shade',
                    'soil_preference': 'Rich, organic',
                    'moisture_preference': 'Moist',
                    'hardiness_zone': '9-11'
                }
            }
        ]
        
        # Add plants to database
        for plant_data in sample_plants:
            # Create plant
            plant = Plant(
                common_name=plant_data['common_name'],
                scientific_name=plant_data['scientific_name'],
                description=plant_data['description'],
                care_instructions=plant_data['care_instructions'],
                plant_type=plant_data['plant_type'],
                image_url=plant_data['image_url']
            )
            db.session.add(plant)
            db.session.flush()  # Get plant ID
            
            # Create plant characteristics
            char_data = plant_data['characteristics']
            characteristic = PlantCharacteristic(
                plant_id=plant.id,
                **char_data
            )
            db.session.add(characteristic)
        
        # Create a daily feature
        if Plant.query.count() > 0:
            # Get a random plant for the feature
            plant = Plant.query.first()
            
            today = date.today()
            feature = DailyFeature(
                plant_id=plant.id,
                feature_date=today,
                title=f"Featured Plant: {plant.common_name}",
                description=f"Learn about the beautiful {plant.common_name} ({plant.scientific_name}), "
                           f"a {plant.plant_type} known for its distinctive characteristics and beauty in landscapes."
            )
            db.session.add(feature)
        
        db.session.commit()
        print("Database initialized with sample data.")
    else:
        print("Database already contains data. Skipping initialization.")
