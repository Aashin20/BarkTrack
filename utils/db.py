from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
class Database:
    client = None
    db = None

    @classmethod
    def initialize(cls):
        if not cls.client:
            uri = os.getenv("URI")
            cls.client = MongoClient(uri, server_api=ServerApi('1'))
            cls.db = cls.client.auth_db
            try:
                cls.client.admin.command('ping')
                print("Connected to MongoDB!")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise e
    @classmethod
    def get_db(cls):
        if not cls.client:
            cls.initialize()
        return cls.db