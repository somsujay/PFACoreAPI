import logging.config
import os
#import util.bootstrap.boot_util as bu

from app.util.bootStrapUtil import bootstrapper  # Import the loaded settings

try:
    #dict_app_config = bu.read_app_config()
    #dict_bootstrap_config = bu.read_bootstrap_config()


    env_type = bootstrapper.env_type   #dict_bootstrap_config.get('env-type')
    #lgr.info(f"Environment type is : {env_type}")
    if env_type == 'DEV':
        project_root = 'DEVROOT'
    elif env_type == 'PROD':
        project_root = 'ROOT'
#    log_location = os.path.join(os.getenv(project_root), dict_bootstrap_config.get('log-location'))
    log_location = os.path.join(os.getenv(project_root), bootstrapper.log_location)

    if not os.path.exists(log_location):
        os.makedirs(log_location)
    #print("---------------> Log File ", log_location+bootstrapper.log_file_name)
    #print("--------------->",os.getcwd())
    logging.config.fileConfig(bootstrapper.log_config_file_name, defaults={'logfilename': log_location+bootstrapper.log_file_name})
    logger = logging.getLogger(__name__)
except Exception as e:
    print('Error Initializing Logger...%s', e)
