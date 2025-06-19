from utils.auth import get_current_user
from utils.profile import get_user_details
from fastapi import APIRouter, Depends, Body
from utils.profile import add_dog_to_user, get_user_dogs
from fastapi import APIRouter, HTTPException
from utils.db import Database
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class FeedbackModel(BaseModel):
    experience: str
    easy_to_use: str
    liked_feature: str
    improvement: str
    additional_comments: Optional[str] = None

@router.get("/")
async def get_details(current_user: dict = Depends(get_current_user)):
    return get_user_details(current_user["user_id"])

@router.post("/dog/add")
async def add_dog(dog: dict = Body(...),current_user: dict = Depends(get_current_user)):
    return add_dog_to_user(current_user["user_id"], dog)


