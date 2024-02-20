from quqi.common.utils.redis_utils import RedisStore

redis_store = RedisStore()


def init_redis_store(app):
    redis_store.init_app(app)
