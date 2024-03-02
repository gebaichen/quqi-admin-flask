from flask import current_app, request
from flask_login import current_user
from flask_restful import Resource

from quqi.common.decorator import login_api_required, permission_required_api
from quqi.common.returns import return_error_api, return_success_api
from quqi.common.utils.response_code import RET
from quqi.extensions import db


class ProfilesBaseInfo(Resource):
    @login_api_required
    @permission_required_api("dashboard")
    def put(self):
        avatar = request.json.get("avatar")
        username = request.json.get("username")
        mobile = request.json.get("mobile")
        email = request.json.get("email")
        if not all([avatar, username, mobile, email]):
            return return_error_api(code=RET.header_data_is_small, msg="请求头缺少数据")
        current_user.avatar = avatar
        current_user.username = username
        current_user.mobile = mobile
        current_user.email = email
        try:
            # 保存
            current_user.save_add_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
        return return_success_api()
