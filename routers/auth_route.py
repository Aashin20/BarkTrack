from fastapi import APIRouter, HTTPException, Response, Request, status
from pydantic import BaseModel, EmailStr
from utils.auth import register as reg, login as lg
from utils.authtoken import create_access_token, create_refresh_token, verify_token

router = APIRouter()

class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(user: UserModel):
    try:
        result = reg(name=user.name, email=user.email, password=user.password)
        return result["message"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(user: LoginModel, response: Response):
    user = lg(user.email, user.password)
    access_token = create_access_token({"user_id": user["id"], "name": user["name"], "email": user["email"]})
    refresh_token = create_refresh_token(user["id"])
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

