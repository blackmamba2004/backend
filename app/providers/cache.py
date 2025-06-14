from dishka import Provider, Scope, provide

from redis.asyncio import Redis

from app.components import RedisCache
from app.config import RedisConfig


class RedisCacheProvider(Provider):
    scope = Scope.APP

    @provide
    def get_cache(
        self, config: RedisConfig
    ) -> RedisCache:
        return RedisCache(Redis.from_url(config.URI), config)
