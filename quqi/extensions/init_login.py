from flask_login import LoginManager

login_manager = LoginManager()
# 需要权限的页面重定向到首页
login_manager.login_view = "passport.login"

import quqi.models


# 用于获取用户对象
@login_manager.user_loader
def load_user(user_id):
    return quqi.models.UserModel.query.get(user_id)


def init_login(app):
    login_manager.init_app(app)
