from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    
    # 用户个人信息
    name = db.Column(db.String(64))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    suburb = db.Column(db.String(100))
    visa_type = db.Column(db.String(50))
    visa_expiry = db.Column(db.Date)
    can_drive = db.Column(db.Boolean)
    has_car = db.Column(db.Boolean)
    available_start_date = db.Column(db.Date)
    english_speaking = db.Column(db.Boolean)
    english_writing = db.Column(db.Boolean)
    forklift_license = db.Column(db.Boolean)
    forklift_experience_years = db.Column(db.Float)
    warehouse_experience = db.Column(db.Boolean)
    last_warehouse_company = db.Column(db.String(100))
    
    applications = db.relationship('JobApplication', backref='applicant', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    title_zh = db.Column(db.String(128))  # 中文职位名称
    description = db.Column(db.Text, nullable=False)
    description_zh = db.Column(db.Text)    # 中文职位描述
    location = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    applications = db.relationship('JobApplication', backref='job', lazy='dynamic')

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 