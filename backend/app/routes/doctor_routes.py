from fastapi import APIRouter, HTTPException, status
from app.models.doctor import Doctor
from app.database import database as db
from bson import ObjectId
from datetime import datetime

doctor_router = APIRouter()

@doctor_router.post("/", response_model=Doctor)
async def create_doctor(doctor: Doctor):
    doctor_dict = doctor.dict(by_alias=True)
    result = db["doctors"].insert_one(doctor_dict)
    doctor_dict["_id"] = result.inserted_id
    return doctor_dict

@doctor_router.get("/{doctor_id}", response_model=Doctor)
async def get_doctor(doctor_id: str):
    doctor = db["doctors"].find_one({"_id": ObjectId(doctor_id)})
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return Doctor(**doctor)

@doctor_router.put("/{doctor_id}", response_model=Doctor)
async def update_doctor(doctor_id: str, doctor: Doctor):
    doctor_dict = doctor.dict(by_alias=True, exclude_unset=True)
    result = db["doctors"].update_one({"_id": ObjectId(doctor_id)}, {"$set": doctor_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")
    updated_doctor = db["doctors"].find_one({"_id": ObjectId(doctor_id)})
    return Doctor(**updated_doctor)

@doctor_router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: str):
    result = db["doctors"].delete_one({"_id": ObjectId(doctor_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return None
