from fastapi import APIRouter, HTTPException, status
from app.models.appointment import Appointment
from app.database import database as db
from bson import ObjectId
from datetime import datetime

appointment_router = APIRouter()

@appointment_router.post("/", response_model=Appointment)
async def create_appointment(appointment: Appointment):
    appointment.createdAt = datetime.utcnow()
    appointment.updatedAt = datetime.utcnow()
    appointment_dict = appointment.dict(by_alias=True)
    result = db["appointments"].insert_one(appointment_dict)
    appointment_dict["_id"] = result.inserted_id
    return appointment_dict

@appointment_router.get("/{appointment_id}", response_model=Appointment)
async def get_appointment(appointment_id: str):
    appointment = db["appointments"].find_one({"_id": ObjectId(appointment_id)})
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return Appointment(**appointment)

@appointment_router.put("/{appointment_id}", response_model=Appointment)
async def update_appointment(appointment_id: str, appointment: Appointment):
    appointment.updatedAt = datetime.utcnow()
    appointment_dict = appointment.dict(by_alias=True, exclude_unset=True)
    result = db["appointments"].update_one({"_id": ObjectId(appointment_id)}, {"$set": appointment_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    updated_appointment = db["appointments"].find_one({"_id": ObjectId(appointment_id)})
    return Appointment(**updated_appointment)

@appointment_router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: str):
    result = db["appointments"].delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return None
