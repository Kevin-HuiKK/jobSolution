import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'zh']
    BABEL_DEFAULT_LOCALE = 'en'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Gmail邮件服务器设置
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your.email@gmail.com'  # 替换为你的Gmail邮箱
    MAIL_PASSWORD = 'your-app-specific-password'  # 替换为你的应用专用密码
    ADMINS = ['your.email@gmail.com']  # 使用相同的Gmail邮箱

    # 注意：要使用Gmail发送邮件，你需要：
    # 1. 在Gmail账户中开启"两步验证"
    # 2. 生成"应用专用密码"
    # 3. 使用应用专用密码作为MAIL_PASSWORD 