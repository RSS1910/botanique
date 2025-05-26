from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms import SelectField, IntegerField, FloatField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class QuestionnaireForm(FlaskForm):
    # Height range
    height_range = SelectField('Height Range', choices=[
        ('', 'Select height range'),
        ('small', 'Small (< 1 meter)'),
        ('medium', 'Medium (1-3 meters)'),
        ('tall', 'Tall (3-10 meters)'),
        ('very_tall', 'Very Tall (> 10 meters)')
    ])
    
    # Geographic location
    geographic_location = SelectField('Geographic Location', choices=[
        ('', 'Select location'),
        ('north_america', 'North America'),
        ('south_america', 'South America'),
        ('europe', 'Europe'),
        ('asia', 'Asia'),
        ('africa', 'Africa'),
        ('australia', 'Australia'),
        ('global', 'Global (Found Worldwide)')
    ])
    
    # Flower characteristics
    has_flowers = SelectField('Does it have flowers?', choices=[
        ('', 'Select option'),
        ('yes', 'Yes'),
        ('no', 'No'),
        ('unknown', "I don't know")
    ])
    
    flower_color = SelectField('Flower Color', choices=[
        ('', 'Select color'),
        ('white', 'White'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('orange', 'Orange'),
        ('multi', 'Multi-colored'),
        ('na', 'Not Applicable')
    ])
    
    # Leaf characteristics
    leaf_shape = SelectField('Leaf Shape', choices=[
        ('', 'Select shape'),
        ('needle', 'Needle-like'),
        ('broad', 'Broad and flat'),
        ('heart', 'Heart-shaped'),
        ('oval', 'Oval'),
        ('lobed', 'Lobed'),
        ('compound', 'Compound'),
        ('scale', 'Scale-like'),
        ('unknown', "I don't know")
    ])
    
    leaf_arrangement = SelectField('Leaf Arrangement', choices=[
        ('', 'Select arrangement'),
        ('alternate', 'Alternate'),
        ('opposite', 'Opposite'),
        ('whorled', 'Whorled'),
        ('basal', 'Basal'),
        ('unknown', "I don't know")
    ])
    
    # Bark characteristics
    bark_texture = SelectField('Bark Texture', choices=[
        ('', 'Select texture'),
        ('smooth', 'Smooth'),
        ('rough', 'Rough'),
        ('peeling', 'Peeling'),
        ('furrowed', 'Furrowed/Ridged'),
        ('unknown', "I don't know"),
        ('na', 'Not Applicable')
    ])
    
    # Seasonal changes
    deciduous = SelectField('Is it deciduous (loses leaves seasonally)?', choices=[
        ('', 'Select option'),
        ('yes', 'Yes (Deciduous)'),
        ('no', 'No (Evergreen)'),
        ('unknown', "I don't know")
    ])
    
    # Fruit characteristics
    has_fruit = SelectField('Does it have visible fruits or seeds?', choices=[
        ('', 'Select option'),
        ('yes', 'Yes'),
        ('no', 'No'),
        ('unknown', "I don't know")
    ])
    
    fruit_type = SelectField('Fruit Type', choices=[
        ('', 'Select type'),
        ('berry', 'Berry'),
        ('nut', 'Nut'),
        ('pod', 'Pod'),
        ('capsule', 'Capsule'),
        ('cone', 'Cone'),
        ('samara', 'Samara (winged)'),
        ('drupe', 'Drupe (stone fruit)'),
        ('unknown', "I don't know"),
        ('na', 'Not Applicable')
    ])
    
    # Growth pattern
    growth_pattern = SelectField('Growth Pattern', choices=[
        ('', 'Select pattern'),
        ('upright', 'Upright/Erect'),
        ('spreading', 'Spreading'),
        ('climbing', 'Climbing/Vining'),
        ('rounded', 'Rounded'),
        ('weeping', 'Weeping'),
        ('unknown', "I don't know")
    ])
    
    # Environmental preferences
    sunlight_preference = SelectField('Sunlight Preference', choices=[
        ('', 'Select preference'),
        ('full_sun', 'Full Sun'),
        ('partial_shade', 'Partial Shade'),
        ('full_shade', 'Full Shade'),
        ('unknown', "I don't know")
    ])
    
    # Submit button
    submit = SubmitField('Identify Plant')

class AddPlantForm(FlaskForm):
    common_name = StringField('Common Name', validators=[DataRequired()])
    scientific_name = StringField('Scientific Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    care_instructions = TextAreaField('Care Instructions')
    plant_type = SelectField('Plant Type', choices=[
        ('tree', 'Tree'),
        ('shrub', 'Shrub'),
        ('flower', 'Flower'),
        ('grass', 'Grass'),
        ('fern', 'Fern'),
        ('succulent', 'Succulent'),
        ('vine', 'Vine'),
        ('herb', 'Herb')
    ])
    image_url = StringField('Image URL')
    image_upload = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    
    # Characteristics
    min_height = IntegerField('Minimum Height (cm)', validators=[Optional()])
    max_height = IntegerField('Maximum Height (cm)', validators=[Optional()])
    geographic_location = StringField('Geographic Location')
    has_flowers = BooleanField('Has Flowers')
    flower_color = StringField('Flower Color')
    flowering_season = StringField('Flowering Season')
    leaf_shape = StringField('Leaf Shape')
    leaf_arrangement = StringField('Leaf Arrangement')
    leaf_color = StringField('Leaf Color')
    bark_texture = StringField('Bark Texture')
    deciduous = BooleanField('Deciduous')
    fall_color = StringField('Fall Color')
    has_fruit = BooleanField('Has Fruit')
    fruit_type = StringField('Fruit Type')
    fruit_color = StringField('Fruit Color')
    growth_pattern = StringField('Growth Pattern')
    growth_rate = SelectField('Growth Rate', choices=[
        ('', 'Select rate'),
        ('slow', 'Slow'),
        ('medium', 'Medium'),
        ('fast', 'Fast')
    ])
    sunlight_preference = StringField('Sunlight Preference')
    soil_preference = StringField('Soil Preference')
    moisture_preference = StringField('Moisture Preference')
    hardiness_zone = StringField('Hardiness Zone')
    
    submit = SubmitField('Add Plant')

class EditPlantForm(FlaskForm):
    common_name = StringField('Common Name', validators=[DataRequired()])
    scientific_name = StringField('Scientific Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    care_instructions = TextAreaField('Care Instructions')
    plant_type = SelectField('Plant Type', choices=[
        ('tree', 'Tree'),
        ('shrub', 'Shrub'),
        ('flower', 'Flower'),
        ('grass', 'Grass'),
        ('fern', 'Fern'),
        ('succulent', 'Succulent'),
        ('vine', 'Vine'),
        ('herb', 'Herb')
    ])
    image_url = StringField('Image URL')
    image_upload = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    
    # Characteristics fields (same as AddPlantForm)
    min_height = IntegerField('Minimum Height (cm)', validators=[Optional()])
    max_height = IntegerField('Maximum Height (cm)', validators=[Optional()])
    geographic_location = StringField('Geographic Location')
    has_flowers = BooleanField('Has Flowers')
    flower_color = StringField('Flower Color')
    flowering_season = StringField('Flowering Season')
    leaf_shape = StringField('Leaf Shape')
    leaf_arrangement = StringField('Leaf Arrangement')
    leaf_color = StringField('Leaf Color')
    bark_texture = StringField('Bark Texture')
    deciduous = BooleanField('Deciduous')
    fall_color = StringField('Fall Color')
    has_fruit = BooleanField('Has Fruit')
    fruit_type = StringField('Fruit Type')
    fruit_color = StringField('Fruit Color')
    growth_pattern = StringField('Growth Pattern')
    growth_rate = SelectField('Growth Rate', choices=[
        ('', 'Select rate'),
        ('slow', 'Slow'),
        ('medium', 'Medium'),
        ('fast', 'Fast')
    ])
    sunlight_preference = StringField('Sunlight Preference')
    soil_preference = StringField('Soil Preference')
    moisture_preference = StringField('Moisture Preference')
    hardiness_zone = StringField('Hardiness Zone')
    
    submit = SubmitField('Update Plant')

class DailyFeatureForm(FlaskForm):
    plant_id = SelectField('Plant', coerce=int, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Feature')

class UserPlantForm(FlaskForm):
    nickname = StringField('Nickname', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Plant')
    
class SearchForm(FlaskForm):
    query = StringField('Search for plants by name', validators=[DataRequired()])
    submit = SubmitField('Search')
