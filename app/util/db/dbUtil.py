# app/db/dbUtil.py
from typing import List
from app.util.db.dbPoolManager import database
import aiomysql

async def get_data_from_db() -> List[dict]:
    async with database.pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            query = """SELECT SYMBOL AS 'Stock',
                        CAST(ACC_NO AS CHAR) As
                        'Account', MARKET as 'Market',
                        QTY_IN_HAND as 'Quantity',
                        CONVERT(AVG_PRICE, DECIMAL(8, 2)) as 'AvgPrice', CONVERT(BOOK_VALUE, DECIMAL(8, 2))
                        AS
                        'BookValue',
                        CONVERT(GAIN_LOSS, DECIMAL(9, 2))
                        AS
                        'GainLoss', CONVERT(PCT_GAIN_LOSS, DECIMAL(5, 2))
                        AS
                        'PctGainLoss'
                        FROM
                        pfa_vw_current_statistics;"""

            # await cursor.execute("SELECT * FROM items")  # Adjust table name as necessary
            await cursor.execute(query)  # Adjust table name as necessary


            result = await cursor.fetchall()
    #print("get_data_from_db-->", result)
    return result

async def create_item(item: dict):
    async with database.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("INSERT INTO item (name,description) VALUES (%s, %s)",
                                 (item['name'], item['description']))
            await conn.commit()
