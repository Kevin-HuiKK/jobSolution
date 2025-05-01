# Job Portal

一个基于 Flask 的双语招聘门户网站，支持中英文切换。

## 功能特点

- 用户注册和认证
- 职位发布和管理
- 简历上传和申请跟踪
- 中英文双语支持
- 管理员后台管理
- 邮件通知系统

## 系统要求

- Python 3.8+
- SQLite 3
- 虚拟环境（推荐）

## 部署步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd jobWeb
```

### 2. 创建并激活虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件并设置以下配置：

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
MAIL_SERVER=your-mail-server
```

### 5. 初始化数据库

```bash
# 创建数据库和表
python init_db.py
```

初始化后会自动创建：
- 管理员账户（用户名：admin，密码：admin）
- 示例职位数据

### 6. 运行应用

```bash
# 开发环境
flask run

export FLASK_RUN_HOST=0.0.0.0
flask run  --port=5001



测试qidong
$env:FLASK_DEBUG=1; flask run
  #后太启动
  nohup python run.py > flask.out 2>&1 &


# 生产环境
gunicorn -w 4 run:app
```

## 数据库说明

本项目使用 SQLite 数据库，数据库文件为 `app.db`。

### 数据库结构

主要表格：
- users：用户信息
- jobs：职位信息
- job_applications：职位申请记录

### 数据库管理

1. 查看数据库状态：
```bash
python check_db.py
```

2. 重置数据库：
```bash
# 删除现有数据库文件
rm app.db
# 重新初始化
python init_db.py
```

## 目录结构

```
jobWeb/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用初始化
│   ├── models.py          # 数据模型
│   ├── routes.py          # 路由
│   ├── forms.py           # 表单
│   └── templates/         # 模板文件
├── migrations/            # 数据库迁移文件
├── instance/             # 实例配置
├── uploads/              # 上传文件目录
├── logs/                 # 日志目录
├── config.py            # 配置文件
├── init_db.py           # 数据库初始化脚本
├── run.py               # 应用入口
└── requirements.txt     # 依赖包列表
```

## 常见问题

1. 数据库初始化失败
   - 确保有写入权限
   - 检查 SQLite 版本是否兼容

2. 邮件发送失败
   - 检查邮件服务器配置
   - 确认网络连接

3. 文件上传问题
   - 确保 uploads 目录存在且有写入权限
   - 检查文件大小限制

## 维护说明

1. 日志文件
   - 应用日志：`app.log`
   - 管理员操作日志：`admin.log`

2. 备份建议
   - 定期备份 `app.db`
   - 备份 `uploads` 目录

## 安全建议

1. 生产环境部署
   - 修改默认管理员密码
   - 使用强密钥
   - 启用 HTTPS
   - 配置适当的文件权限

2. 数据库安全
   - 定期备份
   - 限制数据库文件访问权限

## 技术支持

如有问题，请联系技术支持团队。 





##nginx配置更换新
server {
		listen 443 ssl;
		server_name job.topsupplier.com.au;

		ssl_certificate     D:/kevin/keys/newkeys/job.topsupplier.com.au-chain.pem;
		ssl_certificate_key D:/kevin/keys/newkeys/job.topsupplier.com.au-key.pem;

		# 强制升级 HTTP 内容到 HTTPS
		add_header Content-Security-Policy upgrade-insecure-requests;

		# 普通请求代理到后端
		location / {
			proxy_pass http://192.168.70.110:5000;  # 替换为你的实际后端服务地址

            proxy_set_header Host $host;  #正确传递域名信息
			proxy_set_header X-Forwarded-Host $http_host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;

			proxy_redirect off;
			
			# 文件上传相关配置
			proxy_connect_timeout 300s;
			proxy_send_timeout 300s;
			proxy_read_timeout 300s;

			add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
			proxy_cookie_flags session_id samesite=lax secure;
		}
		# 文件上传大小限制
		client_max_body_size 30M;
		# 启用 gzip 压缩
		gzip_types text/css text/scss text/plain text/xml application/xml application/json application/javascript;
		gzip on;
	}








-----提交v1.1
改进国际化(i18n)实现

1. 更新Babel配置 (app/__init__.py):
- 优化locale_selector配置，使用babel.init_app(app, locale_selector=get_locale)
- 改进get_locale()函数，增加浏览器语言自动检测
- 移除重复的Babel初始化代码

2. 优化语言切换显示 (app/templates/base.html):
- 使用翻译函数替换硬编码文本
- 语言选择器显示改为 {{ _('Language') }}: {{ _('Chinese') }}/{{ _('English') }}

3. 添加新的翻译条目 (app/translations/zh/LC_MESSAGES/messages.po):
- 新增"Chinese"和"English"的中文翻译
- 重新编译翻译文件(.mo)

4. 代码优化:
- 统一使用g.language进行语言状态管理
- 保留动态内容（如职位标题）的双语切换逻辑
- 移除冗余的语言判断代码

技术细节：
- 使用Flask-Babel的_()函数处理静态文本翻译
- 保留数据库存储的双语内容（如job.title_zh）的条件判断
- 优化语言切换的用户体验