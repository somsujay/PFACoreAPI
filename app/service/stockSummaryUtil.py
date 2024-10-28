from typing import Dict

import pandas as pd

from app.util.db import dbUtil
from app.util.app_util import AppSettings, appconfig
from app.util.logging_util import logger as lgr


async def get_acc_wise_stocks_details(selected_accounts, selected_market, selected_stocks) -> pd.DataFrame:
    try:
        lgr.info(f"...............Account {selected_accounts} Market {selected_market} "
              f"Selected Stock: {selected_stocks}   ")


        stock_details_dict = await dbUtil.get_data_from_db(appconfig.current_summary_stock_list_all, None)
        stock_detail_df = pd.DataFrame(stock_details_dict)  # stock_detail_df_g

        if len(selected_accounts) == 0:
            lgr.info(f"No Accounts are selected........... ")
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

        # Crosstab for Quantity
        qty_sum = pd.crosstab(
            index=[stock_detail_df['Stock'], stock_detail_df['Account']],
            columns='Quantity',
            values=stock_detail_df['Quantity'],
            aggfunc='sum'
        )

        # Crosstab for AvgPrice (mean)
        avg_price_mean = pd.crosstab(
            index=[stock_detail_df['Stock'], stock_detail_df['Account']],
            columns='AvgPrice',
            values=stock_detail_df['AvgPrice'],
            aggfunc='mean'
        )

        # Crosstab for BookValue (sum)
        bookvalue_sum = pd.crosstab(
            index=[stock_detail_df['Stock'], stock_detail_df['Account']],
            columns='BookValue',
            values=stock_detail_df['BookValue'],
            aggfunc='sum'
        )

        # Crosstab for GainLoss (sum)
        gainloss_sum = pd.crosstab(
            index=[stock_detail_df['Stock'], stock_detail_df['Account']],
            columns='GainLoss',
            values=stock_detail_df['GainLoss'],
            aggfunc='sum'
        )

        # Crosstab for PctGainLoss (mean)
        pct_gainloss_mean = pd.crosstab(
            index=[stock_detail_df['Stock'], stock_detail_df['Account']],
            columns='PctGainLoss',
            values=stock_detail_df['PctGainLoss'],
            aggfunc='mean'
        )

        # Combine the crosstabs
        crosstab_combined = pd.concat([qty_sum, avg_price_mean, bookvalue_sum, gainloss_sum, pct_gainloss_mean], axis=1)

        # Adding category totals with sum and mean on the same row
        category_totals = crosstab_combined.groupby(level=0).agg(
            {
                'Quantity': 'sum',
                'AvgPrice': 'mean',
                'BookValue': 'sum',
                'GainLoss': 'sum',
                'PctGainLoss': 'mean'
            }
        )

        # Update the index to differentiate category totals
        category_totals.index = pd.MultiIndex.from_tuples(
            [(cat, 'Total') for cat in category_totals.index],
            names=['Stock', 'Account']
        )
        category_totals['PctGainLoss'] = (pd.to_numeric(category_totals['GainLoss'], errors='coerce')
                                          / pd.to_numeric(category_totals['BookValue'], errors='coerce'))*100

        lgr.debug(f"category_totals : {category_totals.tail(10)}")

        # Concatenate the data without sorting grand totals
        result = pd.concat([crosstab_combined, category_totals]).sort_index(level=0)


        result = result.astype({'Quantity': 'int32',
                                    'AvgPrice': 'float',
                                    'BookValue': 'float',
                                    'GainLoss': 'float',
                                    'PctGainLoss': 'float'})

        result.style.format({'Quantity': '{:,.0f}',
                                      'AvgPrice': '{:,.2f}',
                                      'BookValue': '{:,.2f}',
                                      'GainLoss': '{:,.2f}',
                                      'PctGainLoss': '{:,.32f}'
                                      })
        result = result.round(2)
        return result.reset_index()
    except Exception as e:
        lgr.error('Error Getting Data from Database....%s', e)
        raise e

async def get_market_wise_stocks(selected_accounts, selected_market) -> Dict:
    try:
        lgr.info("Som")
        myquery = create_query(appconfig.market_ws_stocks,selected_accounts,selected_market)

        #lgr.info(f"myquery ==> {myquery}")
        stock_details_dict = await dbUtil.get_data_from_db(myquery, None)

        lgr.debug(f"Sujay---> {stock_details_dict}")

        return stock_details_dict


    except Exception as e:
        lgr.error('Error Getting Data from Database....%s', e)
        raise e


def create_query(query, *params) -> str:

    # User inputs for ACC_NO and MARKET
    lgr.info(f"Parameters : Count: {len(params)} {params}")
    i=0
    query = appconfig.market_ws_stocks
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


