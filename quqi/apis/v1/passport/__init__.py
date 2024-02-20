from flask_restful import Api

from .apis import GetCaptcha, Login, Logout


def register_passport_api(api_bp):
    # 集中注册 passport 下面的类视图
    # 最大的好处，方便管理，不需要关注每一个函数的细节
    passport_api = Api(api_bp)

    # rest full 风格的 api 服务器
    # 登录注册数据的操作
    passport_api.add_resource(Login, "/passport/login", endpoint="login")
    passport_api.add_resource(
        GetCaptcha, "/passport/getCaptcha", endpoint="get_captcha"
    )
    passport_api.add_resource(Logout, "/passport/logout", endpoint="logout")
