from flask import Flask, request, session, current_app, send_from_directory
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
        session['language'] = 'en'
    return session['language']

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 确保日志目录存在
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 配置日志
    file_handler = RotatingFileHandler(
        'logs/jobweb.log',
        maxBytes=10240,
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('JobWeb startup')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
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

    # 初始化Babel
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    babel.locale_selector_func = get_locale

    return app

from app import models 