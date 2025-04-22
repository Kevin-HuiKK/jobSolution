from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from flask_babel import lazy_gettext as _l
from app.models import User

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), 
        validators=[DataRequired(), EqualTo('password')])
    
    # Personal Information
    name = StringField(_l('Full Name'), validators=[DataRequired()])
    gender = SelectField(_l('Gender'), 
        choices=[('male', _l('Male')), ('female', _l('Female'))],
        validators=[DataRequired()])
    age = IntegerField(_l('Age'), validators=[DataRequired()])
    phone = StringField(_l('Phone Number'), validators=[DataRequired()])
    suburb = StringField(_l('Suburb'), validators=[DataRequired()])
    
    # Visa Information
    visa_type = StringField(_l('Visa Type'), validators=[DataRequired()])
    visa_expiry = DateField(_l('Visa Expiry Date'), validators=[DataRequired()])
    
    # Driving Information
    can_drive = BooleanField(_l('Can Drive'))
    has_car = BooleanField(_l('Has Car'))
    available_start_date = DateField(_l('Available Start Date'), validators=[DataRequired()])
    
    # Language Skills
    english_speaking = BooleanField(_l('Can Speak English'))
    english_writing = BooleanField(_l('Can Write English'))
    
    # Work Experience
    forklift_license = BooleanField(_l('Has Forklift License'))
    forklift_experience_years = FloatField(_l('Forklift Experience (Years)'), 
        validators=[Optional()])
    warehouse_experience = BooleanField(_l('Has Warehouse Experience'))
    last_warehouse_company = StringField(_l('Last Warehouse Company'), 
        validators=[Optional()])
    
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))

class ProfileForm(FlaskForm):
    # Personal Information
    name = StringField(_l('Full Name'), validators=[DataRequired()])
    gender = SelectField(_l('Gender'), 
        choices=[('male', _l('Male')), ('female', _l('Female'))],
        validators=[DataRequired()])
    age = IntegerField(_l('Age'), validators=[DataRequired()])
    phone = StringField(_l('Phone Number'), validators=[DataRequired()])
    suburb = StringField(_l('Suburb'), validators=[DataRequired()])
    
    # Visa Information
    visa_type = StringField(_l('Visa Type'), validators=[DataRequired()])
    visa_expiry = DateField(_l('Visa Expiry Date'), validators=[DataRequired()])
    
    # Driving Information
    can_drive = BooleanField(_l('Can Drive'))
    has_car = BooleanField(_l('Has Car'))
    available_start_date = DateField(_l('Available Start Date'), validators=[DataRequired()])
    
    # Language Skills
    english_speaking = BooleanField(_l('Can Speak English'))
    english_writing = BooleanField(_l('Can Write English'))
    
    # Work Experience
    forklift_license = BooleanField(_l('Has Forklift License'))
    forklift_experience_years = FloatField(_l('Forklift Experience (Years)'), 
        validators=[Optional()])
    warehouse_experience = BooleanField(_l('Has Warehouse Experience'))
    last_warehouse_company = StringField(_l('Last Warehouse Company'), 
        validators=[Optional()])
    
    submit = SubmitField(_l('Update Profile'))

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_l('Current Password'), validators=[DataRequired()])
    password = PasswordField(_l('New Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat New Password'), 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Change Password')) 