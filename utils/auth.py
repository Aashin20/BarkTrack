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
    db=client.auth_db
    users=db.users

    exists = users.find_one({"email":email})
    if exists:
        return "User already exists"
    
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
        return "Registered Successfully"
    

    


