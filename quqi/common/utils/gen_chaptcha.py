from io import BytesIO
from random import choices

from captcha.image import ImageCaptcha
from flask import make_response, session
from flask_login import current_user
from PIL import Image


def gen_captcha(content="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"):
    """生成验证码"""
    image = ImageCaptcha()
    # 获取字符串
    captcha_text = "".join(choices(content, k=4))
    # 生成图像
    captcha_image = image.generate(captcha_text).read()
    return captcha_text, captcha_image


if __name__ == "__main__":
    print(gen_captcha())
