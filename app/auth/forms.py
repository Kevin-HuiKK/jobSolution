from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional, Length
from flask_babel import lazy_gettext as _l
from app.models import User
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    remember_me = BooleanField(_l('记住我'))
    submit = SubmitField(_l('登录'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    password2 = PasswordField(_l('确认密码'), validators=[DataRequired(), EqualTo('password')])
    
    # Personal Information
    name = StringField(_l('姓名'), validators=[DataRequired(), Length(max=64)])
    gender = SelectField(_l('性别'), choices=[('male', _l('男')), ('female', _l('女')), ('other', _l('其他'))],
        validators=[DataRequired()])
    age = IntegerField(_l('年龄'), validators=[DataRequired()])
    phone = StringField(_l('电话'), validators=[DataRequired(), Length(max=20)])
    suburb = StringField(_l('居住区'), validators=[DataRequired(), Length(max=100)])
    
    # Visa Information
    visa_type = StringField(_l('签证类型'), validators=[DataRequired(), Length(max=50)])
    visa_expiry = DateField(_l('签证到期日'), format='%Y-%m-%d', validators=[DataRequired()])
    
    # Driving Information
    can_drive = BooleanField(_l('有驾照'))
    has_car = BooleanField(_l('有车'))
    available_start_date = DateField(_l('可开始工作日期'), format='%Y-%m-%d', validators=[DataRequired()])
    
    # Language Skills
    english_speaking = BooleanField(_l('英语口语'))
    english_writing = BooleanField(_l('英语写作'))
    
    # Work Experience
    forklift_license = BooleanField(_l('叉车证'))
    forklift_experience_years = FloatField(_l('叉车工作年限'), validators=[Optional()])
    warehouse_experience = BooleanField(_l('仓库工作经验'))
    last_warehouse_company = StringField(_l('上一个仓库公司'), validators=[Length(max=100)])
    
    submit = SubmitField(_l('注册'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('该用户名已被使用，请使用其他用户名。'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('该邮箱已被注册，请使用其他邮箱。'))

class ProfileForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    age = IntegerField('Age', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    suburb = StringField('Suburb', validators=[DataRequired(), Length(max=100)])
    about_me = TextAreaField('About Me', validators=[Length(max=500)])
    
    # Visa Information
    visa_type = SelectField('Visa Type', choices=[
        ('', 'Please select visa type'),
        ('citizen', 'Australian Citizen'),
        ('pr', 'Permanent Resident'),
        ('student', 'Student Visa'),
        ('work', 'Work Visa'),
        ('whv', 'Working Holiday Visa'),
        ('other', 'Other')
    ])
    visa_expiry = DateField('Visa Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    # Driving Information
    can_drive = BooleanField('Have Driver License')
    has_car = BooleanField('Have Car')
    available_start_date = DateField('Available Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    # Language Skills
    english_speaking = BooleanField('English Speaking')
    english_writing = BooleanField('English Writing')
    
    # Work Experience
    forklift_license = BooleanField('Forklift License')
    forklift_experience_years = FloatField('Years of Forklift Experience', validators=[Optional()])
    warehouse_experience = BooleanField('Warehouse Experience')
    last_warehouse_company = StringField('Last Warehouse Company', validators=[Length(max=100)])
    
    resume = FileField('Resume', validators=[FileAllowed(['pdf', 'doc', 'docx'])])
    
    submit = SubmitField('Save Changes')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_l('当前密码'), validators=[DataRequired()])
    password = PasswordField(_l('新密码'), validators=[DataRequired()])
    password2 = PasswordField(_l('确认新密码'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('更改密码'))

class EditProfileForm(FlaskForm):
    username = StringField(_l('用户名'), validators=[DataRequired()])
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
    about_me = TextAreaField(_l('个人简介'), validators=[Length(max=500)],
                           description=_l('请介绍一下你自己（最多500字）'))
    avatar = FileField(_l('头像'), validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], _l('只允许上传jpg或png格式的图片'))
    ])
    submit = SubmitField(_l('保存修改'))

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(_l('该用户名已被使用，请使用其他用户名。'))

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError(_l('该邮箱已被注册，请使用其他邮箱。')) 