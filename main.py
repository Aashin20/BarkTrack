from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel,EmailStr
from utils.auth import register as reg
import uvicorn
from utils.db import Database

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to MongoDB.....")
    Database.initialize()
    yield
    print("Shutting down MongoDB....")
    if Database.client:
        Database.client.close()

app=FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserModel(BaseModel):
    name : str
    email : EmailStr
    password : str

@app.post("/register")
async def register(user:UserModel):
    try:
        result=reg(name=user.name,email=user.email,password=user.password)
        return result["message"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
