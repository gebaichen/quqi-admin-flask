from flask import Blueprint, Flask

error_bp = Blueprint("error", __name__, url_prefix="/")

from .views import *


def register_error_bp(app: Flask):
    app.register_blueprint(error_bp)
