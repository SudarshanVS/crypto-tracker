from redis.asyncio import Redis, ConnectionPool

from config.settings import REDIS_URI, REDIS_MAX_CONNECTIONS


class RedisClient:
    def __init__(self):
        self.client = None
        self.pool = None

    async def connect(self):
        self.pool = ConnectionPool.from_url(
            url=REDIS_URI,
            decode_responses=True,
            max_connections=REDIS_MAX_CONNECTIONS
        )
        self.client = Redis(connection_pool=self.pool)


    async def disconnect(self):
        if self.client:
            await self.client.close()
            self.client = None
        if self.pool:
            await self.pool.disconnect()
            self.pool = None

    def get_client(self):
        return self.client


redis_client = RedisClient()

