from flask import current_app, request
from flask_restful import Resource

from quqi.common.decorator import (
    login_api_required,
    login_table_api_required,
    permission_required_api,
    permission_required_table_api,
)
from quqi.common.returns import (
    return_error_api,
    return_success_api,
    return_table_api,
    return_table_error_api,
)
from quqi.common.utils.response_code import RET
from quqi.extensions import db
from quqi.models import RoleModel, UserModel


class UserAPI(Resource):
    @login_table_api_required
    @permission_required_table_api("dashboard:system:user:read")
    def get(self, user_id):
        if user_id:
            return return_table_error_api(code=RET.get_error, msg="请求失败")
        page = request.args.get("page", type=int, default=1)
        # 获取一页有多少条数据
        limit = request.args.get("limit", type=int, default=10)
        try:
            users = UserModel.query.paginate(page=page, per_page=limit, error_out=False)
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_table_error_api(code=RET.commit_error, msg="操作失败")
        data = [
            {
                "id": user.id,
                "name": user.username,
                "role": user.role.name,
                "role_id": user.role.id,
                "role_code": user.role.code,
                "mobile": user.mobile,
                "email": user.email,
                "address": user.address,
            }
            for user in users.items
        ]
        return return_table_api(count=users.total, data=data)

    @login_api_required
    @permission_required_api("dashboard:system:user:add")
    def post(self, user_id):
        if user_id:
            return return_error_api(code=RET.get_error, msg="请求错误")
        user_name = request.json.get("name")
        user_email = request.json.get("email")
        user_mobile = request.json.get("mobile")
        if not user_name:
            return return_error_api(code=RET.header_data_is_small, msg="请求头缺少")
        # 判断手机号，用户名邮箱是否唯一
        u_n = UserModel.query.filter(UserModel.username == user_name).first()
        u_e = UserModel.query.filter(UserModel.email == user_email).first()
        u_m = UserModel.query.filter(UserModel.mobile == user_mobile).first()
        if u_n or u_e or u_m:
            return return_error_api(code=RET.header_data_error, msg="注册信息重复")
        user_new = UserModel()
        user_new.username = user_name
        user_new.email = user_email
        user_new.mobile = user_mobile
        user_new.role_id = 1
        user_new.set_password_hash("123456")
        try:
            # 保存
            user_new.save_add_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
        user_new.save_add_db()
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:user:edit")
    def put(self, user_id):
        if not user_id:
            return return_error_api(code=RET.get_error, msg="请求失败")
        user: UserModel = UserModel.query.get(user_id)
        if not user:
            return return_error_api(code=RET.get_error, msg="没有此学生")
        stu_name_new = request.json.get("name")
        if not stu_name_new:
            return return_error_api(code=RET.header_data_is_small, msg="请求头缺少")
        user.username = stu_name_new
        try:
            # 保存
            user.save_add_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:user:del")
    def delete(self, user_id):
        if not user_id:
            return return_error_api(code=RET.get_error, msg="请求失败")
        user: UserModel = UserModel.query.get(user_id)
        if not user:
            return return_error_api(code=RET.get_error, msg="没有此学生")
        try:
            # 保存
            user.save_delete_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
        return return_success_api()


class UserGiveRole(Resource):
    @login_api_required
    @permission_required_api("dashboard:system:user:add")
    def post(self, user_id):
        role_code = request.json.get("role_code")
        if not all([role_code, user_id]):
            return return_error_api(code=RET.get_error, msg="请求失败")
        user: UserModel = UserModel.query.get(user_id)
        if not user:
            return return_error_api(code=RET.get_error, msg="请求错误")
        role: RoleModel = RoleModel.query.filter(RoleModel.code == role_code).first()
        if not role:
            return return_error_api(code=RET.get_error, msg="请求错误")
        user.role_id = role.id
        try:
            # 保存
            user.save_add_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
        return return_success_api()
