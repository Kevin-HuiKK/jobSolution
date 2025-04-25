from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from flask_babel import _
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   filename='app.log',
                   filemode='a')
logger = logging.getLogger(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 直接检查用户名是否为 admin
        if not current_user.is_authenticated:
            flash(_('You need to be logged in to access this page.'))
            logger.warning(f"未登录用户尝试访问管理页面")
            return redirect(url_for('auth.login'))
        
        # 记录用户尝试访问
        logger.info(f"用户 {current_user.username} 尝试访问管理页面")
        
        # admin 用户自动拥有权限，或者检查 is_admin 属性
        if current_user.username != 'admin' and not current_user.is_admin:
            flash(_('You need to be an administrator to access this page.'))
            logger.warning(f"非管理员用户 {current_user.username} 尝试访问管理页面")
            return redirect(url_for('main.index'))
        
        logger.info(f"管理员用户 {current_user.username} 成功访问管理页面")
        return f(*args, **kwargs)
    return decorated_function 