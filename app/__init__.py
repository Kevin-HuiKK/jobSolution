from flask import Flask, request, session, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_mail import Mail
from config import Config
import re

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
mail = Mail()

def nl2br(value):
    return value.replace('\n', '<br>') if value else ''

def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'

    # 注册自定义过滤器
    app.jinja_env.filters['nl2br'] = nl2br

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 初始化Babel
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    babel.init_app(app)
    babel.locale_selector_func = get_locale

    return app

from app import models 