import os

from .init_assets import init_assets
from .init_cors import init_cors
from .init_csrf_from import *
from .init_database import *
from .init_limiter import *
from .init_login import *
from .init_migrate import *
from .init_redis import *

# 注册插件
from .init_session import *


def register_extensions(app):
    init_sqlalchemy(app)
    init_cors(app)
    init_migrate(app, db)
    init_login(app)
    init_redis_store(app)
    register_csrf_from(app)
    init_session(app)
    init_assets(app)
    config_name = os.getenv("FLASK_CONFIG")
    if config_name == "production":
        register_limiter(app)
