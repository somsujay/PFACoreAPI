import pandas as pd

from app.util.db import dbUtil
from app.util.appUtil import AppSettings, appconfig
from app.util.loggingUtil import logger as lgr


async def getAccWiseStocksDetails(selected_accounts, selected_market, selected_stocks) -> pd.DataFrame:

    lgr.info(f"...............Account {selected_accounts} Market {selected_market} "
          f"Selected Stock: {selected_stocks}   ")

    stock_details_dict = await dbUtil.get_data_from_db(appconfig.current_summary_stock_list_all)
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

