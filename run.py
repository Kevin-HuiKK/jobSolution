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
    logger.info("应用程序启动")
    # 设置 host='0.0.0.0' 允许外部访问
    # debug=True 开启调试模式，生产环境请设置为 False
    app.run(host='0.0.0.0', port=5000, debug=True) 