from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

def register(name,email,password):
    uri=os.getenv("URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Connected to MongoDB!")
    except Exception as e:
        print(e)

    bytes=password.encode('utf-8')
    salt=bcrypt.gensalt()
    hash=bcrypt.hashpw(bytes,salt)

    
 


