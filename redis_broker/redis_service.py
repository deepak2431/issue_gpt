import redis


def init_redis_client():
    """
    initiate the redis client
    """

    redis_client = redis.Redis(charset="utf-8", decode_responses=True)

    return redis_client
