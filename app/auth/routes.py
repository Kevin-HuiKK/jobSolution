from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import _
from app import db
from app.auth import bp
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm, ProfileForm, ChangePasswordForm
import traceback

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
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
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
        db.session.commit()
        flash(_('Your profile has been updated.'))
        return redirect(url_for('auth.profile'))
    return render_template('auth/profile.html', title=_('Edit Profile'), form=form)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash(_('Invalid current password'))
            return redirect(url_for('auth.change_password'))
        current_user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been changed.'))
        return redirect(url_for('main.index'))
    return render_template('auth/change_password.html', title=_('Change Password'), form=form) 