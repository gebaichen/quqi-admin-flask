from functools import wraps

from flask import abort, session
from flask_login import current_user

from quqi.common.returns import *
from quqi.common.utils.response_code import RET


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_active:
                return abort(403)
            if permission not in session.get("permission", ""):
                return abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            roles = role.split("&")
            if not current_user.is_active:
                return abort(403)
            if current_user.role.code not in roles:
                return abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_required_api(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_active:
                return return_error_api(msg="你没有这个权限", code=RET.permission_error)
            if permission not in session["permission"]:
                return return_error_api(msg="你没有这个权限", code=RET.permission_error)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def permission_required_table_api(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_active:
                return return_table_error_api(msg="你没有这个权限", code=RET.permission_error)
            if permission not in session["permission"]:
                return return_table_error_api(msg="你没有这个权限", code=RET.permission_error)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def role_required_api(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            roles = role.split("&")
            if not current_user.is_active:
                return return_error_api(msg="你没有这个权限", code=RET.permission_error)
            if current_user.role.code not in roles:
                return return_error_api(msg="此用户角色不能进行操作", code=RET.permission_error)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def role_required_api_table(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            roles = role.split("&")
            if not current_user.is_active:
                return return_table_error_api(msg="你没有这个权限", code=RET.permission_error)
            if current_user.role.code not in roles:
                return return_table_error_api(
                    msg="此用户角色不能进行操作", code=RET.permission_error
                )
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def api_admin_required(f):
    return role_required_api("tea&admin")(f)


def admin_required(f):
    return role_required("tea&admin")(f)


def api_admin_table_required(f):
    return role_required_api_table("tea&admin")(f)


def login_api_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_active:
            return return_error_api(msg="请先登录之后再进行操作", code=RET.not_active)
        result = func(*args, **kwargs)
        return result

    return wrapper


def login_table_api_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_active:
            return return_table_error_api(msg="请先登录之后再进行操作", code=RET.not_active)
        result = func(*args, **kwargs)
        return result

    return wrapper
