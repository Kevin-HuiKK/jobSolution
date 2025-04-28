from flask import render_template, redirect, url_for, flash, request, send_file, current_app, jsonify, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm, EditProfileForm
import traceback
import os
from app.utils import save_file, delete_file, get_file_info
from werkzeug.utils import secure_filename
import uuid
import logging
from datetime import datetime
from flask import g

# 配置日志
logger = logging.getLogger(__name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                name=form.name.data,
                gender=form.gender.data,
                age=form.age.data,
                phone=form.phone.data,
                suburb=form.suburb.data,
                visa_type=form.visa_type.data,
                visa_expiry=form.visa_expiry.data,
                can_drive=form.can_drive.data,
                has_car=form.has_car.data,
                available_start_date=form.available_start_date.data,
                english_speaking=form.english_speaking.data,
                english_writing=form.english_writing.data,
                forklift_license=form.forklift_license.data,
                forklift_experience_years=form.forklift_experience_years.data,
                warehouse_experience=form.warehouse_experience.data,
                last_warehouse_company=form.last_warehouse_company.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(_('Congratulations, you are now a registered user!'))
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            print("Registration error:", str(e))
            print(traceback.format_exc())
            flash(_('An error occurred during registration. Please try again.'))
    
    # 如果表单验证失败，显示错误信息
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}")
    
    return render_template('auth/register.html', title=_('Register'), form=form)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    logger.info(f"用户 {current_user.username} 访问个人资料页面")
    # 创建表单并用当前用户数据填充
    form = ProfileForm()
    if request.method == 'GET':
        # 在GET请求时填充表单数据
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.gender.data = current_user.gender
        form.age.data = current_user.age
        form.phone.data = current_user.phone
        form.suburb.data = current_user.suburb
        form.visa_type.data = current_user.visa_type
        form.visa_expiry.data = current_user.visa_expiry
        form.can_drive.data = current_user.can_drive
        form.has_car.data = current_user.has_car
        form.available_start_date.data = current_user.available_start_date
        form.english_speaking.data = current_user.english_speaking
        form.english_writing.data = current_user.english_writing
        form.forklift_license.data = current_user.forklift_license
        form.forklift_experience_years.data = current_user.forklift_experience_years
        form.warehouse_experience.data = current_user.warehouse_experience
        form.last_warehouse_company.data = current_user.last_warehouse_company
        form.about_me.data = current_user.about_me
        logger.info(f"已加载用户 {current_user.username} 的个人资料数据")

    if form.validate_on_submit():
        try:
            logger.info(f"用户 {current_user.username} 开始更新个人资料")
            # 更新用户数据
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.gender = form.gender.data
            current_user.age = form.age.data
            current_user.phone = form.phone.data
            current_user.suburb = form.suburb.data
            current_user.visa_type = form.visa_type.data
            current_user.visa_expiry = form.visa_expiry.data
            current_user.can_drive = form.can_drive.data
            current_user.has_car = form.has_car.data
            current_user.available_start_date = form.available_start_date.data
            current_user.english_speaking = form.english_speaking.data
            current_user.english_writing = form.english_writing.data
            current_user.forklift_license = form.forklift_license.data
            current_user.forklift_experience_years = form.forklift_experience_years.data
            current_user.warehouse_experience = form.warehouse_experience.data
            current_user.last_warehouse_company = form.last_warehouse_company.data
            current_user.about_me = form.about_me.data

            # 处理简历上传
            if form.resume.data:
                logger.info(f"用户 {current_user.username} 开始上传简历")
                try:
                    # 保存文件并获取路径
                    file_path, url_path = save_file(form.resume.data, 'resumes')
                    if file_path and url_path:
                        # 如果存在旧文件，删除它
                        if current_user.resume_path:
                            old_file = os.path.join(current_app.config['RESUME_FOLDER'], 
                                                  os.path.basename(current_user.resume_path))
                            delete_file(old_file)
                        
                        # 保存URL路径到数据库
                        current_user.resume_path = url_path
                        logger.info(f"用户 {current_user.username} 简历上传成功")
                        flash(_('Resume uploaded successfully.'), 'success')
                except Exception as e:
                    logger.error(f"简历上传错误: {str(e)}")
                    flash(_('Error uploading resume: ') + str(e), 'danger')

            db.session.commit()
            logger.info(f"用户 {current_user.username} 个人资料更新成功")
            flash(_('Your profile has been updated.'), 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新个人资料失败: {str(e)}\n{traceback.format_exc()}")
            flash(_('Error updating profile: ') + str(e), 'danger')
    
    # 获取当前简历URL（如果存在）
    resume_url = None
    if current_user.resume_path:
        resume_url = url_for('static', filename=current_user.resume_path)
        logger.info(f"用户 {current_user.username} 的简历URL: {resume_url}")
    
    return render_template('auth/profile.html', title=_('Edit Profile'), 
                         form=form, resume_url=resume_url)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.password.data)
            db.session.commit()
            flash(_('密码修改成功'), 'success')
            return redirect(url_for('main.index'))
        else:
            flash(_('当前密码错误'), 'danger')
    return render_template('auth/change_password.html', title=_('修改密码'),
                         form=form)

