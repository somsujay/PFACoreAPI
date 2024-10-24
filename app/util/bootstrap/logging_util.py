# import logging.config
# import os
# import util.bootstrap.boot_util as bu
#
# try:
#     dict_app_config = bu.read_app_config()
#     dict_bootstrap_config = bu.read_bootstrap_config()
#
#
#     env_type = dict_bootstrap_config.get('env-type')
#     #lgr.info(f"Environment type is : {env_type}")
#     if env_type == 'DEV':
#         project_root = 'DEVROOT'
#     elif env_type == 'PROD':
#         project_root = 'ROOT'
#     log_location = os.path.join(os.getenv(project_root), dict_bootstrap_config.get('log-location'))
#
#     if not os.path.exists(log_location):
#         os.makedirs(log_location)
#
#     logging.config.fileConfig(dict_bootstrap_config.get('log-config-file-name'), defaults={'logfilename': log_location+'dashboard-log'})
#     logger = logging.getLogger(__name__)
# except Exception as e:
#     print('Error Initializing Logger...%s', e)
