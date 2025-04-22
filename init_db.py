from app import create_app, db
from app.models import User

app = create_app()

def init_db():
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        # 检查是否已存在管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # 创建管理员用户
            admin = User(
                username='admin',
                email='admin@example.com',
                name='Administrator',
                is_admin=True
            )
            admin.set_password('admin')  # 设置默认密码
            db.session.add(admin)
            db.session.commit()
            print('Created admin user: admin/admin')
        else:
            print('Admin user already exists')

if __name__ == '__main__':
    init_db() 