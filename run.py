import os
import logging
from app import create_app, db
from app.models import User, Job, JobApplication

# 配置日志
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   filename='app.log',
                   filemode='a')
logger = logging.getLogger(__name__)

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Job': Job, 'JobApplication': JobApplication}

if __name__ == '__main__':
    # 添加应用启动日志
    logger.info("应用程序启动")
    app.run(debug=True) 