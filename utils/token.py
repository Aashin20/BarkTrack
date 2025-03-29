from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
token_expiry_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
refresh_token_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
encryption_method = "HS256"


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str
    username: str

class User(BaseModel):
    id: str
    username: str


def create_access_token(user_data: dict, custom_expiry: Optional[timedelta] = None):
    token_content = user_data.copy()
    
    if custom_expiry:
        expiry_time = datetime.utcnow() + custom_expiry
    else:
        expiry_time = datetime.utcnow() + timedelta(minutes=token_expiry_minutes)
    
    token_content.update({
        "exp": expiry_time,
        "type": "access"
    })
    
    return jwt.encode(
        token_content,
        secret_key,
        algorithm=encryption_method
    )


def create_refresh_token(user_id: str):
    expiry_time = datetime.utcnow() + timedelta(days=refresh_token_days)
    
    refresh_token_data = {
        "user_id": user_id,
        "exp": expiry_time,
        "type": "refresh"
    }
    
    return jwt.encode(
        refresh_token_data,
        secret_key,
        algorithm=encryption_method
    )


def verify_token(token_to_verify: str, expected_token_type: str):
    try:
        token_data = jwt.decode(
            token_to_verify,
            secret_key,
            algorithms=[encryption_method]
        )
        
        actual_token_type = token_data.get("type")
        if actual_token_type != expected_token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This token isn't valid for this operation"
            )
        
        return token_data
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sorry, this token isn't valid"
        )