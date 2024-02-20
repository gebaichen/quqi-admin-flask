import os

import pymysql
from flask import Flask

from command import register_command
from flask_configs import config
from quqi.apis import register_api_bp
from quqi.common.utils.utils import setup_log
from quqi.extensions import register_extensions
from quqi.views import register_blueprint


def create_app(config_name=None):
    app = Flask("quqi-admin-flask")

    if not config_name:
        # 没有没有传入配置文件，则从本地文件读取
        config_name = os.getenv("FLASK_CONFIG", "development")
    # 记录log
    setup_log(config_name)
    # 添加config
    app.config.from_object(config[config_name])

    pymysql.install_as_MySQLdb()
    # 注册插件
    register_extensions(app)
    # 注册蓝图
    register_blueprint(app)
    # 注册api
    register_api_bp(app)
    # 注册自定义命令
    register_command(app)
    # 返回APP对象
    return app
