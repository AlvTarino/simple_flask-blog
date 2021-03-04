import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail


# to set the users profile picture
def save_picture(form_picture):
    # Using secrets, we randomize the name of the picture uploaded so as to avoid picture names clashing
    random_hex = secrets.token_hex(8)
    # Using os.path.splitext, we get and save the extension of the picture uploaded
    # _ ->we want the file extension only, so we throw away the filename variable by putting an underscore
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Path where the uploaded picture will be saved
    picture_path = os.path.join(app.root_path, 'static/profiles', picture_fn)
    # resizing the uploaded image using Pillow
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# function to send resetting email with token to a specific user
def send_reset_email(user):
    # to get the token
    generated_token = user.get_reset_token()
    msg = Message(' Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('password_token', token=generated_token, _external=True) }
If you did not make this request then simply ignore this email and no changes will be made'''
    # to send the email with the token
    mail.send(msg)