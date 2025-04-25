from flask import render_template, current_app
from flask_mail import Message
from flask_babel import _
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_application_accepted_email(application):
    send_email(
        _('[%(company)s] Your application has been accepted', company=current_app.config['COMPANY_NAME']),
        sender=current_app.config['MAIL_SENDER'],
        recipients=[application.applicant.email],
        text_body=_('''Dear %(username)s,

We are pleased to inform you that your application for the position of %(job_title)s has been accepted.

Please check your application status in your account for more details.

Best regards,
%(company)s Team
''', username=application.applicant.username,
    job_title=application.job.title,
    company=current_app.config['COMPANY_NAME']),
        html_body=None
    )

def send_application_rejected_email(application):
    send_email(
        _('[%(company)s] Update on your application', company=current_app.config['COMPANY_NAME']),
        sender=current_app.config['MAIL_SENDER'],
        recipients=[application.applicant.email],
        text_body=_('''Dear %(username)s,

Thank you for your interest in the position of %(job_title)s.

After careful consideration, we regret to inform you that we have decided to move forward with other candidates whose qualifications more closely match our current needs.

We appreciate your interest in joining our team and wish you the best in your job search.

Best regards,
%(company)s Team
''', username=application.applicant.username,
    job_title=application.job.title,
    company=current_app.config['COMPANY_NAME']),
        html_body=None
    ) 