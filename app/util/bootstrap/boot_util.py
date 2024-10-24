#from distutils.command.config import config

import yaml
from pathlib import Path


# def read_bootstrap_config():
#     try:
#         with open('./config/bootstrap_config.yaml', 'r') as f:
#             bootstrap_config = yaml.safe_load(f)
#         return bootstrap_config
#     except:
#             print('Error Initializing Bootstrap Config File...')
#
#
# def read_app_config():
#     try:
#         with open('./config/application_config.yaml', 'r') as f:
#             app_config_dict = yaml.safe_load(f)
#         return app_config_dict
#     except:
#         print('Error Initializing Application Config File...')


from pydantic_settings import BaseSettings  # Use pydantic-settings instead of pydantic


class Settings(BaseSettings):
        db_host: str
        db_port: int
        db_user: str
        db_password: str
        db_name: str
        log_location: str
        log_config_file_name:  str


def load_config() -> Settings:
    # Load the YAML file
    current_path = Path().absolute()
    print(f"Current path: {current_path}")
    with open("./app/config/bootstrap_config.yaml", "r") as file:
        config = yaml.safe_load(file)

    # Create an instance of Settings populated with YAML data
    bootstrapper = Settings(
        db_host=config["database"]["host"],
        db_port=config["database"]["port"],
        db_user=config["database"]["user"],
        db_password=config["database"]["password"],
        db_name=config["database"]["name"],
        log_location=config["logging-param"]["log-location"],
        log_config_file_name=config["logging-param"]["log-config-file-name"]

    )
    print("Settings: ", bootstrapper)
    return bootstrapper


# Load settings
bootstrapper = load_config()


