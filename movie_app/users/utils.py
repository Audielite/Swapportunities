import secrets
import os
from PIL import Image
from flask import url_for
from movie_app import mail
from flask_mail import Message
from flask import current_app


def save_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    pic_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(pic_size)
    i.save(picture_path)
    i.save(picture_path)
    return picture_fn

def send_email(user):
    token = user.reset_token()
    email_msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    email_msg.body = f''' Click the link to reset your password: {url_for('users.token_request', token=token, _external=True)} Ignore if you did request this reset '''
    mail.send(email_msg)

