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
