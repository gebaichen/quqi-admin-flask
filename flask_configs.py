# filename:flask_configs.py
import datetime
import logging
import os

from dotenv import load_dotenv

from quqi.extensions import redis_store

basedir = os.path.abspath(os.path.dirname(__name__))

dot_env_path = os.path.join(basedir, ".env")
flask_env_path = os.path.join(basedir, ".flaskenv")

if os.path.exists(dot_env_path):
    load_dotenv(dot_env_path)

if os.path.exists(flask_env_path):
    load_dotenv(flask_env_path)
root_path = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev key")
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "dev key")
    # redis配置
    redis_host = os.getenv("redis-host", "127.0.0.1")
    redis_port = os.getenv("redis-port", 6379)
    # redis密码如果有就配置
    redis_password = os.getenv("redis-password", None)
    REDIS_HOST = redis_host
    REDIS_PORT = redis_port
    REDIS_PASSWORD = redis_password
    SQLALCHEMY_DATABASE_URI = "sqlite:///quqi_admin.db"
    # 配置logging级别
    LOG_LEVEL = logging.DEBUG
    # 配置邮箱
    # Session保存配置
    SESSION_TYPE = "redis"
    # 开启session签名
    SESSION_USE_SIGNER = True
    # 指定 Session 保存的 redis
    SESSION_REDIS = redis_store.strict_redis
    # 设置需要过期
    SESSION_PERMANENT = False
    # 设置过期时间
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=10)

    # 配置jsonify返回json的编码支持中文
    JSON_AS_ASCII = False


class DevelopmentConfig(BaseConfig):
    """开发配置"""

    ASSETS_DEBUG = True


class TestingConfig(BaseConfig):
    """测试配置"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # 内存数据库


class ProductionConfig(BaseConfig):
    """生成环境配置"""

    mysql_host = os.getenv("mysql-host", "127.0.0.1")
    mysql_password = os.getenv("mysql-password", "123456")
    mysql_port = os.getenv("mysql-port", 3306)
    mysql_user = os.getenv("mysql-user", "root")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/quqiadminflask?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.ERROR


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
