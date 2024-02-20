import hashlib
import os
import uuid
from datetime import datetime

from flask_configs import root_path


def save_pic(filename, content):
    image_url_path = os.path.join(root_path, "static", "images_avatar_url")
    if not os.path.exists(image_url_path):
        os.mkdir(image_url_path)
    sys_path = os.path.join(
        root_path, "static", "images_avatar_url", datetime.today().strftime("%Y-%m")
    )
    filepath = "/static/images_avatar_url/" + datetime.today().strftime("%Y-%m") + "/"
    if not os.path.exists(sys_path):
        os.mkdir(sys_path)
    img_suffix = "." + filename.split(".")[-1]
    file_name_uuid = uuid.uuid4().hex
    filename_hash = hashlib.md5(
        hashlib.md5(file_name_uuid.encode("utf-8")).hexdigest().encode("utf-8")
    ).hexdigest()
    new_file_name = filename_hash + img_suffix
    sys_path_file = os.path.join(sys_path, new_file_name)
    with open(sys_path_file, mode="wb") as f:
        f.write(content)
    return filepath + new_file_name
