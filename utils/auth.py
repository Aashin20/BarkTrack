from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import bcrypt
from .db import Database

load_dotenv()

def register(name,email,password):
    users = Database.get_db().users
    exists = users.find_one({"email":email})
    if exists:
        return {"message":"User already exists"}
    
    else:
        bytes=password.encode('utf-8')
        salt=bcrypt.gensalt()
        hash=bcrypt.hashpw(bytes,salt).decode('utf-8')

        info={
            "name": name,
            "email":email,
            "password": hash
        }
        
        users.insert_one(info)  
        return {"message":"Registered Successfully"}
    

    


