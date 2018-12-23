import os

from dota_team import app
from flask_login import current_user

from PIL import Image


def save_profile_img(form_img):
    _, file_ext = os.path.splitext(form_img.filename)
    file_name = f"{str(current_user.login)}{file_ext}"

    out_size = (128, 128)
    i = Image.open(form_img)
    i.thumbnail(out_size)

    save_path = os.path.join(app.root_path, "static/img", file_name)
    i.save(save_path)

    return file_name
