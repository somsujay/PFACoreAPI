import aiomysql
from app.util.bootStrapUtil import bootstrapper  # Import the loaded settings

DATABASE_CONFIG = {
    "host": bootstrapper.db_host,
    "port": bootstrapper.db_port,
    "user": bootstrapper.db_user,
    "password": bootstrapper.db_password,
    "db": bootstrapper.db_name

}

class Database:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        self.pool = await aiomysql.create_pool(**DATABASE_CONFIG)

    async def close_pool(self):
        self.pool.close()
        await self.pool.wait_closed()

database = Database()
