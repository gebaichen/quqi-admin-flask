from flask import render_template
from flask_wtf.csrf import CSRFProtect

csrf_protect = CSRFProtect()


def register_csrf_from(app):
    # 注册app
    csrf_protect.init_app(app)
