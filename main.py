from fastapi import FastAPI,HTTPException,Depends, Response, Request,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from contextlib import asynccontextmanager
from pydantic import BaseModel,EmailStr
from utils.auth import register as reg,login as lg
import uvicorn
from utils.db import Database
from utils.token import create_access_token,verify_token,create_refresh_token

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to MongoDB.....")
    Database.initialize()
    yield
    print("Shutting down MongoDB....")
    if Database.client:
        Database.client.close()

app=FastAPI(lifespan=lifespan)
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")
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

class LoginModel(BaseModel):
    email : EmailStr
    password : str

@app.post("/register")
async def register(user:UserModel):
    try:
        result=reg(name=user.name,email=user.email,password=user.password)
        return result["message"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/login")
def login(user:LoginModel,response: Response):
    user = lg(user.email, user.password)
    access_token = create_access_token({"user_id": user["id"], "name": user["name"], "email": user["email"]})
    refresh_token = create_refresh_token(user["id"])
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")
    
    payload = verify_token(refresh_token, "refresh")
    new_access_token = create_access_token({"user_id": payload["user_id"]})
    return {"access_token": new_access_token, "token_type": "bearer"}

@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Successfully Logged out"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
