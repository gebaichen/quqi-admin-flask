from copy import deepcopy

from flask import current_app, request
from flask_restful import Resource
from sqlalchemy import not_, or_

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
from quqi.models import PowerModel, RoleModel, UserModel


class PowerAPI(Resource):
    @login_table_api_required
    @permission_required_table_api("dashboard:system:power:read")
    def get(self, p_id):
        type = request.args.get("type", default="null")
        if p_id:
            return return_table_error_api(code=RET.get_error, msg="请求错误")
        if type == "tree":
            rights_all = db.session.execute(db.select(PowerModel)).scalars()
            rights_list = [
                {
                    "id": r.id,
                    "pid": r.pid if r.pid else 0,
                    "title": r.name,
                    "sort": r.sort,
                    "children_count": r.children.count(),
                    "type": r.type,
                }
                for r in rights_all
            ]
            # 2. 获取已有权限 id 集合
            # 3. 列表转属性组件
            rights_list.sort(key=lambda item: (item["pid"], item["id"]), reverse=True)
            tree_dict = {}
            # for i in rights_obj_list:
            #     if i.children.count() != 0 and i.type == "menu":
            #         rights_obj_list.remove(i)
            for rights_dict in rights_list:  # 遍历子节点
                # 2. 如果当前阶段已经存在于树状表格字典，则是父节点
                if rights_dict["id"] in tree_dict.keys():
                    # 将之前的节点添加到父节点之下
                    rights_dict["children"] = deepcopy(tree_dict[rights_dict["id"]])
                    rights_dict["children"].sort(key=lambda item: item["sort"])
                    del tree_dict[rights_dict["id"]]

                # 1. 如果父节点未出现在树状字典里面，就新增子节点列表，否则就追加
                if rights_dict["pid"] not in tree_dict.keys():
                    tree_dict[rights_dict["pid"]] = [rights_dict]
                else:
                    tree_dict[rights_dict["pid"]].append(rights_dict)
            return return_success_api(data=tree_dict[0])
            # return {"code": 0, "data": tree_dict.get(0)}
        else:
            page = request.args.get("page", type=int, default=1)
            per_page = request.args.get("limit", type=int, default=10)

            pages = PowerModel.query.filter(PowerModel.type == "menu").paginate(
                page=page, per_page=per_page, error_out=False
            )

            ret = []

            # 构建树状表格的数据
            for page in pages.items:
                data = page.json()
                data["children"] = []
                for child in page.children:
                    child_data = child.json()
                    if child.children:
                        child_data["children"] = [
                            sub_child.json() for sub_child in child.children
                        ]
                        child_data["isParent"] = True

                    data["children"].append(child_data)
                    data["isParent"] = True
                ret.append(data)
            return return_table_api(data=ret, count=pages.total)

    @login_api_required
    @permission_required_api("dashboard:system:power:add")
    def post(self, p_id):
        if p_id:
            return return_table_error_api(code=RET.get_error, msg="请求错误")
        code = request.json.get("code")
        name = request.json.get("name")
        pid = request.json.get("pid")
        sort = request.json.get("sort")
        type = request.json.get("type")
        url = request.json.get("url")
        if not all([code, name, sort, type]):
            return return_error_api(code=RET.header_data_is_small, msg="请求头缺少")
        power = PowerModel()
        power.code = code
        power.name = name
        power.pid = pid
        power.sort = sort
        power.type = type
        power.url = url
        power.save_add_db()
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:power:edit")
    def put(self, p_id):
        if not p_id:
            return return_table_error_api(code=RET.get_error, msg="请求错误")
        code = request.json.get("code")
        name = request.json.get("name")
        pid = request.json.get("pid")
        sort = request.json.get("sort")
        type = request.json.get("type")
        url = request.json.get("url")
        if not all([code, name, sort, type]):
            return return_error_api(code=RET.header_data_is_small, msg="请求头缺少")
        power = PowerModel.query.get(p_id)
        if not power:
            return return_error_api(code=RET.get_error, msg="没有数据")
        power.code = code
        power.name = name
        power.pid = pid
        power.sort = sort
        power.type = type
        if url:
            power.url = url
        power.save_put_db()
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:power:del")
    def delete(self, p_id):
        if not p_id:
            return return_table_error_api(code=RET.get_error, msg="请求错误")
        power: PowerModel = PowerModel.query.get(p_id)
        if not power:
            return return_error_api(code=RET.get_error, msg="没有数据")
        power.save_delete_db()
        return return_success_api()


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


class GiveRole(Resource):
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
