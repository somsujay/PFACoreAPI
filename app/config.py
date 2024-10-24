# import yaml
# from pydantic_settings import BaseSettings  # Use pydantic-settings instead of pydantic
#
#
# class Settings(BaseSettings):
#         debug: bool
#         secret_key: str
#         db_host: str
#         db_port: int
#         db_user: str
#         db_password: str
#         db_name: str
#
#
# def loadAppConfig() -> Settings:
#     # Load the YAML file
#     with open("config.yaml", "r") as file:
#         config = yaml.safe_load(file)
#
#     # Create an instance of Settings populated with YAML data
#     settings = Settings(
#         debug=config["app"]["debug"],
#         secret_key=config["app"]["secret_key"],
#         db_host=config["database"]["host"],
#         db_port=config["database"]["port"],
#         db_user=config["database"]["user"],
#         db_password=config["database"]["password"],
#         db_name=config["database"]["name"]
#     )
#
#     return settings
#
#
# # Load settings
# settings = loadAppConfig()
