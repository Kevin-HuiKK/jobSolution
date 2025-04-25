import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['zh', 'en']
    BABEL_DEFAULT_LOCALE = 'en'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 邮件服务器配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # 注意：要使用Gmail发送邮件，你需要：
    # 1. 在Gmail账户中开启"两步验证"
    # 2. 生成"应用专用密码"
    # 3. 使用应用专用密码作为MAIL_PASSWORD 

    # 邮件模板 - 英文
    EMAIL_ACCEPT_TEMPLATE_EN = '''Dear {name},

We are pleased to inform you that your application for the position of {job_title} at {company} has been accepted.

We will contact you shortly with further details.

Best regards,
{company} Team'''

    # 邮件模板 - 中文
    EMAIL_ACCEPT_TEMPLATE_ZH = '''亲爱的 {name}：

我们很高兴地通知您，您申请的 {company} 公司 {job_title} 职位已被接受。

我们将很快与您联系，提供更多详细信息。

此致
{company} 团队'''

    # 邮件模板 - 英文
    EMAIL_REJECT_TEMPLATE_EN = '''Dear {name},

Thank you for your interest in the {job_title} position at {company}.

After careful consideration, we regret to inform you that we have decided to move forward with other candidates.

We wish you the best in your job search.

Best regards,
{company} Team'''

    # 邮件模板 - 中文
    EMAIL_REJECT_TEMPLATE_ZH = '''亲爱的 {name}：

感谢您对 {company} 公司 {job_title} 职位的关注。

经过慎重考虑，我们很遗憾地通知您，我们决定继续与其他候选人进行合作。

祝您求职顺利。

此致
{company} 团队'''

    # 应用配置
    APP_ID = os.environ.get('APP_ID')

    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-password'
    MAIL_SENDER = 'noreply@jobportal.com'
    COMPANY_NAME = 'Job Portal'
    
    # 语言配置
    LANGUAGES = ['en', 'zh']
    BABEL_DEFAULT_LOCALE = 'en'
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    UPLOAD_URL_PREFIX = '/uploads'
    
    # 物理存储路径
    RESUME_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    AVATAR_FOLDER = os.path.join(UPLOAD_FOLDER, 'avatars')
    CERTIFICATE_FOLDER = os.path.join(UPLOAD_FOLDER, 'certificates')
    
    # URL 访问路径
    RESUME_URL_PREFIX = UPLOAD_URL_PREFIX + '/resumes'
    AVATAR_URL_PREFIX = UPLOAD_URL_PREFIX + '/avatars'
    CERTIFICATE_URL_PREFIX = UPLOAD_URL_PREFIX + '/certificates'
    
    # 允许的文件类型
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'doc', 'docx'}
    ALLOWED_CERTIFICATE_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    
    # 文件大小限制
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # 应用程序配置
    POSTS_PER_PAGE = 10 