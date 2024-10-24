# import json
#
# import pandas as pd
# import requests
# from util import common_util as cu
# import yfinance as yf
# from util.logging_util import logger as lgr
# import util.bootstrap.boot_util as bu
#
# def get_exchange_rate(trade_date):
#     #temp_date = "2019-10-16"
#
#     bootstrap_config_dict = bu.read_bootstrap_config()
#     dict_app_config = bu.read_app_config()
#
#     api_url = bootstrap_config_dict.get('rapid-api-end-point')+trade_date
#     api_headers = bootstrap_config_dict.get('rapid-api-header')
#     query_params = dict_app_config.get('query-params')
#
#
#     response = requests.get(api_url, headers=api_headers, params=query_params)
#     response_dict = json.loads(response.text)
#
#     cad = response_dict.get("rates")[dict_app_config.get('currency-code-ca')]
#     usd = response_dict.get("rates")[dict_app_config.get('currency-code-us')]
#     #lgr.info("USD to CAD : ", cad / usd)
#     return cad / usd
#
#
# def check_stock_ticker(ticker):
#     try:
#         stock_info = get_stock_info(ticker)
#         lgr.debug(f"{stock_info}")
#         return stock_info
#     except Exception as e:
#         lgr.error('Exception: %s', e)
#         return None
#
# def get_stock_info(ticker):
#     bootstrap_config_dict = bu.read_bootstrap_config()
#     url = bootstrap_config_dict.get('rapid-api-get-summary-end-point')
#
#     querystring = {}
#
#     querystring['symbol'] = ticker
#
#     headers = bootstrap_config_dict.get('rapid-api-get-summary-header')
#     response = requests.get(url, headers=headers, params=querystring)
#     stock_info = json.loads(response.text)
#     return stock_info
#
#
# def getCrossTab(accounts, market, stocks) -> pd.DataFrame:
#
#     url = "http://127.0.0.1:8000/cross_tab_from_db/"
#
#     payload = json.dumps({
#       "accounts": accounts,
#       "markets": market,
#       "stocks": stocks
#     })
#     headers = {
#       'Content-Type': 'application/json'
#     }
#
#      # Make the POST request
#     response = requests.request("POST", url, headers=headers, data=payload)
#
#     lgr.info(f"response  : {json.loads(response.text)}")
#
#     # Assuming the response content-type is application/json
#     #response_data = response.json()
#
#     response_dict = json.loads(response.text)
#
#     response_data  = response_dict
#
#     # Step 1: Extract and load the nested JSON string
#     if response_data is None or not response_data:
#         return []
#     else:
#         cross_tab_result_str = response_data.get("cross_tab_result")
#
#
#
#     cross_tab_result = json.loads(cross_tab_result_str)
#
#     columns = cross_tab_result["columns"]
#     #lgr.info(columns)
#
#     data = cross_tab_result["data"]
#     #lgr.info(data)
#
#     return pd.DataFrame(data, columns=columns)
#
#
