from flask import Blueprint, Flask

# 添加auth 蓝图
passport_bp = Blueprint("passport", __name__)
# 导入所有auth 蓝图的路由
from .views import *


# 添加注册auth 蓝图的function
def register_passport_bp(app: Flask):
    app.register_blueprint(passport_bp)
