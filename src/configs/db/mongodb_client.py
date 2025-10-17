from pymongo import MongoClient


class MongoDBClient:
    USERNAME = "db_user"
    PASSWORD = "iyJWiQYrMD8uifkQ"

    MONGO_URI_AUTH = f"mongodb+srv://{USERNAME}:{PASSWORD}@slrcluster.bedi13f.mongodb.net/?retryWrites=true&w=majority&appName=SLRCluster"

    def __init__(self):
        try:
            self.client = MongoClient(self.MONGO_URI_AUTH)
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_client(self):
        return self.client
