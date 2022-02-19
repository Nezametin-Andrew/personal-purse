import asyncio
import pickle
import aioredis

from data import config


class UserStorage:

    data_pool = None

    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    async def redis_pool():
        UserStorage.data_pool = aioredis.from_url(**config.redis, db=3)

    async def get_data(self):
        async with self.data_pool.client() as conn:
            data = await conn.get(self.user_id)
            return pickle.loads(data)

    async def set_data(self, data):
        async with self.data_pool.client() as conn:
            await conn.set(self.user_id, pickle.dumps(data))

    async def update_data(self, key=None, data=None):
        old_data = await self.get_data()
        if key is None:
            old_data.update(data)
        else:
            old_data[key] = data
        await self.set_data(old_data)
        return await self.get_data()


asyncio.get_event_loop().run_until_complete(UserStorage.redis_pool())
