# 招聘管理系统

这是一个基于Flask的招聘管理系统，支持求职者注册、投递简历和雇主发布职位等功能。

## 功能特点

- 用户注册和登录
- 个人信息管理
- 职位发布和管理
- 简历投递
- 中英文双语支持

## 安装和运行

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 初始化数据库：
```bash
flask db upgrade
```

4. 运行应用：
```bash
flask run
```

## 技术栈

- 后端：Python Flask
- 数据库：SQLite
- 前端：HTML, JavaScript, Bootstrap
- 国际化：Flask-Babel 