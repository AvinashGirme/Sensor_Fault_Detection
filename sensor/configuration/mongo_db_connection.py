import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import MONGODB_URL_KEY
import certifi
import os
ca=certifi.where()

class MonogoDBClient:
    client=None
    def __init__(self,database_name=DATABASE_NAME) -> None:
        try:
            if MonogoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                print(mongo_db_url)
                if "localhost" in mongo_db_url:
                    MonogoDBClient.client=pymongo.MongoClient(mongo_db_url)
                else:
                    MonogoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
                
                self.client=MonogoDBClient.client
                self.database=self.client[database_name]
                self.database_name=database_name
            except Exception as e:
                raise e
                
