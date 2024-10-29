import aiomysql
from app.util.bootstrap_util import bootstrapper
from app.util.logging_util import logger as lgr # Import the loaded settings

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
        try:
            self.pool = await aiomysql.create_pool(**DATABASE_CONFIG)
        except Exception as e:
            lgr.error('Error Initializing Database Pool....%s', e)
            raise e

    async def close_pool(self):
        try:
            self.pool.close()
            await self.pool.wait_closed()
        except Exception as e:
            lgr.error('Error Closing Database Pool....%s', e)
            raise e

database = Database()
