import os

from dota_team import app
from flask_login import current_user

from PIL import Image


def save_profile_img(form_img):
    _, file_ext = os.path.splitext(form_img.filename)
    file_name = f"{str(current_user.login)}{file_ext}"

    out_size = (288, 288)
    i = Image.open(form_img)
    i.thumbnail(out_size)

    save_path = os.path.join(app.root_path, "static/img", file_name)
    i.save(save_path)

    return file_name


def get_search_params(form):
    search_dict = {}

    # зато работает
    if form.mmr.data != "default":
        search_dict["mmr"] = form.mmr.data
    if form.aim.data != "defualt":
        search_dict["aim"] = form.aim.data  
    if form.position.data != "default":
        search_dict["position"] = form.position.data
    if form.login_search.data:
        search_dict["login"] = form.login_search.data
    
    return search_dict
