from app import create_app, db
from app.models import User, Job, JobApplication

app = create_app()
with app.app_context():
    db.create_all()
    
    # 创建管理员用户（如果不存在）
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin')
        db.session.add(admin)
    
    # 创建一些示例工作
    jobs = [
        {
            'title': 'Warehouse Worker',
            'title_zh': '仓库工人',
            'description': 'We are looking for warehouse workers...',
            'description_zh': '我们正在招聘仓库工人...',
            'location': 'Sydney',
            'headcount': '5'
        },
        {
            'title': 'Forklift Driver',
            'title_zh': '叉车司机',
            'description': 'Experienced forklift driver needed...',
            'description_zh': '需要有经验的叉车司机...',
            'location': 'Melbourne',
            'headcount': 'any'
        }
    ]
    
    for job_data in jobs:
        job = Job.query.filter_by(title=job_data['title']).first()
        if not job:
            job = Job(**job_data)
            db.session.add(job)
    
    db.session.commit()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 