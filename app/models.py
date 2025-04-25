from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    # 个人资料相关字段
    about_me = db.Column(db.Text)  # 修改为 Text 类型，不限制长度
    avatar = db.Column(db.String(255))  # 增加长度到255
    website = db.Column(db.String(120))  # 新增：个人网站
    social_media = db.Column(db.JSON)    # 新增：社交媒体链接
    skills = db.Column(db.JSON)          # 新增：技能列表
    interests = db.Column(db.Text)       # 新增：兴趣爱好
    
    # 文件存储相关
    resume_path = db.Column(db.String(255))  # 保持不变
    certificates_path = db.Column(db.JSON)    # 新增：证书文件路径
    
    # 时间相关
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 新增：账户创建时间
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
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

    # 检查是否为管理员
    @property
    def is_admin(self):
        return self.username == 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    title_zh = db.Column(db.String(120))
    description = db.Column(db.Text, nullable=False)
    description_zh = db.Column(db.Text)
    location = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    headcount = db.Column(db.String(20))  # 可以是数字或'any'
    current_headcount = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    applications = db.relationship('JobApplication', backref='job', lazy='dynamic')

    def get_headcount_display(self):
        return self.headcount if self.headcount else 'any'

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))