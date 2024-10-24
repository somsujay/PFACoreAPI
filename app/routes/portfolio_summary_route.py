import aiomysql
from fastapi import APIRouter, HTTPException
import app.business_rules.portfolio_summary_util as psu
import pandas as pd

#from app.db.database import get_db_pool
from app.models import CrossTabRequest
from app.db import crud
from app.util.bootstrap.boot_util import bootstrapper  # Import the loaded settings


router = APIRouter()

# @router.get("/status/")
# async def get_status():
#     return {
#         # "debug": settings.debug,
#         # "secret_key": settings.secret_key,
#         "db_host": bootstrapper.db_host
#     }

@router.post("/cross_tab_from_db/")
# async def get_cross_tab_from_db(request: CrossTabRequest):
#     """
#     POST request to process data from the database and return a cross-tabulation DataFrame.
#     """
#     pool = await get_db_pool()
#
#     selected_accounts = request.accounts
#     selected_market = request.markets
#     selected_stocks = request.stocks
#
#     print("accounts --> ",selected_accounts )
#     print("markets --> ", selected_market)
#     print("stocks --> ", selected_stocks)
#
#     async with pool.acquire() as conn:
#         async with conn.cursor(aiomysql.DictCursor) as cursor:
#
#             # query = """
#             # SELECT category, subcategory, value
#             # FROM your_table_name;
#             # """  # Modify the table and column names as per your schema
#
#             query ="""SELECT SYMBOL AS 'Stock',
#             CAST(ACC_NO AS CHAR) As
#             'Account', MARKET as 'Market',
#             QTY_IN_HAND as 'Quantity',
#             CONVERT(AVG_PRICE, DECIMAL(8, 2)) as 'AvgPrice', CONVERT(BOOK_VALUE, DECIMAL(8, 2))
#             AS
#             'BookValue',
#             CONVERT(GAIN_LOSS, DECIMAL(9, 2))
#             AS
#             'GainLoss', CONVERT(PCT_GAIN_LOSS, DECIMAL(5, 2))
#             AS
#             'PctGainLoss'
#             FROM
#             pfa_vw_current_statistics;"""
#
#             await cursor.execute(query)
#             rows = await cursor.fetchall()  # Fetch data from DB
#
#             print(f"1. update_details_table...............Account {selected_accounts} Market {selected_market}  ")
#
#             #stock_detail_df = psu.create_crosstab (pd.DataFrame(rows)) #stock_detail_df_g
#             stock_detail_df = pd.DataFrame(rows)  # stock_detail_df_g
#             print("stock_detail_df ", stock_detail_df)
#
#             #selected_stocks = request.stocks #[table_data[i]['Stock'] for i in selected_rows if i < len(table_data)]
#
#             print(f"Selected Stock(s) :  {selected_stocks}")
#
#             if len(selected_accounts) == 0:
#                 print(f"No Accounts are selected........... ")
#                 return []  # No selection, return empty data
#
#             if len(selected_stocks) == 0:
#                 stock_detail_df = stock_detail_df[
#                     (stock_detail_df['Account'].isin(selected_accounts)) &
#                     (stock_detail_df['Market'].isin(selected_market))
#                     ]
#             elif len(selected_stocks) > 0:
#                 stock_detail_df = stock_detail_df[
#                     (stock_detail_df['Account'].isin(selected_accounts)) &
#                     (stock_detail_df['Market'].isin(selected_market)) &
#                     (stock_detail_df['Stock'].isin(selected_stocks))
#                     ]
#
#             # Process the fetched data using cross_tab function
#             if rows:
#                 # Convert rows (list of dicts) to cross-tab format
#                 #result_df = cross_tab(rows, request.index, request.columns, request.values)
#                 result_df =  psu.create_crosstab (stock_detail_df)
#                 result_json = result_df.to_json(orient='split')  # Convert DataFrame to JSON
#
#                 return {"cross_tab_result": result_json}
#             else:
#                 raise HTTPException(status_code=404, detail="No data found")

async def get_cross_tab_from_db(request: CrossTabRequest):
    """
    POST request to process data from the database and return a cross-tabulation DataFrame.
    """
    # pool = await get_db_pool()

    selected_accounts = request.accounts
    selected_market = request.markets
    selected_stocks = request.stocks

    print("accounts --> ",selected_accounts )
    print("markets --> ", selected_market)
    print("stocks --> ", selected_stocks)

    items = await crud.fetch_items()

    # async with pool.acquire() as conn:
    #     async with conn.cursor(aiomysql.DictCursor) as cursor:
    #
    #         # query = """
    #         # SELECT category, subcategory, value
    #         # FROM your_table_name;
    #         # """  # Modify the table and column names as per your schema
    #
    #         query ="""SELECT SYMBOL AS 'Stock',
    #         CAST(ACC_NO AS CHAR) As
    #         'Account', MARKET as 'Market',
    #         QTY_IN_HAND as 'Quantity',
    #         CONVERT(AVG_PRICE, DECIMAL(8, 2)) as 'AvgPrice', CONVERT(BOOK_VALUE, DECIMAL(8, 2))
    #         AS
    #         'BookValue',
    #         CONVERT(GAIN_LOSS, DECIMAL(9, 2))
    #         AS
    #         'GainLoss', CONVERT(PCT_GAIN_LOSS, DECIMAL(5, 2))
    #         AS
    #         'PctGainLoss'
    #         FROM
    #         pfa_vw_current_statistics;"""
    #
    #         await cursor.execute(query)
    #         rows = await cursor.fetchall()  # Fetch data from DB

    print(f"1. update_details_table...............Account {selected_accounts} Market {selected_market}  ")

    #stock_detail_df = psu.create_crosstab (pd.DataFrame(rows)) #stock_detail_df_g
    stock_detail_df = pd.DataFrame(items)  # stock_detail_df_g
    print("stock_detail_df ", stock_detail_df)

    #selected_stocks = request.stocks #[table_data[i]['Stock'] for i in selected_rows if i < len(table_data)]

    print(f"Selected Stock(s) :  {selected_stocks}")

    if len(selected_accounts) == 0:
        print(f"No Accounts are selected........... ")
        return []  # No selection, return empty data

    if len(selected_stocks) == 0:
        stock_detail_df = stock_detail_df[
            (stock_detail_df['Account'].isin(selected_accounts)) &
            (stock_detail_df['Market'].isin(selected_market))
            ]
    elif len(selected_stocks) > 0:
        stock_detail_df = stock_detail_df[
            (stock_detail_df['Account'].isin(selected_accounts)) &
            (stock_detail_df['Market'].isin(selected_market)) &
            (stock_detail_df['Stock'].isin(selected_stocks))
            ]

    # Process the fetched data using cross_tab function
    if items:
        # Convert rows (list of dicts) to cross-tab format
        #result_df = cross_tab(rows, request.index, request.columns, request.values)
        result_df =  psu.create_crosstab (stock_detail_df)
        result_json = result_df.to_json(orient='split')  # Convert DataFrame to JSON

        return {"cross_tab_result": result_json}
    else:
        raise HTTPException(status_code=404, detail="No data found")

