from flask import Blueprint, Flask

dashboard_bp = Blueprint("dashboard", __name__)

from .views import *


def register_dashboard_bp(app: Flask):
    app.register_blueprint(dashboard_bp)
