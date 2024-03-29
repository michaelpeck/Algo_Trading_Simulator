__author__ = 'michaelpeck'

import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from src import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/assets/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    w, h = i.size
    if w > h:
        diff = (w - h)/2
        j = i.crop((diff,0,w-diff,h))
        j.thumbnail(output_size)
        j.save(picture_path)
    elif h > w:
        diff = (h - w)/2
        j = i.crop((0,diff,w,h-diff))
        j.thumbnail(output_size)
        j.save(picture_path)
    else:
        i.thumbnail(output_size)
        i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)