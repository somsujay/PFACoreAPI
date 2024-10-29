# app/db/dbUtil.py
from typing import List
import aiomysql

from app.util.db.dbPoolManager import database
from app.util.logging_util import logger as lgr
from app.util.app_util import AppSettings, appconfig

async def get_data_from_db(query) -> List[dict]:
    lgr.info(f"Query before DB Call:   {query}")
    try:
        #qry_with_param = build_query_with_param(query, params[0], params[1])
        #lgr.info(f"qry_with_param : {qry_with_param}")
        async with database.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:

                await cursor.execute(query)
                result = await cursor.fetchall()

        lgr.debug(f"Query Result {result}")
        return result
    except Exception as e:
        lgr.error('Error Getting Data from Database....%s', e)
        raise e

async def generate_specific_query(query, *params) -> str:

    # User inputs for ACC_NO and MARKET
    lgr.info(f"Parameters : Count: {len(params)} {params}")
    i=0
    #query = appconfig.market_ws_stocks
    #lgr.info(query1)
    try:
        for param in params:
            lgr.info(f"Parameter [{i}] : {param}")
            if i == 0:
                v0_tuple_list = [(p,) for p in param]
                lgr.info(f"v0_tuple_list {v0_tuple_list}")
                v0_values = ', '.join(f"('{v0_values[0]}')" for v0_values in v0_tuple_list)
                lgr.debug(f"v0_values : {v0_values}")
            elif i==1:
                v1_tuple_list = [(p,) for p in param]
                lgr.info(f"v1_tuple_list {v1_tuple_list}")
                v1_values = ', '.join(f"('{v1_values[0]}')" for v1_values in v1_tuple_list)
                lgr.debug(f"v1_values : {v1_values}")
                #query1 =  query1.format(p1=v1_values)
            elif i == 2:
                v2_tuple_list = [(p,) for p in param]
                lgr.info(f"v2_tuple_list {v2_tuple_list}")
                v2_values = ', '.join(f"('{v2_values[0]}')" for v1_values in v2_tuple_list)
                lgr.debug(f"v2_values : {v2_values}")

            i= i+1
            lgr.info(f"Value of i {i}")

        if len(params) == 3:
            query = query.format(p0= v0_values, p1= v1_values, p2 = v2_values)
            lgr.info(f"query --> {query}")
        elif len(params) == 2:
            query = query.format(p0=v0_values, p1=v1_values)
            lgr.info(f"query --> {query}")
        elif len(params)==1:
            query = query.format(p0=v0_values)
            lgr.info(f"query --> {query}")
        else:
            query = query

        stock_details_dict = await get_data_from_db(query)

        return stock_details_dict

    except Exception as e:
        lgr.error('Error in param processing....%s', e)
        raise e

    #acc_no_tuple_list = [(acc_no,) for acc_no in params[0]]

    #market_tuple_list = [(market,) for market in params[1]]
    #lgr.info(f"Parameters : acc_no_tuple_list= {acc_no_tuple_list}  market_tuple_list = {market_tuple_list}")

    # acc_no_list = [('60483129',), ('60434697',)]
    # market_list = [('CDN',), ('US',)]

    # Convert lists to SQL-compatible format
    #acc_no_values = ', '.join(f"('{acc[0]}')" for acc in acc_no_tuple_list)
    #market_values = ', '.join(f"('{mkt[0]}')" for mkt in market_tuple_list)

    # Format the query with the user-provided values
    #lgr.info(f"appconfig.market_ws_stocks -> {appconfig.market_ws_stocks}")
    #query = appconfig.market_ws_stocks.format(p0=acc_no_values, p1=market_values)

    #lgr.info(f"Final With Query -> {query}")

    return query
    #query = query_template.format(acc_no_values=acc_no_values, market_values=market_values)

