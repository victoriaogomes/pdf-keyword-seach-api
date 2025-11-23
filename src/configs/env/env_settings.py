from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    mongo_db_uri: str
    mongo_db_username: str
    mongo_db_password: str
    open_search_host: str
    open_search_port: str


    class Config:
        env_file = ".env"