from flask import render_template, current_app
from flask_mail import Message
from flask_babel import _
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_application_accepted_email(user, job):
    send_email(
        _('[Job Application] Application Accepted'),
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/application_accepted.txt', user=user, job=job),
        html_body=render_template('email/application_accepted.html', user=user, job=job)
    )

def send_application_rejected_email(user, job):
    send_email(
        _('[Job Application] Application Status Update'),
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/application_rejected.txt', user=user, job=job),
        html_body=render_template('email/application_rejected.html', user=user, job=job)
    ) 