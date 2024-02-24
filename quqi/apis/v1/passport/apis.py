import datetime

from flask import current_app, make_response, request, session
from flask_login import login_user, logout_user
from flask_restful import Resource

from quqi.common.decorator import login_api_required
from quqi.common.ip2region import search_with_file
from quqi.common.returns import return_error_api, return_success_api
from quqi.common.utils.constants import IMAGE_CODE_REDIS_EXPIRES
from quqi.common.utils.gen_chaptcha import gen_captcha
from quqi.common.utils.response_code import RET
from quqi.extensions import db, redis_store
from quqi.models import UserModel


class Login(Resource):
    def post(self):
        mobile = request.json.get("mobile")
        password = request.json.get("password")
        remember_me = request.json.get("remember-me")
        image_code = request.json.get("image_code")
        image_code_id = request.json.get("image_code_id")
        ipv4 = request.remote_addr
        if not all([mobile, password, image_code, image_code_id]):
            return return_error_api(code=RET.header_data_is_small, msg="请求头数据缺少")

        real_image_code = redis_store.strict_redis.get("ImageCode_" + image_code_id)
        # 自动删除图片验证码，释放服务器内存
        redis_store.strict_redis.delete("ImageCode_" + image_code_id)
        if not real_image_code:
            return return_error_api(code=RET.code_expired, msg="验证码已经过期")
        if real_image_code != image_code.upper():
            return return_error_api(code=RET.code_wrong, msg="验证码输入时错误")  # 判断用户名或密码缺少
        if not mobile or not password:
            return return_error_api(
                code=RET.header_data_is_small, msg="用户名或密码缺少"
            )
        # 查找用户
        user = UserModel.query.filter(UserModel.mobile == mobile).first()
        # 判断用户名存不存在
        if not user:
            return return_error_api(code=RET.get_error, msg="用户不存在")
        # 判断密码是否正确
        if not user.check_password_hash(password):
            return return_error_api(code=RET.password_wrong, msg="密码错误")
        user.last_login = datetime.datetime.now()
        address = search_with_file(ipv4).split('|')
        user.address = address[2] + address[3]
        # 如果要记住我
        # 如果要记住我
        if all([remember_me]):
            # 就实现记住我

            login_user(user, remember=True)
        # 登录
        else:
            login_user(user)
        session["permission"] = ";".join([power.code for power in user.role.power])
        try:
            # 保存
            db.session.commit()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("登录失败")
            return return_error_api(code=RET.commit_error, msg="登录失败")
        next_url = request.args.get("next")
        # 设置到 cookie
        return return_success_api(msg="登录成功", next=next_url if next_url else "/")


class GetCaptcha(Resource):
    def get(self):
        image_code = request.args.get("imagecode")

        text, image_content = gen_captcha()
        redis_store.strict_redis.setex(
            "ImageCode_" + image_code, IMAGE_CODE_REDIS_EXPIRES, text
        )
        res = make_response(image_content)
        res.headers["Content-Type"] = "image/png"
        return res


class Logout(Resource):
    """
    退出登录
    """

    @login_api_required
    def get(self):
        # 退出登录
        try:
            logout_user()
            session.pop("permission")
        except Exception as e:
            # 添加log
            current_app.logger.error(e)
            return return_error_api(code=RET.logout_error, msg="退出登录异常")
        return return_success_api("退出登陆成功")
