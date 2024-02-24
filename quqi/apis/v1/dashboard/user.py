from flask import request, current_app
from flask_restful import Resource

from quqi.common.decorator import login_table_api_required, permission_required_table_api, login_api_required, \
    permission_required_api
from quqi.common.returns import return_error_api, return_success_api, return_table_error_api, return_table_api
from quqi.common.utils.response_code import RET
from quqi.models import UserModel, RoleModel


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
        if not user_name:
            return return_error_api(code=RET.header_data_is_small, msg="请求头缺少")
        user_new = UserModel()
        user_new.username = user_name
        user_new.role_id = 1
        user_new.set_password_hash("abc123456")
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
        user.save_put_db()
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:user:del")
    def delete(self, user_id):
        if not user_id:
            return return_error_api(code=RET.get_error, msg="请求失败")
        user: UserModel = UserModel.query.get(user_id)
        if not user:
            return return_error_api(code=RET.get_error, msg="没有此学生")
        user.save_delete_db()
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
        user.save_put_db()
        return return_success_api()
