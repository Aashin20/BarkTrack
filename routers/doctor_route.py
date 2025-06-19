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

@router.get("/", response_model=List[dict])
async def list_doctors():
    collection = get_doctor_collection()
    doctors = []
    for doc in collection.find():
        doctors.append(doctor_helper(doc))
    return doctors

@router.get("/{doctor_id}", response_model=dict)
async def get_doctor(doctor_id: str):
    collection = get_doctor_collection()
    doc = collection.find_one({"_id": ObjectId(doctor_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor_helper(doc)

