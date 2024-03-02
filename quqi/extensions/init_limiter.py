import os

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from quqi.common.returns import return_error_api
from quqi.common.utils.response_code import RET

redis_host = os.getenv("redis-host", "127.0.0.1")
redis_port = os.getenv("redis-port", 6379)
redis_password = os.getenv("redis-password", None)


def limit_key_func():
    return str(request.headers.get("X-Forwarded-For", "127.0.0.1"))


def index_ratelimit_error_responder(request_limit):
    return return_error_api(code=RET.limit_error, msg="访问受限制")


limiter = Limiter(
    key_func=(
        limit_key_func
        if os.getenv("FLASK_CONFIG") == "production"
        else get_remote_address
    ),
    # 每天200次，一小时50次
    default_limits=["4800 per day", "200 per hour", "50 per minute"],
    storage_uri=f"redis:{redis_password if redis_password else ''}//@{redis_host}:{redis_port}/1",
    on_breach=index_ratelimit_error_responder,
)


# limiter.


def register_limiter(app: Flask):
    limiter.init_app(app)
