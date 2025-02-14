from copy import deepcopy

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
from quqi.models import PowerModel


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
        r_n = PowerModel.query.filter(PowerModel.name == name).first()
        if r_n:
            return return_error_api(code=RET.header_data_error, msg="权限信息重复")
        power = PowerModel()
        power.code = code
        power.name = name
        power.pid = pid
        power.sort = sort
        power.type = type
        power.url = url
        try:
            # 保存
            power.save_add_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
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
        try:
            # 保存
            power.save_add_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
        return return_success_api()

    @login_api_required
    @permission_required_api("dashboard:system:power:del")
    def delete(self, p_id):
        if not p_id:
            return return_table_error_api(code=RET.get_error, msg="请求错误")
        power: PowerModel = PowerModel.query.get(p_id)
        if not power:
            return return_error_api(code=RET.get_error, msg="没有数据")
        try:
            # 保存
            power.save_delete_db()
        except Exception as e:
            # 失败就进行滚回操作
            db.session.rollback()
            # 添加log
            current_app.logger.error(e)
            current_app.logger.error("操作失败")
            return return_error_api(code=RET.commit_error, msg="操作失败")
        return return_success_api()
