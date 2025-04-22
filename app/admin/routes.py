from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flask_babel import _
from app import db
from app.admin import bp
from app.models import Job, JobApplication, User
from app.admin.forms import JobForm
from app.decorators import admin_required
from app.email import send_application_accepted_email, send_application_rejected_email

@bp.route('/')
@login_required
@admin_required
def index():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin/index.html', title=_('Admin Dashboard'), jobs=jobs)

@bp.route('/job/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            title_zh=form.title_zh.data,
            description=form.description.data,
            description_zh=form.description_zh.data,
            location=form.location.data,
            is_active=True
        )
        db.session.add(job)
        db.session.commit()
        flash(_('Job posting has been created.'))
        return redirect(url_for('admin.index'))
    return render_template('admin/create_job.html', title=_('Create Job'), form=form)

@bp.route('/job/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_job(id):
    job = Job.query.get_or_404(id)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        job.title = form.title.data
        job.title_zh = form.title_zh.data
        job.description = form.description.data
        job.description_zh = form.description_zh.data
        job.location = form.location.data
        db.session.commit()
        flash(_('Job posting has been updated.'))
        return redirect(url_for('admin.index'))
    return render_template('admin/edit_job.html', title=_('Edit Job'), form=form)

@bp.route('/job/<int:id>/toggle')
@login_required
@admin_required
def toggle_job(id):
    job = Job.query.get_or_404(id)
    job.is_active = not job.is_active
    db.session.commit()
    flash(_('Job status has been updated.'))
    return redirect(url_for('admin.index'))

@bp.route('/applications/<int:job_id>')
@login_required
@admin_required
def view_applications(job_id):
    job = Job.query.get_or_404(job_id)
    applications = JobApplication.query.filter_by(job_id=job_id)\
        .order_by(JobApplication.applied_at.desc()).all()
    return render_template('admin/applications.html', 
        title=_('Applications for {}').format(job.title),
        job=job, applications=applications)

@bp.route('/application/<int:id>/status/<status>')
@login_required
@admin_required
def update_application_status(id, status):
    if status not in ['pending', 'accepted', 'rejected']:
        flash(_('Invalid status.'))
        return redirect(url_for('admin.index'))
    
    application = JobApplication.query.get_or_404(id)
    application.status = status
    db.session.commit()
    flash(_('Application status has been updated.'))
    return redirect(url_for('admin.view_applications', job_id=application.job_id))

@bp.route('/application/<int:id>/accept')
@login_required
@admin_required
def accept_application(id):
    application = JobApplication.query.get_or_404(id)
    application.status = 'accepted'
    db.session.commit()
    send_application_accepted_email(application.applicant, application.job)
    flash(_('Application has been accepted.'))
    return redirect(url_for('admin.view_applications', job_id=application.job_id))

@bp.route('/application/<int:id>/reject')
@login_required
@admin_required
def reject_application(id):
    application = JobApplication.query.get_or_404(id)
    application.status = 'rejected'
    db.session.commit()
    send_application_rejected_email(application.applicant, application.job)
    flash(_('Application has been rejected.'))
    return redirect(url_for('admin.view_applications', job_id=application.job_id)) 