@bp.route('/download_resume/<int:user_id>')
@login_required
def download_resume(user_id):
    """下载用户简历"""
    user = User.query.get_or_404(user_id)
    # 检查权限：只有本人或管理员可以下载
    if not (current_user.id == user_id or current_user.is_admin):
        flash(_('You do not have permission to download this resume.'), 'danger')
        return redirect(url_for('main.index'))
    
    if not user.resume_path:
        flash(_('Resume file not found.'), 'danger')
        return redirect(url_for('main.index'))
    
    try:
        # 从URL路径获取文件名
        filename = os.path.basename(user.resume_path)
        # 构建完整的文件路径
        file_path = os.path.join(current_app.config['RESUME_FOLDER'], filename)
        
        logger.info(f"下载简历 - 用户: {user.username}")
        logger.info(f"文件路径: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            flash(_('Resume file not found on server.'), 'danger')
            return redirect(url_for('main.index'))
        
        # 如果文件名包含UUID，去掉UUID部分
        if '_' in filename:
            orig_filename = filename.split('_', 1)[1]
        else:
            orig_filename = filename
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"resume_{user.username}_{orig_filename}"
        )
    except Exception as e:
        logger.error(f"下载简历失败: {str(e)}")
        flash(_('Error downloading resume.'), 'danger')
        return redirect(url_for('main.index'))

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    from flask import current_app, g, session
    # 添加详细的调试信息
    current_app.logger.debug(f"当前会话信息: {session}")
    current_app.logger.debug(f"当前语言设置 g.language: {g.language}")
    current_app.logger.debug(f"当前请求方法: {request.method}")
    
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        if form.avatar.data:
            avatar_path = save_file(form.avatar.data, 'avatars')
            if avatar_path:
                # 删除旧头像
                if current_user.avatar and os.path.exists(os.path.join(current_app.root_path, 'static', current_user.avatar)):
                    os.remove(os.path.join(current_app.root_path, 'static', current_user.avatar))
                current_user.avatar = avatar_path
        
        db.session.commit()
        flash(_('个人资料已更新'), 'success')
        return redirect(url_for('auth.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('auth/edit_profile.html', title=_('编辑资料'),
                         form=form)

@bp.route('/delete_resume/<int:user_id>', methods=['POST'])
@login_required
def delete_resume(user_id):
    """删除用户简历"""
    user = User.query.get_or_404(user_id)
    if not (current_user.id == user_id or current_user.is_admin):
        return jsonify({'success': False, 'message': _('Permission denied')}), 403
    
    if not user.resume_path:
        return jsonify({'success': False, 'message': _('No resume found')}), 404
    
    try:
        # 构建完整文件路径
        file_path = os.path.join(current_app.config['RESUME_FOLDER'], 
                               os.path.basename(user.resume_path))
        
        # 删除文件
        if delete_file(file_path):
            # 清除数据库中的路径
            user.resume_path = None
            db.session.commit()
            logger.info(f"用户 {user.username} 的简历已删除")
            return jsonify({'success': True, 'message': _('Resume deleted successfully')})
        else:
            return jsonify({'success': False, 'message': _('Failed to delete resume')}), 500
    except Exception as e:
        logger.error(f"删除简历失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/resume_info/<int:user_id>')
@login_required
def resume_info(user_id):
    """获取简历文件信息"""
    user = User.query.get_or_404(user_id)
    if not (current_user.id == user_id or current_user.is_admin):
        return jsonify({'success': False, 'message': _('Permission denied')}), 403
    
    if not user.resume_path:
        return jsonify({'success': False, 'message': _('No resume found')}), 404
    
    try:
        file_path = os.path.join(current_app.config['RESUME_FOLDER'], 
                               os.path.basename(user.resume_path))
        file_info = get_file_info(file_path)
        
        if file_info:
            return jsonify({
                'success': True,
                'data': {
                    'filename': file_info['filename'],
                    'size': file_info['size'],
                    'created': file_info['created'],
                    'modified': file_info['modified'],
                    'url': user.resume_path
                }
            })
        else:
            return jsonify({'success': False, 'message': _('File not found')}), 404
    except Exception as e:
        logger.error(f"获取简历信息失败: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500