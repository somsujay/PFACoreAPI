# app/db/dbUtil.py
from typing import List
import aiomysql

from app.util.db.dbPoolManager import database
#from app.util.appUtil import AppSettings, appconfig
from app.util.loggingUtil import logger as lgr

async def get_data_from_db(query) -> List[dict]:
    async with database.pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:

            lgr.debug(f" Query :  {query}")

            await cursor.execute(query)  # Adjust table name as necessary
            result = await cursor.fetchall()

    lgr.debug("Query Result", result)
    return result

# async def create_item(item: dict):
#     async with database.pool.acquire() as conn:
#         async with conn.cursor() as cursor:
#             await cursor.execute("INSERT INTO item (name,description) VALUES (%s, %s)",
#                                  (item['name'], item['description']))
#             await conn.commit()
