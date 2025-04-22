from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.main import bp
from app.models import Job, JobApplication
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template('main/index.html', title=_('Home'), jobs=jobs)

@bp.route('/job/<int:id>')
def job(id):
    job = Job.query.get_or_404(id)
    return render_template('main/job.html', title=job.title, job=job)

@bp.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    if JobApplication.query.filter_by(user_id=current_user.id, job_id=job_id).first():
        flash(_('You have already applied for this job.'))
        return redirect(url_for('main.job', id=job_id))
    
    application = JobApplication(applicant=current_user, job=job)
    db.session.add(application)
    db.session.commit()
    flash(_('Your application has been submitted.'))
    return redirect(url_for('main.job', id=job_id))

@bp.route('/my_applications')
@login_required
def my_applications():
    applications = JobApplication.query.filter_by(user_id=current_user.id)\
        .order_by(JobApplication.applied_at.desc()).all()
    return render_template('main/my_applications.html', 
        title=_('My Applications'), applications=applications)

@bp.route('/set_language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('main.index')) 