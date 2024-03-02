from flask import Blueprint, Flask

dashboard_bp = Blueprint("dashboard", __name__)

from .console import *
from .index import *
from .power import *
from .profiles import *
from .role import *
from .user import *


def register_dashboard_bp(app: Flask):
    app.register_blueprint(dashboard_bp)
