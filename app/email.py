from threading import Thread
from flask_mail import Message
from flask import current_app, render_template, url_for
from app import mail, app

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_reset_password_mail(user, token):
    reset_password_url = url_for('user.reset_password', token=token, _external=True)
    msg = Message('Hello',
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[user.email],
                  html=render_template('user/reset_password_mail.html', user=user, reset_password_url=reset_password_url))
    
    Thread(target=send_async_mail, args=(app, msg)).start()
