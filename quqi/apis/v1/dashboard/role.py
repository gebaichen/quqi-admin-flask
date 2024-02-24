from flask import request, current_app
from flask_restful import Resource

from quqi.common.decorator import login_table_api_required, permission_required_table_api, login_api_required, \
    permission_required_api
from quqi.common.returns import return_error_api, return_success_api, return_table_error_api, return_table_api
from quqi.common.utils.response_code import RET
from quqi.extensions import db
from quqi.models import RoleModel, PowerModel


class RoleAPI(Resource):
    @login_table_api_required
    @permission_required_table_api("dashboard:system:role:read")
    def get(self, rid):
        type = request.args.get("type", default="null")
        if rid and type == "tree":
            role: RoleModel = db.session.execute(
                db.select(RoleModel).where(RoleModel.id == rid)
            ).scalar()
            # for i in rights_obj_list:
            #     if i.children.count() != 0 and i.type == "menu":
            #         rights_obj_list.remove(i)
            own_rights_list = [
                r.id
                for r in role.power
                if not (r.children.count() != 0 and r.type == "menu")
            ]
            return return_success_api(
                msg="返回角色权限数据成功",
                data=own_rights_list,
            )
            # return return_error_api(code=RET.get_error, msg="请求失败")
        page = request.args.get("page", type=int, default=1)
        # 获取一页有多少条数据
        limit = request.args.get("limit", type=int, default=10)
        try:
            roles = RoleModel.query.paginate(page=page, per_page=limit, error_out=False)
        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_table_error_api(code=RET.commit_error, msg="操作失败")
        data = [role.json() for role in roles.items]
        return return_table_api(count=roles.total, data=data)

    @login_api_required
    @permission_required_api("dashboard:system:role:add")
    def post(self, rid):
        if rid:
            return return_error_api(code=RET.get_error, msg="请求失败")
        code = request.json.get("code")
        name = request.json.get("name")
        if not all([code, name]):
            return return_error_api(code=RET.header_data_is_small, msg="请求失败")
        role = RoleModel()
        role.code = code
        role.name = name
        role.save_add_db()
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:role:edit")
    def put(self, rid):
        if not rid:
            return return_error_api(code=RET.get_error, msg="请求失败")
        role = RoleModel.query.get(rid)
        if not role:
            return return_error_api(code=RET.get_error, msg="请求失败")
        code = request.json.get("code")
        name = request.json.get("name")
        if not all([code, name]):
            return return_error_api(code=RET.header_data_is_small, msg="请求失败")
        role.code = code
        role.name = name
        role.save_put_db()
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:role:del")
    def delete(self, rid):
        if not rid:
            return return_error_api(code=RET.get_error, msg="请求失败")
        role = RoleModel.query.get(rid)
        if not role:
            return return_error_api(code=RET.get_error, msg="请求失败")
        role.save_delete_db()
        return return_success_api()


class RoleGivePower(Resource):
    @login_api_required
    @permission_required_api("dashboard:system:role:add")
    def put(self, rid):
        power_ids = request.json.get("power_ids", "")
        if not all([power_ids, rid]):
            return return_error_api(code=RET.header_data_is_small, msg="请求头缺少")
        try:
            rights_list = list(map(int, power_ids.split(",")))
        except Exception as e:
            current_app.logger.error(e)
            return return_error_api(code=RET.commit_error, msg="请求数据有问题")
        role: RoleModel = db.session.execute(
            db.select(RoleModel).where(RoleModel.id == rid)
        ).scalar()
        if not role:
            return return_error_api(code=RET.header_data_is_small, msg="无数据")
        # rights_obj_list = db.session.execute(
        #     db.select(PowerModel).where(PowerModel.id.in_(rights_list)).where(
        #         or_(not_(PowerModel.children), PowerModel.type != 'menu'))
        # ).all()
        rights_obj_list = PowerModel.query.filter(PowerModel.id.in_(rights_list)).all()
        # print(rights_obj_list)
        # for i in rights_obj_list:
        #     if i.children.count() != 0 and i.type == "menu":
        #         rights_obj_list.remove(i)
        if not rights_obj_list:
            return return_error_api(code=RET.header_data_is_small, msg="无数据")
        role.power = [r for r in rights_obj_list]
        role.save_put_db()
        return return_success_api()