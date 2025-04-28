from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import bcrypt
from .db import Database
from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends,status
from .authtoken import verify_token

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

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
    

def login(email,password):
    users=Database.get_db().users
    user=users.find_one({"email":email})

    if user:
        passw=user.get('password')
        verification=bcrypt.checkpw(password.encode('utf-8'), passw.encode('utf-8')) 

        if verification:
            return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}
        
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
        
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Registered")



async def get_current_user(token: str = Depends(oauth2)):
    try:
        payload = verify_token(token, "access")
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
