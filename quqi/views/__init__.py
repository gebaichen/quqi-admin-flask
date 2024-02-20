import os

from quqi.views.dashboard import register_dashboard_bp
from quqi.views.error import register_error_bp
from quqi.views.passport import register_passport_bp


def register_blueprint(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    # 注册报错蓝图
    config_name = os.getenv("FLASK_CONFIG")
    if config_name == "production":
        register_error_bp(app)
    register_passport_bp(app)
    register_dashboard_bp(app)
