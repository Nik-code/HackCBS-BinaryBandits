from fastapi import APIRouter, HTTPException, status
from app.models.hospital import Hospital
from app.database import database as db
from bson import ObjectId

hospital_router = APIRouter()

@hospital_router.post("/", response_model=Hospital)
async def create_hospital(hospital: Hospital):
    hospital_dict = hospital.dict(by_alias=True)
    result = db["hospitals"].insert_one(hospital_dict)
    hospital_dict["_id"] = result.inserted_id
    return hospital_dict

@hospital_router.get("/{hospital_id}", response_model=Hospital)
async def get_hospital(hospital_id: str):
    hospital = db["hospitals"].find_one({"_id": ObjectId(hospital_id)})
    if hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return Hospital(**hospital)

@hospital_router.put("/{hospital_id}", response_model=Hospital)
async def update_hospital(hospital_id: str, hospital: Hospital):
    hospital_dict = hospital.dict(by_alias=True, exclude_unset=True)
    result = db["hospitals"].update_one({"_id": ObjectId(hospital_id)}, {"$set": hospital_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Hospital not found")
    updated_hospital = db["hospitals"].find_one({"_id": ObjectId(hospital_id)})
    return Hospital(**updated_hospital)

@hospital_router.delete("/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hospital(hospital_id: str):
    result = db["hospitals"].delete_one({"_id": ObjectId(hospital_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return None
