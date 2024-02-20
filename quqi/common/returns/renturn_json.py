from flask import jsonify

from quqi.common.utils.response_code import RET


def return_error_api(msg, code, **kwargs):
    result = {"code": code, "message": msg, "msg": msg, "success": False}
    result.update(kwargs)
    return jsonify(result)


def return_success_api(msg="成功", code=RET.ok, **kwargs):
    result = {"code": code, "message": msg, "msg": msg, "success": True}
    result.update(kwargs)
    return jsonify(result)


def return_table_api(count, data, msg="成功", code=RET.ok, **kwargs):
    result = {
        "code": code,
        "msg": msg,
        "message": msg,
        "count": count,
        "data": data,
        "success": True,
    }
    result.update(kwargs)
    return jsonify(result)


def return_table_error_api(msg, code, **kwargs):
    result = {
        "code": code,
        "msg": msg,
        "message": msg,
        "success": False,
    }
    result.update(kwargs)
    return jsonify(result)
