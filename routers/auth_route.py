from fastapi import APIRouter, HTTPException, Response, Request, status
from pydantic import BaseModel
from utils.auth import register as reg, login as lg
from utils.authtoken import create_access_token, create_refresh_token, verify_token

router = APIRouter()

class UserModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
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

@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")
    
    payload = verify_token(refresh_token, "refresh")
    new_access_token = create_access_token({"user_id": payload["user_id"]})
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Successfully Logged out"}
