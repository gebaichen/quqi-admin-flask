from flask import Blueprint, Flask

dashboard_bp = Blueprint("dashboard", __name__)

from .index import *
from .console import *
from .power import *
from .role import *
from .user import *
from .profiles import *

def register_dashboard_bp(app: Flask):
    app.register_blueprint(dashboard_bp)
