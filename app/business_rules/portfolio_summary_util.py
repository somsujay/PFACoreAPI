import pandas as pd
from typing import List, Dict
import pandas as pd
#import util1.bootstrap1.boot_util as bu
#from util1 import common_util as cu
#from util1.logging_util import logger as lgr



# def cross_tab(data: List[Dict], index: str, columns: str, values: str) -> pd.DataFrame:
#     """
#     Cross-tabulate data based on given parameters.
#
#     :param data: List of dictionaries representing input data.
#     :param index: Column to group by rows.
#     :param columns: Column to group by columns.
#     :param values: Values to aggregate.
#     :return: DataFrame with cross-tabulation results.
#     """
#     df = pd.DataFrame(data)  # Convert the data (list of dicts) to a Pandas DataFrame
#     crosstab_df = pd.crosstab(index=df[index], columns=df[columns], values=df[values], aggfunc='sum').fillna(0)
#     return crosstab_df


#dict_app_config = bu.read_app_config()

#def create_crosstab(selected_acc_nos, selected_stocks, selected_market, unconditional):

def create_crosstab(stock_details_df) -> pd.DataFrame:

    #lgr.info(f"create_crosstab function......")

    df =stock_details_df

    # Crosstab for Quantity
    qty_sum = pd.crosstab(
        index=[df['Stock'], df['Account']],
        columns='Quantity',
        values=df['Quantity'],
        aggfunc='sum'
    )

    # Crosstab for AvgPrice (mean)
    avg_price_mean = pd.crosstab(
        index=[df['Stock'], df['Account']],
        columns='AvgPrice',
        values=df['AvgPrice'],
        aggfunc='mean'
    )

    # Crosstab for BookValue (sum)
    bookvalue_sum = pd.crosstab(
        index=[df['Stock'], df['Account']],
        columns='BookValue',
        values=df['BookValue'],
        aggfunc='sum'
    )

    # Crosstab for GainLoss (sum)
    gainloss_sum = pd.crosstab(
        index=[df['Stock'], df['Account']],
        columns='GainLoss',
        values=df['GainLoss'],
        aggfunc='sum'
    )

    # Crosstab for PctGainLoss (mean)
    pct_gainloss_mean = pd.crosstab(
        index=[df['Stock'], df['Account']],
        columns='PctGainLoss',
        values=df['PctGainLoss'],
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
    #category_totals['PctGainLoss'] = df.astype('GainLoss', / df['BookValue']
    category_totals['PctGainLoss'] = (pd.to_numeric(category_totals['GainLoss'], errors='coerce')
                                      / pd.to_numeric(category_totals['BookValue'], errors='coerce'))*100

    #lgr.debug(f"category_totals : {category_totals.tail(10)}")

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

