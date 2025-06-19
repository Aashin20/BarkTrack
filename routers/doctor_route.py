from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from utils.db import get_doctor_collection
from utils.profile import doctor_helper

class DoctorBase(BaseModel):
    name: str
    phone_number: str
    specialty: str
    address: str

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    specialty: Optional[str] = None
    address: Optional[str] = None


router = APIRouter()

@router.post("/", response_model=dict)
async def create_doctor(doctor: DoctorCreate):
    doc = doctor.dict()
    collection = get_doctor_collection()
    result = collection.insert_one(doc)
    new_doc = collection.find_one({"_id": result.inserted_id})
    return {"message": "Doctor created", "doctor": doctor_helper(new_doc)}

