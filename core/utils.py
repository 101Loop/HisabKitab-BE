import redis

from django.conf import settings


def get_redis_conn() -> redis.Redis:
    return redis.Redis.from_url(settings.REDIS_URL, retry_on_timeout=True)
