from redis import StrictRedis


class RedisStore:
    def __init__(self, app=None):
        # 如果传入了APP对象
        if app is not None:
            # 注册插件
            self.init_app(app)
        # 创建一个空对象
        self.strict_redis: StrictRedis = None

    def init_app(self, app):
        # 配置 redis 数据库
        if "REDIS_HOST" not in app.config:
            raise Exception("需要先加载redis配置信息")
        # 创建一个对象
        redis_password = app.config["REDIS_PASSWORD"]
        # 三元表达式
        self.strict_redis = StrictRedis(
            host=app.config["REDIS_HOST"],
            port=app.config["REDIS_PORT"],
            decode_responses=True,
            password=redis_password if redis_password else None,
            db=2,
        )
        # 将APP对象加上一个strict_redis属性
        setattr(app, "strict_redis", self.strict_redis)
