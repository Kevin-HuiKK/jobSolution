from flask import Flask, request, session, current_app, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, _
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config
import re
import os
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
babel = Babel()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()

def nl2br(value):
    return value.replace('\n', '<br>') if value else ''

def get_locale():
    if 'language' not in session:
        session['language'] = request.accept_languages.best_match(['zh', 'en']) or 'en'
    return session['language']

# 添加请求钩子
def register_before_request(app):
    @app.before_request
    def before_request():
        g.language = session.get('language', 'en')
        app.logger.debug(f"设置当前请求的语言: g.language = {g.language}")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 配置日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # 修改日志处理配置
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240,
        backupCount=10,
        delay=True,  # 延迟创建文件，直到第一次写入
        encoding='utf-8'  # 明确指定编码
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)  # 将日志级别改为INFO，减少不必要的DEBUG信息
    
    # 添加控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    console_handler.setLevel(logging.INFO)
    
    # 配置应用日志
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('应用启动')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    moment.init_app(app)
    bootstrap.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = _('Please log in to access this page.')

    # 注册自定义过滤器
    app.jinja_env.filters['nl2br'] = nl2br

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # 注册请求钩子
    register_before_request(app)
    
    return app

from app import models 