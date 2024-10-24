# from util1.logging_util import logger as lgr
# import util1.bootstrap1.boot_util as bu
# import mariadb
from datetime import datetime
import os
import pandas as pd

# def get_connection():
#     bootstrap_config_dict = bu.read_bootstrap_config()
#
#     try:
#         connection = mariadb.connect(user=bootstrap_config_dict.get('user_name'),
#             password=bootstrap_config_dict.get('password'),
#             host=bootstrap_config_dict.get('host'),
#             database=bootstrap_config_dict.get('database')
#         )
#     except mariadb.DatabaseError as e:
#         lgr.error(f"Error reading data from MySQL table\n {e}")
#         #lgr.error(f'Exception: %s', e)
#         return None
#
#     return connection
#
# def get_data_from_db(get_query,params):
#     try:
#       conn = get_connection()
#       cur = conn.cursor()
#
#       cur.execute(get_query,params)
#     except mariadb.Error as e:
#       lgr.error(f"Error retrieving (get_data_from_db) entry from database: {e}")
#
#     return cur
#
# def get_data_from_db_new(get_query,params):
#     lgr.debug(f"Values : {get_query} {params}")
#
#     try:
#       conn = get_connection()
#       cur = conn.cursor()
#       cur.execute(get_query,params)
#     except mariadb.Error as e:
#       lgr.error(f"Error retrieving (get_data_from_db) entry from database: {e}")
#
#     return cur
#
#
# def add_specific_records(insert_statement, tbl_values):
#
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute(insert_statement, tbl_values)
#         lgr.debug("Successfully added entry to database")
#     except mariadb.Error as e:
#         lgr.error(f"Error adding (add_data_to_db) entry from database: {e}")
#         cur.close()
#     finally:
#         conn.commit()
#         cur.close()
#
# def add_bulk_data_to_db(insert_statement, insert_list):
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.executemany(insert_statement, insert_list)
#         lgr.debug("Successfully added entry to database")
#     except mariadb.Error as e:
#         lgr.error(f"Error adding (add_bulk_data_to_db) entry from database: {e}")
#         cur.close()
#     finally:
#         conn.commit()
#         cur.close()
#
# def update_specific_records(update_statement, update_params):
#     lgr.debug(f"Update Params: {update_params}")
#     lgr.debug(f'Update Statement: {update_statement}')
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute(update_statement, update_params)
#         lgr.debug("Successfully added entry to database")
#     except mariadb.Error as e:
#         lgr.error(f"Error updating (update_specific_records) entry from database: {e}")
#         cur.close()
#     finally:
#         conn.commit()
#         cur.close()
#
# def delete_specific_records(delete_statement, delete_params):
#     lgr.debug(f"Delete Params: {delete_params}")
#     lgr.debug(f'Delete Statement: {delete_statement}')
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute(delete_statement, delete_params)
#         lgr.debug("Successfully deleted from database")
#     except mariadb.Error as e:
#         lgr.error(f"Error deleting (delete_specific_records) entry from database: {e}")
#         cur.close()
#     finally:
#         conn.commit()
#         cur.close()
#
# def get_rs_as_pd(select_query, query_param):
#     records_cur = get_data_from_db(select_query,query_param)
#     db_records_desc = records_cur.description
#     db_records_column_list =[]
#
#     for i in range(len(db_records_desc)):
#         db_records_column_list.append(db_records_desc[i][0])
#
#     db_records = records_cur.fetchall()
#
#     lgr.debug(f"Database Records: --> {db_records}")
#
#     df = pd.DataFrame(db_records)
#     df.columns=db_records_column_list
#     lgr.debug(f"Data Frame of DB Records:  {df}")
#     return df
#
# ###################################DB Utils End here#######################################
#
# def rename_and_archive_any_file(input_file_path, arc_file_path, file_name, extension, prefix, postfix):
#
#     current_time_stamp = datetime.now()
#     new_name_w_ext =''
#     #old_name = tran_file_name
#     if (prefix == '' and postfix != ''):
#         new_name_w_ext = file_name + '_' + postfix + '_' + str(current_time_stamp.strftime("%d-%m-%y-%H.%M.%S.%f")) +extension
#     elif(prefix != '' and postfix == ''):
#         new_name_w_ext = prefix + '_' + file_name + '_' + str(current_time_stamp.strftime("%d-%m-%y-%H.%M.%S.%f")) +extension
#     elif (prefix == '' and postfix == ''):
#         new_name_w_ext = file_name + '_' + str(current_time_stamp.strftime("%d-%m-%y-%H.%M.%S.%f")) +extension
#     else:
#         new_name_w_ext = prefix + '_' + file_name + '_' + postfix + '_' + str(current_time_stamp.strftime("%d-%m-%y-%H.%M.%S.%f")) +extension
#
#
#     os.rename(input_file_path+file_name+extension, arc_file_path + new_name_w_ext)
#     lgr.debug(f"After Renaming & Moving: {new_name_w_ext}")
#
# def convert_list_to_dict(lst):
#     res_dict = {}
#     for i in range(0, len(lst), 2):
#         res_dict[lst[i]] = lst[i + 1]
#     return res_dict
#
#
# def convert_nested_list_to_list_of_tuple(nested_list):
#     list_of_tuple = []
#     for l in nested_list:
#         #print("==============>", tuple(l))
#         list_of_tuple.append(tuple(l))
#     return list_of_tuple
#
# def add_portfolio_stock(stock_info_dict):
#     dict_app_config = bu.read_app_config()
#     lgr.debug(f"Stock Info: \n {stock_info_dict}")
#     # stock_info = yf.Ticker(stock)
#     # lgr.debug("Stock Name: ", stock_info.info.get('longName'))
#     # # lgr.debug(stock_info.info)
#     lgr.debug(f"Stock Exchange: {stock_info_dict['price']['exchange']}")
#     lgr.debug(f"Stock Symbol: {stock_info_dict['symbol']}")
#     lgr.debug(f"Stock Long Name: {stock_info_dict['price']['longName']}")
#     lgr.debug(f"Stock Website: {stock_info_dict['summaryProfile']['website']}")
#
#     lgr.debug(f"Stock Industry: {stock_info_dict['summaryProfile']['industry']}")
#     lgr.debug(f"Stock Sector: {stock_info_dict['summaryProfile']['sector']}")
#     lgr.debug(f"Stock MarketCap: {stock_info_dict['price']['marketCap']['raw']}")
#     lgr.debug(f"Stock Country: {stock_info_dict['summaryProfile']['country']}")
#
#     add_specific_records(dict_app_config.get('insert-portfolio-stock'),
#                          (stock_info_dict['price']['exchange'], stock_info_dict['symbol'],
#                           stock_info_dict['price']['longName'],
#                           stock_info_dict['summaryProfile']['website'], stock_info_dict['summaryProfile']['industry'],
#                           stock_info_dict['summaryProfile']['sector'],
#                           stock_info_dict['price']['marketCap']['raw'], stock_info_dict['summaryProfile']['country'], 'Y'))
#
#     lgr.info(f"Deleting Daily Stock Price and Daily Stats for (Symbol) : {stock_info_dict.get('symbol')}"
#              f" Exchange: {stock_info_dict['price']['exchange']} ")
#     lgr.info(f"Deleting Daily Stock Price and Daily {stock_info_dict.get('symbol')} Stock Industry: {stock_info_dict['summaryProfile']['industry']} ")
#     lgr.info(f"Deleting Daily Stock Price and Daily {stock_info_dict.get('symbol')} Stock Sector: {stock_info_dict['summaryProfile']['sector']}")
#
#     delete_specific_records(dict_app_config.get('delete-from-daily-stock-price'), [stock_info_dict.get('symbol')])
#     delete_specific_records(dict_app_config.get('delete-from-daily-stats'), [stock_info_dict.get('symbol')])
#
# def get_local_user_root():
#     bootstrap_config_dict = bu.read_bootstrap_config()
#
#     env_type = bootstrap_config_dict.get('env-type')
#     lgr.info(f"Environment type is : {env_type}")
#     if env_type  == 'DEV':
#         project_root = os.getenv('DEVROOT')
#     elif env_type == 'PROD':
#         project_root = os.getenv('ROOT')
#
#     lgr.info(f"Root path: {project_root}")
#
#     return project_root
#
# def get_rs_as_pd_for_in(select_query, query_param):
#     records_cur = get_data_from_db_for_in(select_query,query_param)
#
#     lgr.debug(f"Select Query : {select_query}")
#     lgr.debug(f" Query Param : {query_param}")
#
#     db_records_desc = records_cur.description
#     db_records_column_list =[]
#
#     for i in range(len(db_records_desc)):
#         db_records_column_list.append(db_records_desc[i][0])
#
#     db_records = records_cur.fetchall()
#
#     lgr.debug(f"Database Records: --> {db_records}")
#
#     df = pd.DataFrame(db_records)
#     df.columns=db_records_column_list
#     lgr.debug(f"Data Frame of DB Records:  {df.tail(1)}")
#     return df
#
# def get_data_from_db_for_in(select_query_with_in,params_tuple):
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
#
#         #####Handle Tuple Here
#         lgr.debug(f"Select Query.... : {select_query_with_in}")
#         lgr.debug(f" Length ... : {len(params_tuple)}")
#         for i in range(len(params_tuple)):
#             lgr.debug(f" Query Param...params_tuple[{i}] : {params_tuple[i]}")
#
#         filtered_tuple_list = [t for t in params_tuple if t]
#         lgr.debug(f"filtered_tuple_list  {filtered_tuple_list}")
#
#         params_tuple =  filtered_tuple_list
#
#         if len(params_tuple) ==1:
#             query = select_query_with_in % (','.join(['%s'] * len(params_tuple[0])),)
#         elif len(params_tuple) == 2:
#             query = select_query_with_in % (','.join(['%s'] * len(params_tuple[0])), ','.join(['%s'] * len(params_tuple[1])))
#
#         lgr.debug(f"Select Query after Join Addition.... : {query}")
#
#         if len(params_tuple) ==1:
#             params = params_tuple[0]
#         elif len(params_tuple) ==2:
#             params = params_tuple[0] + params_tuple[1]
#
#         lgr.debug(f"  Param (params).after joining.. : {params}")
#
#         #############################
#
#         cur.execute(query,params)
#         #lgr.info(f"Just after execute query {cur.fetchall()}")
#     except mariadb.Error as e:
#         lgr.error(f"Error retrieving (get_data_from_db_for_in) entry from database: {e}")
#
#     return cur
#
