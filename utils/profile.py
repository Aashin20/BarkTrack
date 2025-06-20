from bson import ObjectId
from .db import Database
from fastapi import HTTPException
import base64

def add_dog_to_user(user_id: str, dog_data: dict):
    users = Database.get_db().users

    if "image" in dog_data and isinstance(dog_data["image"], bytes):
        dog_data["image"] = base64.b64encode(dog_data["image"]).decode("utf-8")

    result = users.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"dogs": dog_data}}
    )

    if result.modified_count == 1:
        return {"message": "Dog added successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found or dog not added")

def get_user_dogs(user_id: str):
    users = Database.get_db().users
    user = users.find_one({"_id": ObjectId(user_id)}, {"dogs": 1})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get("dogs", [])

def get_user_details(user_id: str):
    users = Database.get_db().users
    user = users.find_one(
        {"_id": ObjectId(user_id)},
        {"password": 0}  
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user

def doctor_helper(doctor) -> dict:
    return {
        "id": str(doctor["_id"]),
        "name": doctor["name"],
        "phone_number": doctor["phone_number"],
        "specialty": doctor["specialty"],
        "address": doctor["address"],
    }
