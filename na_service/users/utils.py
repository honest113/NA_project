import secrets, os
from flask import current_app
from PIL import Image
from na_service import celery, mail, Message


def save_picture(user_prefix, form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = user_prefix + "_" + random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_fn
    )
    i = Image.open(form_picture)
    width, height = i.size
    output_size = (width, height)
    if width > 160 or height > 160:
        if width > height :
            width = 160
            height = height/width * 160
        else :
            height = 160
            width = width/height * 160
        output_size = (width, height)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@celery.task
def send_reset_email(data):
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[data['user_email']])
    msg.body = data['body']
    mail.send(msg)