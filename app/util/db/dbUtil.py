# app/db/dbUtil.py
from typing import List
import aiomysql

from app.util.db.dbPoolManager import database
from app.util.logging_util import logger as lgr
from app.util.app_util import AppSettings, appconfig


def create_query() -> str:

    # User inputs for ACC_NO and MARKET
    acc_no_list = [('60483129',), ('60434697',)]
    market_list = [('CDN',), ('US',)]

    # Convert lists to SQL-compatible format
    acc_no_values = ', '.join(f"('{acc[0]}')" for acc in acc_no_list)
    market_values = ', '.join(f"('{mkt[0]}')" for mkt in market_list)

    # Format the query with the user-provided values
    #lgr.info(f"appconfig.market_ws_stocks -> {appconfig.market_ws_stocks}")
    query = appconfig.market_ws_stocks.format(acc_no_values=acc_no_values, market_values=market_values)

    #lgr.info(f"Final With Query -> {query}")

    return query
    #query = query_template.format(acc_no_values=acc_no_values, market_values=market_values)


async def get_data_from_db(query, param) -> List[dict]:
    try:
        async with database.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:

                await cursor.execute(query)
                result = await cursor.fetchall()

        lgr.debug(f"Query Result {result}")
        return result
    except Exception as e:
        lgr.error('Error Getting Data from Database....%s', e)
        raise e


