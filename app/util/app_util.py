from typing import Dict
import yaml
from pathlib import Path
from pydantic_settings import BaseSettings  # Use pydantic-settings instead of pydantic

from app.util.logging_util import logger as lgr


class AppSettings(BaseSettings):
        stock_market_cdn: Dict[str, str]
        #market_ws_stocks_no_arg: str
        current_summary_stock_list_all: str
        market_ws_stocks: str
        # db_port: int
        # db_user: str
        # db_password: str
        # db_name: str
        # log_location: str
        # log_config_file_name:  str
        # env_type: str
        # env_name: str
        # log_file_name: str

def loadAppConfig() -> AppSettings:
    # Load the YAML file
    try:
        current_path = Path().absolute()
        lgr.debug(f"Current Config File Path: {current_path}")
        with open("./app/config/app_config.yaml", "r") as file:
            config = yaml.safe_load(file)

        # Create an instance of Settings populated with YAML data
        appconfig = AppSettings(

            stock_market_cdn=config["stock-market"],
            #market_ws_stocks_no_arg=config["portfolio-stock-summary"]["market-ws-stocks-no-arg"],
            current_summary_stock_list_all=config["portfolio-stock-summary"]["current-summary-stock-list-all"],
            market_ws_stocks=config["portfolio-stock-summary"]["market-ws-stocks"]

        )
        #("AppConfig: ", appconfig)
        return appconfig
    except Exception as e:
        lgr.error('Error Initializing Bootstrap Config File....%s', e)
        raise e



# Load settings
appconfig = loadAppConfig()


