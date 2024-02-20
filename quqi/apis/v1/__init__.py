from flask import Blueprint, Flask

from quqi.apis.v1.dashboard import register_dashboard_api
from quqi.apis.v1.passport import register_passport_api

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

register_passport_api(api_v1_bp)
register_dashboard_api(api_v1_bp)


# 注册一个api的蓝图
def register_api_v1_bp(app: Flask):
    app.register_blueprint(api_v1_bp)
