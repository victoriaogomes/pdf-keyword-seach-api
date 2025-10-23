from kink import inject
from pymongo import MongoClient

from configs.env.env_settings import EnvSettings


@inject
class MongoDBClient:
    LOG_ERROR_CONNECTING = "Error connecting to MongoDB: {}"

    def __init__(self, env_settings: EnvSettings):
        try:
            mongo_uri = env_settings.mongo_db_uri.format(USERNAME=env_settings.mongo_db_username,
                                                         PASSWORD=env_settings.mongo_db_password)
            self.client = MongoClient(mongo_uri)
        except Exception as e:
            print(self.LOG_ERROR_CONNECTING.format(e))

    def get_client(self):
        return self.client
